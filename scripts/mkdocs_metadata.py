"""MkDocs hook for rendering preserved specification metadata."""

from __future__ import annotations

import os
import posixpath
import re
from pathlib import Path
from pathlib import PurePosixPath


COMMENT_RE = re.compile(r"\A<!--\n(?P<body>.*?)\n-->\n?", re.DOTALL)
FIELD_RE = re.compile(r"^(?P<key>Document|Specification|Status|Version):\s*(?P<value>.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#\s+(?P<heading>.+)$", re.MULTILINE)
ID_RE = re.compile(r"\b(?P<id>(?:MDP|MAD|MAC|MEG|MIP|MOP|MDL|MDS|MDG)-\d{3})\b", re.IGNORECASE)
TITLE_ID_PREFIX_RE = re.compile(r"^(?:MDP|MAD|MAC|MEG|MIP|MOP|MDL|MDS|MDG)-\d{3}\s+[—-]\s+(.+)$", re.IGNORECASE)
SPECIFICATION_FOLDER_RE = re.compile(
    r"^(?P<id>(?:mdp|mad|mac|meg|mip|mop|mdl|mds|mdg)-\d{3})-(?P<title>.+)$"
)


def on_nav(nav, config, files):
    """Use page H1 headings as navigation titles instead of filename labels."""
    docs_dir = Path(config["docs_dir"])
    for page in _iter_pages(nav.items):
        heading = _heading_from_source(docs_dir / page.file.src_uri)
        if heading:
            page.title = _display_title(heading)
    return nav


def on_page_markdown(markdown: str, page, config, files) -> str:
    """Add a visible metadata block from the source file's top comment."""
    heading = _heading_from_markdown(markdown)
    if heading:
        page.title = _display_title(heading)

    match = COMMENT_RE.match(markdown)
    if not match:
        return markdown

    metadata = _parse_metadata(match.group("body"), markdown, page.file.src_uri)
    if not metadata:
        return markdown

    table = [
        '??? info "Document metadata"',
        "",
        f"    | Field | Value |",
        f"    | --- | --- |",
        f"    | {metadata['document_label']} | {metadata['document']} |",
        f"    | Status | {metadata['status']} |",
    ]
    # MDG-001 chapter 03 removes the document version field. Legacy pages that still
    # declare one keep rendering it until they are migrated.
    if metadata["version"]:
        table.append(f"    | Version | {metadata['version']} |")
    table.append("")

    return markdown[: match.end()] + "\n".join(table) + "\n" + markdown[match.end() :]


def on_page_content(html: str, page, config, files) -> str:
    """Add a specification-level PDF download to published pages."""
    if os.environ.get("ENABLE_PDF_DOWNLOADS", "").lower() not in {"1", "true", "yes"}:
        return html

    specification = _specification_from_path(page.file.src_uri)
    if not specification:
        return html

    document_id, folder = specification
    start = PurePosixPath(page.url)
    href = posixpath.relpath(f"downloads/{_pdf_name(folder)}", start=str(start))
    button = (
        '<a class="md-button mosaic-pdf-download" '
        f'href="{href}" download title="Download {document_id} as a single PDF">'
        f'Download {document_id} PDF</a>'
    )
    return button + html


def _iter_pages(items):
    for item in items:
        if hasattr(item, "file") and item.file.src_uri.endswith(".md"):
            yield item
        elif hasattr(item, "children"):
            yield from _iter_pages(item.children)


def _heading_from_source(path: Path) -> str | None:
    try:
        markdown = path.read_text(encoding="utf-8")
    except OSError:
        return None

    match = HEADING_RE.search(markdown)
    return match.group("heading").strip() if match else None


def _heading_from_markdown(markdown: str) -> str | None:
    match = HEADING_RE.search(markdown)
    return match.group("heading").strip() if match else None


def _display_title(heading: str) -> str:
    match = TITLE_ID_PREFIX_RE.match(heading)
    return match.group(1).strip() if match else heading


def _parse_metadata(comment: str, markdown: str, src_uri: str) -> dict[str, str] | None:
    fields = {m.group("key").lower(): m.group("value") for m in FIELD_RE.finditer(comment)}
    document = fields.get("document") or _document_id_from_heading(markdown) or _document_id_from_path(src_uri)
    status = fields.get("status")
    version = fields.get("version")

    if not document or not status:
        return None

    is_specification = ID_RE.fullmatch(document) is not None

    return {
        "document": document.upper() if is_specification else document,
        "document_label": "Document ID" if is_specification else "Document",
        "status": status,
        "version": version or "",
    }


def _document_id_from_heading(markdown: str) -> str | None:
    heading = HEADING_RE.search(markdown)
    if not heading:
        return None

    match = ID_RE.search(heading.group("heading"))
    return match.group("id") if match else None


def _document_id_from_path(src_uri: str) -> str | None:
    for part in PurePosixPath(src_uri).parts:
        match = ID_RE.search(part)
        if match:
            return match.group("id")

    return None


def _specification_from_path(src_uri: str) -> tuple[str, str] | None:
    for part in PurePosixPath(src_uri).parts:
        match = SPECIFICATION_FOLDER_RE.fullmatch(part)
        if match:
            return match.group("id").upper(), part

    return None


def _pdf_name(folder: str) -> str:
    family, number, title = folder.split("-", 2)
    return f"{family.upper()}-{number}-{title}.pdf"
