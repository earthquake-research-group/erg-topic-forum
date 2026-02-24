#!/usr/bin/env python3
"""Scaffold a new session directory from a GitHub issue body.

Usage:
    Set environment variables, then run:
        ISSUE_BODY="..." ISSUE_TITLE="..." ISSUE_NUMBER="42" \\
            python scripts/create_session_from_issue.py

    Writes the session slug to .session_slug in the repo root
    so the calling workflow can reference it.
"""

import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = REPO_ROOT / "templates" / "session"
SESSIONS_DIR = REPO_ROOT / "sessions"


def parse_issue_body(body: str) -> dict:
    """Parse a GitHub issue form body into {field_label: value}."""
    fields = {}
    # Split on lines that start a new ### section
    sections = re.split(r"(?m)^### ", body)
    for section in sections:
        if not section.strip():
            continue
        parts = section.split("\n", 1)
        label = parts[0].strip()
        value = parts[1].strip() if len(parts) > 1 else ""
        # GitHub renders empty optional fields as "_No response_"
        # Textarea fields with render: text wrap content in ```text ... ``` blocks
        if value in ("_No response_", ""):
            value = ""
        elif re.match(r"^```\w*\s*```$", value, re.DOTALL):
            value = ""
        else:
            # Strip code block wrapper from textarea fields that have content
            value = re.sub(r"^```\w*\n?(.*?)```$", r"\1", value, flags=re.DOTALL).strip()
        fields[label] = value
    return fields


def make_slug(presenter: str, title: str) -> str:
    """Generate a session slug from presenter last name and title."""

    def slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_]+", "-", text)
        return text.strip("-")

    lastname = slugify(presenter.split()[-1]) if presenter else "session"
    title_slug = slugify(title)[:45]
    return f"{lastname}_{title_slug}"


def main():
    issue_body = os.environ.get("ISSUE_BODY", "")
    issue_title = os.environ.get("ISSUE_TITLE", "")
    issue_number = os.environ.get("ISSUE_NUMBER", "?")

    if not issue_body:
        print("ERROR: ISSUE_BODY is empty.", file=sys.stderr)
        sys.exit(1)

    print(f"Scaffolding session from issue #{issue_number}")
    fields = parse_issue_body(issue_body)

    # Extract fields using the exact label text from propose-session.yml
    title = fields.get("Session title", "").strip() or issue_title.removeprefix("[Session]").strip()
    presenter = fields.get("Presenter", "").strip()
    session_type = fields.get("Session type", "paper-discussion").strip()
    session_date = fields.get("Session date (YYYY-MM-DD)", "").strip()
    abstract = fields.get("Abstract (paste text)", "").strip()
    bibtex = fields.get("BibTeX (optional)", "").strip()
    doi = fields.get("DOI (optional)", "").strip()
    notes = fields.get("Notes (optional)", "").strip()

    missing = [f for f, v in [("title", title), ("presenter", presenter), ("date", session_date)] if not v]
    if missing:
        print(f"ERROR: Missing required fields: {', '.join(missing)}", file=sys.stderr)
        print("Parsed fields:", fields, file=sys.stderr)
        sys.exit(1)

    slug = make_slug(presenter, title)
    target_dir = SESSIONS_DIR / slug

    if target_dir.exists():
        print(f"ERROR: Session directory already exists: sessions/{slug}/", file=sys.stderr)
        sys.exit(1)

    print(f"  Slug:     {slug}")
    print(f"  Title:    {title}")
    print(f"  Author:   {presenter}")
    print(f"  Date:     {session_date}")
    print(f"  Type:     {session_type}")

    # Copy template directory
    shutil.copytree(TEMPLATE_DIR, target_dir)

    # Build substitution values
    categories = f"[{session_type}]"
    abstract_text = abstract if abstract else "_Paste the paper abstract here._"

    # Fill QMD template tokens
    qmd_path = target_dir / "index.qmd"
    qmd = qmd_path.read_text()
    qmd = qmd.replace("{{TITLE}}", title)
    qmd = qmd.replace("{{AUTHOR}}", presenter)
    qmd = qmd.replace("{{DATE}}", session_date)
    qmd = qmd.replace("{{CATEGORIES}}", categories)
    qmd = qmd.replace("{{ABSTRACT}}", abstract_text)
    qmd_path.write_text(qmd)

    # Write BibTeX (empty file is fine — Quarto handles it gracefully)
    bib_path = target_dir / "paper.bib"
    bib_path.write_text(bibtex + "\n" if bibtex else "")

    # Ensure assets/ directory exists (copytree won't copy empty dirs)
    (target_dir / "assets").mkdir(exist_ok=True)

    print(f"Session scaffolded: sessions/{slug}/")

    # Write slug to file so GH Actions step output can read it
    (REPO_ROOT / ".session_slug").write_text(slug)


if __name__ == "__main__":
    main()
