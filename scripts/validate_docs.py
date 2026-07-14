"""Validate repository documentation structure before building MkDocs."""

from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

from markdown.extensions.toc import slugify


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs"
BOOK_ROOTS = [
    DOCS_ROOT / "engineering" / "documentation",
    DOCS_ROOT / "engineering" / "architecture",
    DOCS_ROOT / "engineering" / "guides",
    DOCS_ROOT / "engineering" / "protocols",
    DOCS_ROOT / "engineering" / "operations",
    DOCS_ROOT / "design" / "language",
    DOCS_ROOT / "design" / "system",
]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
METADATA_RE = re.compile(r"\A<!--\n(?P<body>.*?)\n-->", re.DOTALL)
REQUIRED_FIELDS = ("File", "Document", "Status", "Version")
DOCUMENT_ID_RE = re.compile(r"\b(?:MDP|MAD|MAC|MEG|MIP|MOP|MDL|MDS|MDG)-\d{3}\b")
VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")
H1_RE = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)
LINK_RE = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")
MARKDOWN_LINK_RE = re.compile(r"!?\[(?P<label>[^\]]*)\]\((?P<target>[^)]+)\)")
FENCED_BLOCK_RE = re.compile(
    r"^```(?P<language>[^\n]*)\n(?P<body>.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)
TEXT_DIAGRAM_ARROW_RE = re.compile(r"^\s*(?:↓|↑|→|←|↔|⇄|⇆|▼|▲)\s*$", re.MULTILINE)
TEXT_HIERARCHY_RE = re.compile(r"[├└]")
FILE_TREE_ENTRY_RE = re.compile(
    r"\b[^\s/]+\.(?:md|go|yaml|yml|json|css|toml|png|jpg|jpeg|svg|sql|sh|txt)\b",
    re.IGNORECASE,
)
NAMED_DOCUMENT_RE = re.compile(
    r"^(?P<id>(?:MDP|MAD|MAC|MEG|MIP|MOP|MDL|MDS|MDG)-\d{3})\s+—\s+(?P<title>.+)$"
)
UNAVAILABLE_MARKERS = ("planned; not yet published", "deferred; not yet published")
MANUAL_NAV_RE = re.compile(
    r"^(?:#{1,6}\s+|\*\*)(?:Previous|Next) File(?:\*\*)?\s*$",
    re.MULTILINE,
)
REVIEW_STATUS_RE = re.compile(r"^# Review Status\s*$", re.MULTILINE)
OWNER_RE = re.compile(r"^\|\s*Owner\s*\|\s*(?P<owner>[^|]+?)\s*\|$", re.MULTILINE)
GLOSSARY_BEFORE_REFERENCES_RE = re.compile(
    r"^(?P<indent>\s*)(?:- )?[Gg]lossary(?:\.md)?\n\n?"
    r"(?P=indent)(?:- )?[Rr]eferences(?:\.md)?$",
    re.MULTILINE,
)
REFERENCE_PAGE_RE = re.compile(r"^(?:\d+-)?references\.md$")
GLOSSARY_PAGE_RE = re.compile(r"^(?:\d+-)?glossary\.md$")


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def authored_markdown_files() -> list[Path]:
    root_pages = [ROOT / name for name in ("README.md", "AGENTS.md", "CLAUDE.md")]
    docs_pages = sorted(
        path for path in DOCS_ROOT.rglob("*.md") if "output" not in path.relative_to(DOCS_ROOT).parts
    )
    return [path for path in root_pages if path.is_file()] + docs_pages


def navigational_lines(text: str):
    """Yield lines that contain authored prose rather than comments or examples."""
    in_fence = False
    in_comment = False
    for number, line in enumerate(text.splitlines(), start=1):
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if "<!--" in line:
            if "-->" not in line.split("<!--", 1)[1]:
                in_comment = True
            continue
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence or re.match(r"^( {4}|\t)", line):
            continue
        yield number, line


def mask_inline_code(line: str) -> str:
    """Preserve offsets while excluding inline code from navigation checks."""
    return re.sub(r"(`+)(.*?)\1", lambda match: " " * len(match.group(0)), line)


def link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        return target[1:-1]
    if " " in target:
        return target.split(" ", 1)[0]
    return target


def discover_document_catalog(
    metadata: dict[Path, dict[str, str]], errors: list[str]
) -> dict[str, tuple[str, Path, Path]]:
    """Return document ID -> (canonical title, index path, specification folder)."""
    catalog: dict[str, tuple[str, Path, Path]] = {}
    for index in sorted(DOCS_ROOT.rglob("index.md")):
        fields = metadata.get(index)
        if not fields:
            continue
        document_id = fields.get("Document", "")
        if not DOCUMENT_ID_RE.fullmatch(document_id):
            continue
        heading = H1_RE.search(index.read_text(encoding="utf-8"))
        if not heading:
            errors.append(f"Specification index is missing H1: {relative_path(index)}")
            continue
        title = re.sub(
            rf"^{re.escape(document_id)}\s*[—-]\s*", "", heading.group("title").strip()
        ).strip()
        if document_id in catalog:
            errors.append(f"Document catalog repeats {document_id}: {relative_path(index)}")
            continue
        catalog[document_id] = (title, index, index.parent)
    return catalog


def owning_document(path: Path, catalog: dict[str, tuple[str, Path, Path]]) -> Optional[str]:
    for document_id, (_, _, folder) in catalog.items():
        try:
            path.relative_to(folder)
            return document_id
        except ValueError:
            pass
    return None


def resolve_local_target(path: Path, raw_target: str) -> tuple[Optional[Path], str]:
    target = link_target(raw_target)
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return None, ""
    file_part, _, fragment = target.partition("#")
    file_part = unquote(file_part.split("?", 1)[0])
    destination = path if not file_part else (path.parent / file_part).resolve()
    return destination, unquote(fragment)


@lru_cache(maxsize=None)
def heading_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        visible = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", match.group(1))
        visible = re.sub(r"[`*_~]", "", visible)
        base = slugify(visible, "-")
        count = counts.get(base, 0)
        anchor = base if count == 0 else f"{base}_{count}"
        counts[base] = count + 1
        anchors.add(anchor)
    return anchors


def parse_metadata(path: Path, text: str, errors: list[str]) -> Optional[dict[str, str]]:
    match = METADATA_RE.match(text)
    if not match:
        errors.append(f"Markdown file is missing top metadata comment: {relative_path(path)}")
        return None

    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key in fields:
            errors.append(f"Markdown metadata repeats {key}: {relative_path(path)}")
        fields[key] = value.strip()

    if "Specification" in fields:
        errors.append(f"Markdown metadata uses Specification instead of Document: {relative_path(path)}")

    for field in REQUIRED_FIELDS:
        if not fields.get(field):
            errors.append(f"Markdown metadata is missing {field}: {relative_path(path)}")

    declared_file = fields.get("File")
    if declared_file and declared_file != relative_path(path):
        errors.append(
            f"Markdown metadata has stale File path: {relative_path(path)} "
            f"(declares {declared_file})"
        )

    version = fields.get("Version")
    if version and not VERSION_RE.fullmatch(version):
        errors.append(f"Markdown metadata has invalid Version: {relative_path(path)} ({version})")

    return fields


def page_value(line: str) -> Optional[str]:
    stripped = line.strip()
    if not stripped.startswith("- "):
        return None

    value = stripped[2:].strip()
    if value and value[0] in {"'", '"'} and value.endswith(value[0]):
        value = value[1:-1]
    return value


def find_page(names: list[str], pattern: re.Pattern[str]) -> Optional[str]:
    return next((name for name in names if pattern.fullmatch(name)), None)


def validate_pages_navigation(book: Path, markdown_names: list[str], errors: list[str]) -> None:
    pages = book / ".pages"
    if not pages.is_file():
        errors.append(f"Book is missing .pages navigation: {relative_path(book)}")
        return

    entries = [value for line in pages.read_text(encoding="utf-8").splitlines() if (value := page_value(line))]
    reference = find_page(markdown_names, REFERENCE_PAGE_RE)
    glossary = find_page(markdown_names, GLOSSARY_PAGE_RE)
    required = ["index.md", "00-document-control.md", reference, glossary]

    missing = [name for name in required if name and name not in entries]
    if missing:
        errors.append(f"Book .pages omits required pages: {relative_path(pages)} ({', '.join(missing)})")
        return

    positions = [entries.index(name) for name in required if name]
    if positions != sorted(positions):
        errors.append(f"Book .pages has invalid chapter order: {relative_path(pages)}")


def table_value(text: str, field_names: tuple[str, ...]) -> Optional[str]:
    names = "|".join(re.escape(field) for field in field_names)
    match = re.search(rf"^\|\s*(?:{names})\s*\|\s*([^|]+?)\s*\|$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def validate_book(book: Path, metadata: dict[Path, dict[str, str]], errors: list[str]) -> None:
    if not SLUG_RE.fullmatch(book.name):
        errors.append(f"Book folder is not URL-safe: {relative_path(book)}")

    expected_id = "-".join(book.name.split("-")[:2]).upper()
    if not DOCUMENT_ID_RE.fullmatch(expected_id):
        errors.append(f"Book folder is missing a recognised document ID: {relative_path(book)}")

    markdown_files = sorted(book.rglob("*.md"))
    markdown_names = [path.name for path in markdown_files]
    reference = find_page(markdown_names, REFERENCE_PAGE_RE)
    glossary = find_page(markdown_names, GLOSSARY_PAGE_RE)
    for required in ("index.md", "00-document-control.md"):
        if required not in markdown_names:
            errors.append(f"Book is missing {required}: {relative_path(book)}")
    if reference is None:
        errors.append(f"Book is missing References: {relative_path(book)}")
    if glossary is None:
        errors.append(f"Book is missing Glossary: {relative_path(book)}")

    validate_pages_navigation(book, markdown_names, errors)

    values: dict[str, set[str]] = {field: set() for field in ("Document", "Status", "Version")}
    for path in markdown_files:
        fields = metadata.get(path)
        if not fields:
            continue
        for field in values:
            if fields.get(field):
                values[field].add(fields[field])

    for field, distinct in values.items():
        if len(distinct) != 1:
            errors.append(
                f"Book has inconsistent {field} metadata: {relative_path(book)} "
                f"({', '.join(sorted(distinct))})"
            )

    document_values = values["Document"]
    if document_values and next(iter(document_values)) != expected_id:
        errors.append(
            f"Book metadata does not match folder document ID: {relative_path(book)} "
            f"({next(iter(document_values))} != {expected_id})"
        )

    control = book / "00-document-control.md"
    if not control.is_file() or control not in metadata:
        return

    text = control.read_text(encoding="utf-8")
    fields = metadata[control]
    table_fields = {
        "Document": table_value(text, ("Document", "Document ID")),
        "Status": table_value(text, ("Status",)),
        "Version": table_value(text, ("Version",)),
    }
    for field, value in table_fields.items():
        if value is None:
            errors.append(f"Document Control table is missing {field}: {relative_path(control)}")
        elif value != fields.get(field):
            errors.append(
                f"Document Control table disagrees with {field} metadata: "
                f"{relative_path(control)} ({value} != {fields.get(field)})"
            )

    owner_match = OWNER_RE.search(text)
    if not owner_match:
        errors.append(f"Document Control table is missing Owner: {relative_path(control)}")
    elif owner_match.group("owner").lower().startswith("lead "):
        errors.append(f"Document Control uses role-based Lead owner: {relative_path(control)}")


def validate_local_links(path: Path, text: str, errors: list[str]) -> None:
    for line_number, raw_line in navigational_lines(text):
        line = mask_inline_code(raw_line)
        for match in LINK_RE.finditer(line):
            target = link_target(match.group("target"))
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            destination, fragment = resolve_local_target(path, target)
            if destination is None:
                continue
            if not destination.exists():
                errors.append(f"Broken local link: {relative_path(path)}:{line_number} ({target})")
                continue
            if fragment and destination.is_file() and destination.suffix.lower() == ".md":
                if fragment not in heading_anchors(destination):
                    errors.append(
                        f"Broken local link fragment: {relative_path(path)}:{line_number} "
                        f"({target})"
                    )


def validate_cross_references(
    path: Path,
    text: str,
    catalog: dict[str, tuple[str, Path, Path]],
    errors: list[str],
) -> None:
    owner = owning_document(path, catalog)
    for line_number, raw_line in navigational_lines(text):
        line = mask_inline_code(raw_line)
        links = list(MARKDOWN_LINK_RE.finditer(line))

        references = list(DOCUMENT_ID_RE.finditer(line))
        for reference_number, reference in enumerate(references):
            document_id = reference.group(0)
            containing_link = next(
                (link for link in links if link.start() <= reference.start() < link.end()), None
            )
            if document_id in catalog:
                if document_id != owner and containing_link is None:
                    errors.append(
                        f"Unlinked cross-document reference: "
                        f"{relative_path(path)}:{line_number} ({document_id})"
                    )
            else:
                if containing_link is not None:
                    errors.append(
                        f"Unavailable document identifier is linked: "
                        f"{relative_path(path)}:{line_number} ({document_id})"
                    )
                next_reference = (
                    references[reference_number + 1].start()
                    if reference_number + 1 < len(references)
                    else len(line)
                )
                marker_text = line[reference.end():next_reference]
                if not any(marker in marker_text for marker in UNAVAILABLE_MARKERS):
                    errors.append(
                        f"Unavailable document identifier lacks planned/deferred marker: "
                        f"{relative_path(path)}:{line_number} ({document_id})"
                    )

        for link in links:
            label = link.group("label")
            destination, _ = resolve_local_target(path, link.group("target"))
            for document_id in DOCUMENT_ID_RE.findall(label):
                if document_id not in catalog:
                    continue
                if destination is None or owning_document(destination, catalog) != document_id:
                    errors.append(
                        f"Document link points into the wrong specification: "
                        f"{relative_path(path)}:{line_number} ({document_id})"
                    )

            named = NAMED_DOCUMENT_RE.fullmatch(label.strip())
            if named and named.group("id") in catalog:
                canonical_title = catalog[named.group("id")][0]
                if named.group("title").strip() != canonical_title:
                    errors.append(
                        f"Document link uses a noncanonical title: "
                        f"{relative_path(path)}:{line_number} "
                        f"({named.group('id')} — {named.group('title').strip()})"
                    )


def validate_text_diagrams(path: Path, text: str, errors: list[str]) -> None:
    for match in FENCED_BLOCK_RE.finditer(text):
        if match.group("language").strip() not in {"", "text"}:
            continue

        body = match.group("body")
        line = text.count("\n", 0, match.start()) + 1
        if TEXT_DIAGRAM_ARROW_RE.search(body):
            errors.append(
                f"Text fence contains diagram arrows instead of Mermaid: "
                f"{relative_path(path)}:{line}"
            )

        if not TEXT_HIERARCHY_RE.search(body):
            continue

        nonempty = [candidate.strip() for candidate in body.splitlines() if candidate.strip()]
        has_directory = any(candidate.endswith("/") for candidate in nonempty)
        has_files = len(FILE_TREE_ENTRY_RE.findall(body)) >= 2
        if not has_directory and not has_files:
            errors.append(
                f"Text fence contains a non-file hierarchy instead of Mermaid: "
                f"{relative_path(path)}:{line}"
            )


def main() -> int:
    errors: list[str] = []
    markdown_files = sorted(
        path for path in DOCS_ROOT.rglob("*.md") if "output" not in path.relative_to(DOCS_ROOT).parts
    )
    authored_files = authored_markdown_files()
    metadata: dict[Path, dict[str, str]] = {}

    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        fields = parse_metadata(path, text, errors)
        if fields:
            metadata[path] = fields

        if REVIEW_STATUS_RE.search(text):
            errors.append(f"Markdown contains Review Status: {relative_path(path)}")
        if MANUAL_NAV_RE.search(text):
            errors.append(f"Markdown contains manual previous/next navigation: {relative_path(path)}")
        if GLOSSARY_BEFORE_REFERENCES_RE.search(text):
            errors.append(f"Markdown places Glossary before References: {relative_path(path)}")

    catalog = discover_document_catalog(metadata, errors)

    for path in authored_files:
        text = path.read_text(encoding="utf-8")
        validate_local_links(path, text, errors)
        validate_cross_references(path, text, catalog, errors)
        validate_text_diagrams(path, text, errors)

    books: list[Path] = []
    for folder in BOOK_ROOTS:
        if not folder.is_dir():
            errors.append(f"Missing documentation section: {relative_path(folder)}")
            continue
        books.extend(sorted(path for path in folder.iterdir() if path.is_dir()))

    for book in books:
        validate_book(book, metadata, errors)

    catalog_folders = {folder for _, _, folder in catalog.values()}
    for book in books:
        if book not in catalog_folders:
            errors.append(f"Specification is absent from document catalog: {relative_path(book)}")

    book_files = {path for book in books for path in book.rglob("*.md")}
    for path in set(markdown_files) - book_files:
        fields = metadata.get(path)
        heading = H1_RE.search(path.read_text(encoding="utf-8"))
        if fields and heading and fields.get("Document") != heading.group("title").strip():
            errors.append(
                f"Landing page Document metadata does not match H1: {relative_path(path)} "
                f"({fields.get('Document')} != {heading.group('title').strip()})"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Documentation validation passed ({len(authored_files)} authored Markdown pages, "
        f"{len(catalog)} catalogued specifications)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
