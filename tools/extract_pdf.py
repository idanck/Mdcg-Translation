#!/usr/bin/env python3
"""Extract text and tables from a MDCG source PDF into a working text file.

The output is a translator aid only (it is git-ignored): it gives the human/AI
translator the raw English text to build the canonical ``<ID>.he.json`` from.

Usage:
    python3 tools/extract_pdf.py MDCG-2019-8-v2
    python3 tools/extract_pdf.py MDCG-2019-8-v2 --stdout

The PDF is located automatically inside ``documents/<ID>/original/``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS = ROOT / "documents"


def find_pdf(doc_id: str) -> Path:
    original = DOCUMENTS / doc_id / "original"
    if not original.is_dir():
        sys.exit(f"error: no such document folder: {original}")
    pdfs = sorted(original.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"error: no PDF found in {original}")
    if len(pdfs) > 1:
        print(f"warning: multiple PDFs in {original}, using {pdfs[0].name}", file=sys.stderr)
    return pdfs[0]


def extract(pdf_path: Path) -> str:
    out: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            out.append(f"\n########## PAGE {i} ##########")
            out.append(page.extract_text() or "")
            for ti, table in enumerate(page.extract_tables(), start=1):
                out.append(f"\n--- TABLE {ti} (page {i}) ---")
                for row in table:
                    out.append(" | ".join((c or "").replace("\n", " ") for c in row))
    return "\n".join(out).strip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc_id", help="MDCG document id, e.g. MDCG-2019-8-v2")
    ap.add_argument("--stdout", action="store_true", help="print to stdout instead of writing a file")
    args = ap.parse_args()

    pdf_path = find_pdf(args.doc_id)
    text = extract(pdf_path)

    if args.stdout:
        sys.stdout.write(text)
        return

    out_path = DOCUMENTS / args.doc_id / "original" / f"{args.doc_id}.extracted.txt"
    out_path.write_text(text, encoding="utf-8")
    print(f"wrote {out_path} ({len(text)} chars from {pdf_path.name})")


if __name__ == "__main__":
    main()
