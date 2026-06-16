# MDCG-2019-8-v2

**Title:** Guidance document implant card on the application of Article 18 Regulation (EU) 2017/745  
**Category:** Implant Cards  
**Publication date:** March 2020  
**Source:** [https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en)

---

## Status

| Item | Status |
|------|--------|
| Original (EN) | ✅ `original/mdcg_2019-8_en.pdf` |
| Hebrew translation | 🔍 Under review (full translation done) |

---

## Files

| File | Description |
|------|-------------|
| `original/mdcg_2019-8_en.pdf` | Original English document (PDF) |
| `translation/MDCG-2019-8-v2.he.json` | Canonical bilingual translation (source of truth) |
| `translation/MDCG-2019-8-v2.he.html` | Hebrew RTL rendering, generated from the JSON |

---

## Notes

- Pilot document for the translation format (canonical JSON + generated RTL HTML).
- Sections 1–8 fully translated. Annex I examples are *illustrative*: sample card data
  (names, addresses, UDI/serial numbers) is preserved verbatim and not translated, in line
  with the source's General Note and footnote 9. The multilingual symbol table on the back of
  the card (EU-language equivalents, machine-translated per footnote 9) is summarised rather
  than reproduced per-language.
- To regenerate the HTML after editing the JSON:
  `python3 tools/render_html.py MDCG-2019-8-v2`
- To validate the JSON against the schema: `python3 tools/validate.py MDCG-2019-8-v2`
