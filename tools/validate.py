#!/usr/bin/env python3
"""Validate a document's canonical translation JSON against the schema.

Usage:
    python3 tools/validate.py MDCG-2019-8-v2     # validate one document
    python3 tools/validate.py --all              # validate every *.he.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS = ROOT / "documents"
SCHEMA_PATH = ROOT / "schema" / "mdcg-translation.schema.json"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def json_path(doc_id: str) -> Path:
    return DOCUMENTS / doc_id / "translation" / f"{doc_id}.he.json"


def validate_file(path: Path, schema: dict) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    msgs = []
    for e in errors:
        loc = "/".join(str(p) for p in e.path) or "<root>"
        msgs.append(f"  [{loc}] {e.message}")
    # Extra check: block ids must be unique within a document.
    ids = [b.get("id") for b in data.get("blocks", [])]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        msgs.append(f"  duplicate block ids: {sorted(dupes)}")
    return msgs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc_id", nargs="?", help="MDCG document id")
    ap.add_argument("--all", action="store_true", help="validate every *.he.json")
    args = ap.parse_args()

    schema = load_schema()
    if args.all:
        targets = sorted(DOCUMENTS.glob("*/translation/*.he.json"))
    elif args.doc_id:
        targets = [json_path(args.doc_id)]
    else:
        ap.error("provide a doc_id or --all")

    failed = False
    for path in targets:
        if not path.exists():
            print(f"MISSING {path}")
            failed = True
            continue
        msgs = validate_file(path, schema)
        if msgs:
            failed = True
            print(f"FAIL {path.name}")
            print("\n".join(msgs))
        else:
            print(f"OK   {path.name}")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
