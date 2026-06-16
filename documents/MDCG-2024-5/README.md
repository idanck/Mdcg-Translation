# MDCG-2024-5

**Title:** Guidance on the Investigator's Brochure content  
**Category:** Clinical Investigation and Evaluation  
**Publication date:** April 2024  
**Source:** [https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en)

---

## Status

| Item | Status |
|------|--------|
| Original (EN) | ✅ `original/mdcg_2024-5_en.pdf` |
| Hebrew translation | 🔍 Under review (full translation done) |

---

## Files

| File | Description |
|------|-------------|
| `original/mdcg_2024-5_en.pdf` | Original English document (PDF) |
| `translation/MDCG-2024-5.he.json` | Canonical bilingual translation (source of truth) |
| `translation/MDCG-2024-5.he.html` | Hebrew RTL rendering, generated from the JSON |

---

## Notes

- Full bilingual translation of MDCG 2024-5 (34-page source PDF): cover disclaimer, Abbreviations
  table, sections 1–2.8 (all IB content sub-sections), and Appendix A (cross-reference checklist
  table). Every paragraph, list, table and footnote is translated; numbering preserved.
- Acronyms and regulatory references kept as-is (MDR, "Regulation (EU) 2017/745", Article/Annex
  numbers, IB, CIP, ISO 14155, GSPR, etc.). New domain terms are glossed inline as
  `Hebrew (EN: Term)` on first use.
- The anticipated SAE/SADE table (section 2.5.1) is an empty template in the source; its header
  row is rendered, with blank data rows omitted.
- To regenerate the HTML after editing the JSON: `python3 tools/render_html.py MDCG-2024-5`
- To validate the JSON against the schema: `python3 tools/validate.py MDCG-2024-5`
