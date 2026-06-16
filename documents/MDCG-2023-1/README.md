# MDCG-2023-1

**Title:** Guidance on the health institution exemption under Article 5(5) of Regulation (EU) 2017/745 and Regulation (EU) 2017/746  
**Category:** In-House Devices  
**Publication date:** January 2023  
**Source:** [https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en)

---

## Status

| Item | Status |
|------|--------|
| Original (EN) | ✅ `original/mdcg_2023-1_en.pdf` |
| Hebrew translation | 🔍 Under review (full translation done) |

---

## Files

| File | Description |
|------|-------------|
| `original/mdcg_2023-1_en.pdf` | Original English document (PDF) |
| `translation/MDCG-2023-1.he.json` | Canonical bilingual translation (source of truth) |
| `translation/MDCG-2023-1.he.html` | Hebrew RTL rendering, generated from the JSON |

---

## Notes

- Full translation of Sections 1–3 (3.1–3.11), Annex A and Annex B.
- Annex A public declaration is a *template*: the declaration field labels and the in-house
  device table headers are translated, while the form's blank placeholders are kept as fill-in
  fields. Footnotes (hospital note, risk-class note) are rendered as note blocks.
- Glossary terms applied (e.g. Health Institution → מוסד בריאות, GSPR → דרישות כלליות לבטיחות וביצועים).
  New term introduced: In-house device → מכשיר מתוצרת עצמית.
- To regenerate the HTML after editing the JSON:
  `python3 tools/render_html.py MDCG-2023-1`
- To validate the JSON against the schema: `python3 tools/validate.py MDCG-2023-1`
