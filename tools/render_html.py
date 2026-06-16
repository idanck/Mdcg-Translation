#!/usr/bin/env python3
"""Render a canonical translation JSON into a Hebrew (RTL) HTML page.

The JSON (``documents/<ID>/translation/<ID>.he.json``) is the single source of
truth; the HTML is always regenerated from it and should never be edited by hand.

The page shows the Hebrew translation as primary content and offers a CSS-only
toggle to reveal the English source alongside each block (useful for fidelity
review and bilingual display on the website).

Usage:
    python3 tools/render_html.py MDCG-2019-8-v2
    python3 tools/render_html.py --all
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS = ROOT / "documents"

CSS = """
:root { --fg:#1a1a1a; --muted:#666; --line:#d8d8d8; --accent:#0b5fa5; --en-bg:#f5f7fa; }
* { box-sizing: border-box; }
body { margin:0; font-family: "Segoe UI", "Arial Hebrew", Arial, sans-serif; color:var(--fg);
       line-height:1.7; background:#fff; }
.wrap { max-width: 820px; margin: 0 auto; padding: 2rem 1.25rem 5rem; }
header.doc { border-bottom:2px solid var(--accent); padding-bottom:1rem; margin-bottom:1.5rem; }
header.doc .id { color:var(--accent); font-weight:700; letter-spacing:.04em; }
header.doc h1 { font-size:1.6rem; margin:.4rem 0; }
header.doc .meta { color:var(--muted); font-size:.9rem; }
header.doc .meta a { color:var(--accent); }
.toolbar { margin:1rem 0 2rem; font-size:.9rem; }
.toolbar label { cursor:pointer; user-select:none; }
h2 { font-size:1.3rem; margin-top:2.2rem; border-bottom:1px solid var(--line); padding-bottom:.3rem; }
h3 { font-size:1.12rem; margin-top:1.6rem; }
h4 { font-size:1rem; margin-top:1.2rem; }
.num { color:var(--accent); margin-inline-end:.4rem; }
p { margin:.7rem 0; }
ul, ol { margin:.6rem 0; padding-inline-start:1.6rem; }
li { margin:.3rem 0; }
table { border-collapse:collapse; width:100%; margin:1rem 0; }
th, td { border:1px solid var(--line); padding:.5rem .7rem; text-align:start; vertical-align:top; }
th { background:var(--en-bg); }
.note { font-size:.85rem; color:var(--muted); border-inline-start:3px solid var(--line);
        padding:.2rem .8rem; margin:.6rem 0; }
.note .marker { font-weight:700; color:var(--accent); }
.example { background:var(--en-bg); border:1px solid var(--line); border-radius:6px;
           padding:.8rem 1rem; margin:1rem 0; }
.example .caption { font-weight:600; margin-bottom:.5rem; }
.example pre { white-space:pre-wrap; font-family:inherit; direction:ltr; text-align:left;
               margin:0; color:#333; font-size:.9rem; }
/* English source: hidden by default, revealed via the toggle checkbox. */
.en { display:none; direction:ltr; text-align:left; background:var(--en-bg);
      border-inline-start:3px solid var(--accent); padding:.3rem .7rem; margin:.3rem 0 .9rem;
      font-size:.88rem; color:#333; border-radius:0 4px 4px 0; }
#show-en:checked ~ .content .en { display:block; }
#show-en { margin-inline-end:.4rem; }
footer.doc { margin-top:3rem; padding-top:1rem; border-top:1px solid var(--line);
             color:var(--muted); font-size:.8rem; }
"""


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def en_aside(text: str) -> str:
    if not text:
        return ""
    return f'<div class="en" lang="en">{esc(text)}</div>'


def render_block(b: dict) -> str:
    t = b.get("type")
    bid = esc(b.get("id", ""))
    if t == "heading":
        lvl = min(max(int(b.get("level", 2)) + 1, 2), 4)  # doc h1 is the title; sections start at h2
        num = b.get("number")
        num_html = f'<span class="num">{esc(num)}</span>' if num else ""
        return (f'<h{lvl} id="{bid}">{num_html}{esc(b.get("he",""))}</h{lvl}>'
                f'{en_aside(b.get("en",""))}')
    if t == "paragraph":
        return f'<p id="{bid}">{esc(b.get("he",""))}</p>{en_aside(b.get("en",""))}'
    if t == "list":
        tag = "ol" if b.get("ordered") else "ul"
        items = "".join(
            f'<li>{esc(it.get("he",""))}{en_aside(it.get("en",""))}</li>'
            for it in b.get("items", [])
        )
        return f'<{tag} id="{bid}">{items}</{tag}>'
    if t == "table":
        header = b.get("header")
        rows_html = []
        for ri, row in enumerate(b.get("rows", [])):
            cell_tag = "th" if (header and ri == 0) else "td"
            cells = "".join(
                f'<{cell_tag}>{esc(c.get("he",""))}{en_aside(c.get("en",""))}</{cell_tag}>'
                for c in row
            )
            rows_html.append(f"<tr>{cells}</tr>")
        return f'<table id="{bid}">{"".join(rows_html)}</table>'
    if t == "note":
        marker = b.get("marker")
        m_html = f'<span class="marker">{esc(marker)}</span> ' if marker else ""
        return (f'<div class="note" id="{bid}">{m_html}{esc(b.get("he",""))}'
                f'{en_aside(b.get("en",""))}</div>')
    if t == "example":
        cap = b.get("caption", {})
        return (f'<div class="example" id="{bid}">'
                f'<div class="caption">{esc(cap.get("he",""))}</div>'
                f'<pre>{esc(b.get("verbatim",""))}</pre>'
                f'{en_aside(cap.get("en",""))}</div>')
    return ""


def render(doc: dict) -> str:
    title = doc.get("title", {})
    src = doc.get("source", {})
    src_link = ""
    if src.get("url"):
        src_link = f' · <a href="{esc(src["url"])}" rel="noreferrer">מקור (EN)</a>'
    blocks_html = "\n".join(render_block(b) for b in doc.get("blocks", []))
    meta_bits = []
    if doc.get("category"):
        meta_bits.append(esc(doc["category"]))
    if doc.get("publicationDate"):
        meta_bits.append(esc(doc["publicationDate"]))
    meta = " · ".join(meta_bits)
    return f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title.get("he",""))} — {esc(doc.get("id",""))}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="doc">
  <div class="id">{esc(doc.get("id",""))}</div>
  <h1>{esc(title.get("he",""))}</h1>
  <div class="meta">{meta}{src_link}</div>
  <div class="meta" lang="en" dir="ltr" style="margin-top:.3rem">{esc(title.get("en",""))}</div>
</header>
<input type="checkbox" id="show-en">
<div class="toolbar"><label for="show-en">הצג טקסט מקור באנגלית לצד התרגום</label></div>
<main class="content">
{blocks_html}
</main>
<footer class="doc">
  תרגום לא רשמי לעברית · נוצר אוטומטית מקובץ ה-JSON הקנוני ({esc(doc.get("id",""))}.he.json).
  לתרגום אין מעמד משפטי; הנוסח המחייב הוא מסמך המקור באנגלית.
</footer>
</div>
</body>
</html>
"""


def render_one(doc_id: str) -> Path:
    json_path = DOCUMENTS / doc_id / "translation" / f"{doc_id}.he.json"
    if not json_path.exists():
        sys.exit(f"error: {json_path} not found")
    doc = json.loads(json_path.read_text(encoding="utf-8"))
    out_path = json_path.with_name(f"{doc_id}.he.html")
    out_path.write_text(render(doc), encoding="utf-8")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc_id", nargs="?", help="MDCG document id")
    ap.add_argument("--all", action="store_true", help="render every *.he.json")
    args = ap.parse_args()

    if args.all:
        ids = sorted(p.parent.parent.name for p in DOCUMENTS.glob("*/translation/*.he.json"))
    elif args.doc_id:
        ids = [args.doc_id]
    else:
        ap.error("provide a doc_id or --all")

    for doc_id in ids:
        out = render_one(doc_id)
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
