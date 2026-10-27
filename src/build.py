"""Build data/*.json, data/baselines.csv and index.html from src/dataset.py.

Usage:  python3 src/build.py
No third-party dependencies.
"""
import csv
import datetime
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from dataset import CHARACTERISTICS, SCRIPTS, CONTRAST_NOTES, WCAG2_REFERENCE  # noqa: E402
from sources import SOURCES  # noqa: E402

MATRIX = json.load(open(os.path.join(HERE, "matrix_languages.json"), encoding="utf8"))
MATRIX_CODE = {  # dataset code -> matrix script names
    "Adlm": ["Adlam"], "Arab": ["Arab"], "Beng": ["Beng"], "Cans": ["Cans"], "Cher": ["Cher"],
    "Cyrl": ["Cyrl"], "Deva": ["Deva"], "Ethi": ["Ethi"], "Geor": ["Geor"], "Grek": ["Grek"],
    "Gujr": ["Gujr"], "Guru": ["Guru"], "Hang/Kore": ["Hang", "Kore"], "Hani": ["Hani"], "Hebr": ["Hebr"],
    "Java": ["Java"], "Jpan": ["Japn"], "Khmr": ["Khmr"], "Knda": ["Knda"], "Laoo": ["Laoo"],
    "Latn": ["Latn"], "Mlym": ["Mlym"], "Mong": ["Mong"], "Mymr": ["Mymr"], "Nkoo": ["N’Ko"],
    "Orya": ["Orya"], "Osge": ["Osage"], "Sinh": ["Sinh"], "Sund": ["Sund"], "Taml": ["Taml"],
    "Telu": ["Telu"], "Thai": ["Thai"], "Tibt": ["Tibt"],
}
# language-specific sources (language name as it appears in the matrix)
LANG_SOURCES = {
    ("Adlam", "Fula"): ["n:adlm/fuf"],
    ("Arab", "Arabic"): ["n:arab/arb", "alreq"], ("Arab", "Persian"): ["n:arab/pes", "alreq"],
    ("Arab", "Urdu"): ["n:arab/ur"], ("Arab", "Pashto"): ["n:arab/ps"], ("Arab", "Sindhi"): ["n:arab/sd"],
    ("Arab", "Kurdish"): ["n:arab/ckb"], ("Arab", "Saraiki"): ["n:arab/skr"], ("Arab", "Kashmiri"): ["n:arab/ks"],
    ("Arab", "Uighur"): ["n:arab/ug"], ("Beng", "Bangla"): ["n:beng/bn"],
    ("Cans", "Inuktitut"): ["n:cans/ike"], ("Cans", "Plains Cree"): ["n:cans/crk"], ("Cher", "Cherokee"): ["n:cher/chr"],
    ("Cyrl", "Russian"): ["n:cyrl/ru"], ("Cyrl", "Ukrainian"): ["n:cyrl/uk"], ("Deva", "Hindi"): ["n:deva/hi", "ilreq"],
    ("Ethi", "Amharic"): ["n:ethi/am", "elreq"], ("Geor", "Georgian"): ["n:geor/ka"], ("Grek", "Greek"): ["n:grek/el"],
    ("Gujr", "Gujarati"): ["n:gujr/gu"], ("Guru", "Panjabi"): ["n:guru/pa"], ("Hang", "Korean"): ["n:kore/ko", "klreq"],
    ("Kore", "Korean"): ["n:kore/ko", "klreq"], ("Hani", "SChinese"): ["n:hani/zh", "clreq"], ("Hani", "TChinese"): ["n:hani/zh", "clreq"],
    ("Hebr", "Hebrew"): ["n:hebr/he", "hlreq"], ("Java", "Javanese"): ["n:java/jv"], ("Japn", "Japanese"): ["n:jpan/ja", "jlreq"],
    ("Khmr", "Khmer"): ["n:khmr/km"], ("Laoo", "Lao"): ["n:laoo/lo"], ("Latn", "Fula"): ["n:latn/ff"],
    ("Latn", "Hausa"): ["n:latn/ha"], ("Latn", "Kurdish"): ["n:latn/kmr"], ("Latn", "Dutch"): ["nl-checklist", "css-text-3"],
    ("Latn", "Hungarian"): ["css-text-3"], ("Latn", "Turkish"): ["css-text-3"], ("Latn", "English"): ["css-text-3"],
    ("Mlym", "Malayalam"): ["n:mlym/ml"], ("Mong", "Mongolian"): ["n:mong/mn", "mlreq"], ("Mymr", "Burmese"): ["n:mymr/my"],
    ("Mymr", "Shan"): ["n:mymr/shn"], ("N’Ko", "N’Ko"): ["n:nkoo/nqo"], ("Orya", "Odia"): ["n:orya/or"],
    ("Osage", "Osage"): ["n:osge/osa"], ("Sinh", "Sinhalese"): ["n:sinh/si"], ("Sund", "Sundanese"): ["n:sund/su"],
    ("Taml", "Tamil"): ["n:taml/ta"], ("Telu", "Telugu"): ["n:telu/te"], ("Thai", "Thai"): ["n:thai/th"],
    ("Tibt", "Tibetan"): ["n:tibt/bo"],
}
MATRIX_COLS = [("fonts", "Fonts"), ("transforms", "Transforms"), ("text_decoration", "Text decoration"),
               ("spacing", "Text spacing"), ("line_breaking", "Line breaking"), ("baselines", "Baselines")]
MATRIX_VAL = {"3": "3 OK", "2": "2 Advanced", "1": "1 Basic", "0": "0 Broken", "-": "– n/a or OK", "": "? Unknown"}

STATUS = {
    "numeric": ("Value", "■", "A source states a default value or range."),
    "convention": ("Convention", "●", "A source describes a convention without a number."),
    "not-used": ("Not used", "✕", "A source says the characteristic is not used or not applicable."),
    "no-data": ("No data", "?", "No ingested source says anything usable."),
}

e = lambda s: html.escape(str(s), quote=True)
slug = lambda s: "".join(ch if ch.isalnum() else "-" for ch in s).strip("-").lower()


def src_link(key, anchor):
    s = SOURCES[key]
    url = s["url"] + (("#" + anchor) if anchor else "")
    label = s["title"] + ((" §" + anchor) if anchor else "")
    return f'<a href="{e(url)}">{e(label)}</a>'


def src_list(refs):
    if not refs:
        return ""
    items = "".join(f"<li>{src_link(k, a)}</li>" for k, a in refs)
    return f'<ul class="srcs">{items}</ul>'


def badge(status):
    label, sym, _ = STATUS[status]
    return f'<span class="badge b-{status}"><span aria-hidden="true">{sym}</span> {label}</span>'


# ------------------------------------------------------------------ data outputs
def write_data():
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    out = {
        "generated": datetime.date.today().isoformat(),
        "characteristics": [{"key": k, "label": l, "definition": d} for k, l, d in CHARACTERISTICS],
        "statuses": {k: {"label": v[0], "definition": v[2]} for k, v in STATUS.items()},
        "scripts": [{**s, "exceptions": [{"languages": x[0], "characteristic": x[1], "text": x[2],
                                           "sources": [{"key": k, "anchor": a} for k, a in x[3]]} for x in s["exceptions"]]}
                    for s in SCRIPTS],
        "contrast_notes": [{"text": n["text"], "sources": [{"key": k, "anchor": a} for k, a in n["sources"]]} for n in CONTRAST_NOTES],
        "wcag2_reference": [{"text": n["text"], "sources": [{"key": k, "anchor": a} for k, a in n["sources"]]} for n in WCAG2_REFERENCE],
        "sources": SOURCES,
    }
    json.dump(out, open(os.path.join(ROOT, "data", "dataset.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    json.dump(MATRIX, open(os.path.join(ROOT, "data", "matrix-languages.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "data", "baselines.csv"), "w", newline="", encoding="utf8") as f:
        w = csv.writer(f)
        w.writerow(["script_code", "script", "characteristic", "status", "summary", "details", "sources"])
        for s in SCRIPTS:
            for k, l, _ in CHARACTERISTICS:
                cell = s["cells"][k]
                w.writerow([s["code"], s["name"], l, cell["status"], cell["short"], " | ".join(cell["details"]),
                            " ; ".join(SOURCES[r["key"]]["url"] + ("#" + r["anchor"] if r["anchor"] else "") for r in cell["sources"])])


# ------------------------------------------------------------------ html
CSS = r"""
:root{--bg:#fbfbf9;--fg:#1b1b1a;--muted:#55554f;--line:#d6d5cf;--panel:#ffffff;--head:#f1f0ec;--link:#0b55a8;
--num-bg:#0f5132;--num-fg:#ffffff;--con-bg:#cfe8dc;--con-fg:#10372a;--not-bg:#e9e6f4;--not-fg:#352a63;--nd-bg:#f3f2ee;--nd-fg:#55554f;--focus:#c2410c}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#151514;--fg:#ecebe6;--muted:#b5b3ab;--line:#3a3935;--panel:#1d1d1b;--head:#262623;--link:#8cc2ff;
--num-bg:#7ad1a6;--num-fg:#06281a;--con-bg:#1f4536;--con-fg:#d4f0e2;--not-bg:#332c55;--not-fg:#e3defa;--nd-bg:#22221f;--nd-fg:#b5b3ab;--focus:#fb923c}}
:root[data-theme="dark"]{--bg:#151514;--fg:#ecebe6;--muted:#b5b3ab;--line:#3a3935;--panel:#1d1d1b;--head:#262623;--link:#8cc2ff;
--num-bg:#7ad1a6;--num-fg:#06281a;--con-bg:#1f4536;--con-fg:#d4f0e2;--not-bg:#332c55;--not-fg:#e3defa;--nd-bg:#22221f;--nd-fg:#b5b3ab;--focus:#fb923c}
*{box-sizing:border-box}
html{font-size:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:1rem/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif;overflow-wrap:break-word}
main,.script,dl.cells dt,dl.cells dd{min-width:0}
ul.srcs a,.plain td a{overflow-wrap:anywhere}
.wrap{overflow-x:auto}
a{color:var(--link)}
a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--focus);outline-offset:2px}
.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:var(--panel);padding:.5rem 1rem;z-index:10}
header,main,footer{max-width:78rem;margin:0 auto;padding:0 1rem}
header{padding-top:2rem}
h1{font-size:1.9rem;line-height:1.25;margin:.2rem 0 .6rem}
h2{font-size:1.4rem;margin:2.6rem 0 .6rem;padding-top:.6rem;border-top:1px solid var(--line)}
h3{font-size:1.15rem;margin:1.8rem 0 .4rem}
h4{font-size:1rem;margin:1.1rem 0 .2rem}
.lede{max-width:46rem;color:var(--muted)}
nav.toc ol{columns:2 16rem;padding-left:1.2rem}
.legend{display:flex;flex-wrap:wrap;gap:.5rem 1.2rem;padding:0;list-style:none}
.legend li{display:flex;gap:.5rem;align-items:baseline}
.badge{display:inline-block;padding:.05rem .45rem;border-radius:.3rem;font-size:.8rem;font-weight:600;white-space:nowrap}
.b-numeric{background:var(--num-bg);color:var(--num-fg)}
.b-convention{background:var(--con-bg);color:var(--con-fg)}
.b-not-used{background:var(--not-bg);color:var(--not-fg)}
.b-no-data{background:var(--nd-bg);color:var(--nd-fg);border:1px dashed var(--line)}
.controls{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin:.8rem 0}
.controls button{font:inherit;font-size:.9rem;padding:.35rem .8rem;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:.35rem;cursor:pointer}
.controls button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
.scroller{overflow:auto;max-height:80vh;border:1px solid var(--line);border-radius:.4rem;background:var(--panel)}
table{border-collapse:separate;border-spacing:0}
table.matrix{font-size:.82rem;line-height:1.35}
.matrix th,.matrix td{border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top;padding:.45rem .5rem;text-align:left}
.matrix thead th{position:sticky;top:0;background:var(--head);z-index:2;font-size:.8rem;min-width:9.5rem}
.matrix thead th:first-child{left:0;z-index:3;min-width:9rem}
.matrix tbody th{position:sticky;left:0;background:var(--head);z-index:1;font-weight:600;min-width:9rem}
.matrix tbody th small{display:block;font-weight:400;color:var(--muted)}
.matrix td a{color:inherit;text-decoration:none;display:block}
.matrix td a:hover .short{text-decoration:underline}
.matrix td .short{display:block;margin-top:.25rem}
.matrix td.s-no-data .short{color:var(--muted)}
.compact .matrix td .short{display:none}
.compact .matrix thead th{min-width:5.5rem}
table.plain{width:100%;font-size:.9rem;border:1px solid var(--line);border-radius:.4rem;background:var(--panel)}
.plain th,.plain td{border-bottom:1px solid var(--line);padding:.45rem .6rem;text-align:left;vertical-align:top}
.plain thead th{background:var(--head)}
.script{background:var(--panel);border:1px solid var(--line);border-radius:.5rem;padding:.2rem 1.1rem 1rem;margin:1.2rem 0}
.script h3{margin-top:.9rem}
dl.cells{display:grid;grid-template-columns:minmax(10rem,14rem) 1fr;gap:.2rem 1.2rem;margin:.6rem 0 0}
dl.cells dt{font-weight:600;padding-top:.6rem;border-top:1px solid var(--line)}
dl.cells dd{margin:0;padding-top:.6rem;border-top:1px solid var(--line)}
dl.cells dd ul{margin:.3rem 0;padding-left:1.1rem}
ul.srcs{font-size:.82rem;color:var(--muted);margin:.2rem 0 .4rem;padding-left:1.1rem}
ul.srcs li{margin:.1rem 0}
.note{border-left:4px solid var(--line);padding:.2rem .9rem;color:var(--muted)}
footer{color:var(--muted);font-size:.85rem;padding-bottom:3rem}
@media (max-width:40rem){dl.cells{grid-template-columns:1fr}dl.cells dd{border-top:0;padding-top:0}}
@media print{.controls,.skip,nav.toc{display:none}.scroller{max-height:none;overflow:visible}}
"""

JS = r"""
(function(){
  var btns=document.querySelectorAll('[data-view]');
  function set(v){document.body.classList.toggle('compact',v==='compact');
    btns.forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.view===v));});
    try{localStorage.setItem('tb-view',v);}catch(e){}}
  btns.forEach(function(b){b.addEventListener('click',function(){set(b.dataset.view);});});
  var saved=null;try{saved=localStorage.getItem('tb-view');}catch(e){}
  if(saved)set(saved);
  var sel=document.getElementById('status-filter');
  if(sel){sel.addEventListener('change',function(){var v=sel.value;
    document.querySelectorAll('.matrix td').forEach(function(td){
      td.style.opacity=(!v||td.classList.contains('s-'+v))?'':'0.25';});
    var live=document.getElementById('filter-live');
    var n=v?document.querySelectorAll('.matrix td.s-'+v).length:0;
    live.textContent=v?(n+' cells with status '+sel.options[sel.selectedIndex].text):'Showing all cells';});}
})();
"""


def build_html():
    today = datetime.date.today().isoformat()
    from collections import Counter
    counts = Counter(c["status"] for s in SCRIPTS for c in s["cells"].values())
    total = sum(counts.values())
    nlang = sum(len(sc["languages"]) for sc in MATRIX)
    P = []
    a = P.append
    a('<!doctype html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width, initial-scale=1">'
      '<title>Text Baselines by Script</title>'
      '<meta name="description" content="Script-level typographic conventions for 12 text characteristics across the languages in the W3C i18n language matrix, with sources.">'
      f'<style>{CSS}</style></head><body>')
    a('<a class="skip" href="#main">Skip to content</a>')
    a('<header><p class="lede" style="margin:0">WCAG 3 working data · COGA</p>'
      '<h1>Text baselines by script</h1>'
      f'<p class="lede">Typographic conventions of each language community, grouped by script, for 12 text characteristics. '
      f'Covers the {nlang} language rows ({len(MATRIX)} script groups) of the W3C i18n '
      f'<a href="{e(SOURCES["matrix"]["url"])}">language matrix</a>. Only conventions stated in a cited source are recorded. '
      f'Disability-related needs are not included yet. Built {today}.</p></header>')
    a('<main id="main">')
    a('<nav class="toc" aria-labelledby="toc-h"><h2 id="toc-h" style="border:0;margin-top:1rem">Contents</h2><ol>'
      '<li><a href="#matrix">Matrix: scripts × characteristics</a></li><li><a href="#exceptions">Exceptions by language</a></li>'
      '<li><a href="#contrast">Contrast</a></li><li><a href="#wcag2">WCAG 2 values for comparison</a></li>'
      '<li><a href="#scripts">Details by script</a></li><li><a href="#gaps">Coverage gaps</a></li>'
      '<li><a href="#method">Method and definitions</a></li><li><a href="#sources">Sources</a></li></ol></nav>')

    # matrix
    a('<h2 id="matrix">Matrix: scripts × characteristics</h2>')
    a('<ul class="legend" aria-label="Status key">' + "".join(
        f'<li>{badge(k)} <span>{e(v[2])}</span></li>' for k, v in STATUS.items()) + '</ul>')
    a('<p>' + ", ".join(f'{counts[k]} {STATUS[k][0].lower()}' for k in STATUS) + f' (of {total} cells).</p>')
    a('<div class="controls"><span id="view-l">View:</span>'
      '<button type="button" data-view="full" aria-pressed="true" aria-describedby="view-l">Summaries</button>'
      '<button type="button" data-view="compact" aria-pressed="false" aria-describedby="view-l">Status only</button>'
      '<label for="status-filter">Highlight status:</label><select id="status-filter"><option value="">All</option>'
      + "".join(f'<option value="{k}">{e(v[0])}</option>' for k, v in STATUS.items()) +
      '</select><span id="filter-live" class="lede" aria-live="polite"></span></div>')
    a('<div class="scroller" tabindex="0" role="region" aria-labelledby="matrix-cap"><table class="matrix">'
      '<caption id="matrix-cap" class="skip">Status and summary of each characteristic for each script. Each cell links to its details and sources.</caption><thead><tr><th scope="col">Script</th>')
    for k, l, d in CHARACTERISTICS:
        a(f'<th scope="col" title="{e(d)}">{e(l)}</th>')
    a('</tr></thead><tbody>')
    for s in SCRIPTS:
        sid = slug(s["code"])
        a(f'<tr><th scope="row"><a href="#s-{sid}">{e(s["name"])}</a><small>{e(s["code"])} · {len(s["languages"])} lang.</small></th>')
        for k, l, _ in CHARACTERISTICS:
            cell = s["cells"][k]
            a(f'<td class="s-{cell["status"]}"><a href="#s-{sid}-{k}">{badge(cell["status"])}'
              + ('' if cell["status"] == "no-data" else f'<span class="short">{e(cell["short"])}</span>') + '</a></td>')
        a('</tr>')
    a('</tbody></table></div>')

    # exceptions
    a('<h2 id="exceptions">Exceptions by language</h2>')
    a('<p>Places where a language departs from its script group, or where the script-level row does not apply to a language.</p>')
    a('<div class="wrap" tabindex="0" role="region" aria-label="Exceptions table"><table class="plain"><thead><tr><th scope="col">Script</th><th scope="col">Language(s)</th><th scope="col">Characteristic</th><th scope="col">Exception</th><th scope="col">Sources</th></tr></thead><tbody>')
    labels = {k: l for k, l, _ in CHARACTERISTICS}
    for s in SCRIPTS:
        for langs, ch, text, refs in s["exceptions"]:
            a(f'<tr><td>{e(s["name"])}</td><td>{e(langs)}</td><td>{e(labels.get(ch, "All"))}</td><td>{e(text)}</td><td>{src_list(refs) or "—"}</td></tr>')
    a('</tbody></table></div>')
    a('<h3>Differences between scripts that share a writing tradition</h3><ul>'
      '<li>Japanese vs. Chinese: side lines go to the right of vertical Japanese text and the left of vertical Chinese text; emphasis dots go above horizontal Japanese and below horizontal Chinese. ' +
      src_list([("n:jpan/ja", "text_decoration"), ("n:hani/zh", "text_decoration"), ("clreq", "id84")]) + '</li>'
      '<li>Korean vs. Chinese/Japanese: no automatic gap between Hangul and adjacent Latin text, because Latin may be followed by a Korean particle. ' +
      src_list([("n:kore/ko", "spacing")]) + '</li>'
      '<li>Adlam vs. N’Ko: italics lean right in Adlam and left in N’Ko, by community preference. ' +
      src_list([("n:nkoo/nqo", "fontstyle"), ("n:adlm/fuf", "fontstyle")]) + '</li></ul>')

    # contrast
    a('<h2 id="contrast">Contrast</h2>')
    a('<p>Every contrast cell in the matrix is “No data”. What the sources do say:</p><ul>')
    for n in CONTRAST_NOTES:
        a(f'<li>{e(n["text"])}{src_list(n["sources"])}</li>')
    a('</ul>')

    # wcag2
    a('<h2 id="wcag2">WCAG 2 values for comparison</h2>')
    a('<p class="note">Kept separate from the matrix: these are user-adjustment targets, not community defaults.</p><ul>')
    for n in WCAG2_REFERENCE:
        a(f'<li>{e(n["text"])}{src_list(n["sources"])}</li>')
    a('</ul>')

    # details
    a('<h2 id="scripts">Details by script</h2>')
    a('<p>Matrix scores are from the W3C language matrix (web-support gaps, not reader needs): 3 OK, 2 advanced work needed, 1 basic work needed, 0 broken, – n/a or OK, ? not yet investigated.</p>')
    for s in SCRIPTS:
        sid = slug(s["code"])
        a(f'<section class="script" id="s-{sid}" aria-labelledby="s-{sid}-h"><h3 id="s-{sid}-h">{e(s["name"])} <small>({e(s["code"])})</small></h3>')
        rows = []
        for mname in MATRIX_CODE[s["code"]]:
            for g in MATRIX:
                if g["script"] != mname:
                    continue
                for L in g["languages"]:
                    srcs = LANG_SOURCES.get((mname, L["lang"]), [])
                    rows.append((mname, L, srcs))
        a('<h4>Languages</h4><div class="scroller" style="max-height:none" tabindex="0" role="region" aria-label="Languages in ' + e(s["name"]) + '"><table class="plain"><thead><tr><th scope="col">Language</th><th scope="col">Language-specific sources</th>'
          + "".join(f'<th scope="col">Matrix: {e(lbl)}</th>' for _, lbl in MATRIX_COLS) + '</tr></thead><tbody>')
        for mname, L, srcs in rows:
            name = L["lang"] + (f' <small>({e(mname)})</small>' if len(MATRIX_CODE[s["code"]]) > 1 else "")
            tent = " *" if L.get("tentative") else ""
            srccell = ", ".join(f'<a href="{e(SOURCES[k]["url"])}">{e(SOURCES[k]["title"])}</a>' for k in srcs) or "None — script-level only"
            a(f'<tr><th scope="row">{name}{tent}</th><td>{srccell}</td>' +
              "".join(f'<td>{e(MATRIX_VAL.get(L.get(c, ""), L.get(c, "")))}</td>' for c, _ in MATRIX_COLS) + '</tr>')
        a('</tbody></table></div><p class="lede" style="font-size:.85rem">* tentative matrix scores.</p>')
        a('<h4>Characteristics</h4><dl class="cells">')
        for k, l, _ in CHARACTERISTICS:
            cell = s["cells"][k]
            det = "".join(f"<li>{e(x)}</li>" for x in cell["details"])
            a(f'<dt id="s-{sid}-{k}">{e(l)}</dt><dd>{badge(cell["status"])} <strong>{e(cell["short"])}</strong>'
              + (f"<ul>{det}</ul>" if det else "")
              + src_list([(r["key"], r["anchor"]) for r in cell["sources"]]) + '</dd>')
        a('</dl></section>')

    # gaps
    a('<h2 id="gaps">Coverage gaps</h2><ul>')
    nodata_cols = [(l, sum(1 for s in SCRIPTS if s["cells"][k]["status"] == "no-data")) for k, l, _ in CHARACTERISTICS]
    a('<li>No-data cells per characteristic: ' + "; ".join(f'{e(l)} {n}/{len(SCRIPTS)}' for l, n in nodata_cols) + '.</li>')
    missing = [f'{L["lang"]} ({g["script"]})' for g in MATRIX for L in g["languages"] if (g["script"], L["lang"]) not in LANG_SOURCES]
    a(f'<li>{len(missing)} of {nlang} matrix language rows have no language-specific source: {e(", ".join(missing))}.</li>')
    a('<li>Kannada has no orthography notes or requirements document in the ingested sources.</li>'
      '<li>No requirements document exists for Latin, Cyrillic, Greek, Georgian, or most Indic and South-East Asian scripts; those rows rely on orthography notes, which describe observed practice rather than standards.</li>'
      '<li>Numeric defaults exist only in the Japanese, Chinese, Korean, Ethiopic and Tibetan sources (plus JLReq’s statements about Western layout).</li>'
      '<li>Gap-analysis issues filed on GitHub (per-language requirements threads) were not ingested in this pass.</li></ul>')

    # method
    a('<h2 id="method">Method and definitions</h2><ol>'
      '<li>Language list and script grouping extracted from the language matrix data file in the w3c/typography repository.</li>'
      '<li>Sources ingested: the W3C layout-requirements documents (JLReq, CLReq, KLReq, ALReq, ELReq and style guide, MLReq, HLReq, ILReq, Indic and South-East Asian drafts), the gap-analysis checklists, R. Ishida’s orthography notes for each matrix language that has a page, CSS Text 3, and WCAG 2.2 with its Understanding documents.</li>'
      '<li>Sections matching each characteristic were extracted and read; each cell paraphrases what a source states and links to the section.</li>'
      '<li>“Letter aspect ratio” is mapped to the height of a script’s basic letters relative to Latin x-height and cap-height (as the orthography notes compare them), or to the letter face within the square character frame for Han/Kana.</li>'
      '<li>“Padding” is mapped to margins and text-area definitions, and to page-direction statements that reverse start/end padding.</li>'
      '<li>Whether a script has case is taken from the Unicode Character Database when no prose source covers it.</li>'
      '<li>Hangul and Kore matrix rows are combined; Han’s Simplified and Traditional rows are combined, with differences listed as exceptions.</li></ol>')
    a('<h3>Characteristic definitions used</h3><table class="plain"><thead><tr><th scope="col">Characteristic</th><th scope="col">What was looked for</th></tr></thead><tbody>'
      + "".join(f'<tr><th scope="row">{e(l)}</th><td>{e(d)}</td></tr>' for _, l, d in CHARACTERISTICS) + '</tbody></table>')

    # sources
    a('<h2 id="sources">Sources</h2><table class="plain"><thead><tr><th scope="col">Source</th><th scope="col">Type</th></tr></thead><tbody>')
    for k, s in SOURCES.items():
        a(f'<tr><td><a href="{e(s["url"])}">{e(s["title"])}</a></td><td>{e(s["kind"])}</td></tr>')
    a('</tbody></table>')
    a('</main><footer><p>Data: <a href="data/dataset.json">dataset.json</a> · <a href="data/baselines.csv">baselines.csv</a> · '
      '<a href="data/matrix-languages.json">matrix-languages.json</a>. Regenerate with <code>python3 src/build.py</code>.</p></footer>')
    a(f'<script>{JS}</script></body></html>')
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf8").write("".join(P))


if __name__ == "__main__":
    write_data()
    build_html()
    print("built index.html and data/")
