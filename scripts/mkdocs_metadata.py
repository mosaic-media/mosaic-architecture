"""MkDocs hook for rendering preserved specification metadata."""

from __future__ import annotations

import re
from pathlib import Path
from pathlib import PurePosixPath


COMMENT_RE = re.compile(r"\A<!--\n(?P<body>.*?)\n-->\n?", re.DOTALL)
FIELD_RE = re.compile(r"^(?P<key>Document|Specification|Status|Version):\s*(?P<value>.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#\s+(?P<heading>.+)$", re.MULTILINE)
ID_RE = re.compile(r"\b(?P<id>(?:MAC|MDP|MEG|MIP|MOP|MDL|MDS)-\d{3})\b", re.IGNORECASE)
TITLE_ID_PREFIX_RE = re.compile(r"^(?:MAC|MDP|MEG|MIP|MOP|MDL|MDS)-\d{3}\s+[—-]\s+(.+)$", re.IGNORECASE)
OWNER_ROW_RE = re.compile(r"^\|\s*Owner\s*\|.*\|\s*$\n?", re.MULTILINE)
REVIEW_STATUS_RE = re.compile(r"\n---\n\n# Review Status\b.*\Z", re.DOTALL)


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
    markdown = _remove_boilerplate(markdown)
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
        f"    | Document ID | {metadata['document_id']} |",
        f"    | Status | {metadata['status']} |",
        f"    | Version | {metadata['version']} |",
        "",
    ]

    return markdown[: match.end()] + "\n".join(table) + "\n" + markdown[match.end() :]


def _remove_boilerplate(markdown: str) -> str:
    markdown = OWNER_ROW_RE.sub("", markdown)
    return REVIEW_STATUS_RE.sub("", markdown)


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
    document_id = fields.get("document") or fields.get("specification") or _document_id_from_heading(markdown) or _document_id_from_path(src_uri)
    status = fields.get("status")
    version = fields.get("version")

    if not document_id or not status or not version:
        return None

    return {
        "document_id": document_id.upper(),
        "status": status,
        "version": version,
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
