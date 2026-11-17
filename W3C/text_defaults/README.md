# Text baselines by script

Working data for WCAG 3 provisions on text appearance. For each script group in the W3C i18n [language matrix](https://www.w3.org/International/typography/gap-analysis/language-matrix.html), it records the typographic conventions that language communities use for 12 characteristics:

- font face / weight
- font size
- contrast
- letter aspect ratio
- text decoration
- letter spacing
- capitalization
- end-of-line hyphenation
- line spacing
- paragraph spacing
- line length
- padding (text containers)

Scope of this version:

- It records community conventions and published defaults only.
- Disability-related needs are not included yet.
- Every cell cites the section of the source it paraphrases.
- Cells with no source say "No data".

## Files

| Path | Contents |
|---|---|
| `index.html` | The page. It contains the matrix, the exceptions by language, the contrast findings, the WCAG 2 comparison values, details per script, coverage gaps, the method, and the sources. It is static HTML with no dependencies, and GitHub Pages can serve it as-is. |
| `data/dataset.json` | The full dataset: characteristics, status definitions, scripts, cells, exceptions, and sources. |
| `data/baselines.csv` | One row per script × characteristic, for spreadsheet use. |
| `data/matrix-languages.json` | Language list and selected gap scores extracted from the language matrix data file. |
| `src/dataset.py` | The source of truth for cell content. Edit this file. |
| `src/sources.py` | The source registry with URLs. |
| `src/build.py` | Regenerates `index.html` and `data/`. |

## Rebuild

```
python3 src/build.py
```

## Cell status

| Status | Meaning |
|---|---|
| Value | A source states a default value or range. |
| Convention | A source describes a convention without a number. |
| Not used | A source states the characteristic is not used or not applicable. |
| No data | No ingested source says anything usable. |

## Sources ingested

- W3C layout requirements documents:
  - JLReq, CLReq, KLReq, ALReq
  - ELReq and the Ethiopic style guide
  - MLReq, HLReq, ILReq
  - Indic and South-East Asian drafts
- Gap-analysis checklists in `w3c/typography`.
- Richard Ishida's orthography notes (`r12a/scripts`) for each matrix language that has a page.
- CSS Text Module Level 3.
- WCAG 2.2 and the Understanding documents for SC 1.4.3, 1.4.8 and 1.4.12.

The per-language gap-analysis issue threads on GitHub have not been ingested yet.
