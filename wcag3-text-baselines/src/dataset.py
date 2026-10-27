"""Script-level baselines for 12 text characteristics.

Status codes:
  numeric     a source states a default value or range
  convention  a source describes a convention but gives no number
  not-used    a source states the characteristic is not used / not applicable for the script
  no-data     none of the ingested sources say anything usable

Rules followed when writing cells:
  * Only what an ingested source says. No inference from general knowledge.
  * "short" is the matrix label; "details" carries the paraphrased evidence.
  * Anchors point at the section of the source the statement comes from.
"""

CHARACTERISTICS = [
    ("font", "Font face / weight", "Typeface styles used for body text, and how bold/italic weights are used."),
    ("size", "Font size", "Body-text sizes and minimum sizes stated as defaults."),
    ("contrast", "Contrast", "Any script- or language-specific statement about text/background contrast."),
    ("aspect", "Letter aspect ratio", "Proportions of the letterforms. Mapped to the height of the script's basic letters relative to Latin x-height / cap-height, or to the letter face inside the character frame for CJK."),
    ("decoration", "Text decoration", "Underline, overline, side lines, strikethrough: placement, thickness, meaning."),
    ("letterspacing", "Letter spacing", "Default inter-character spacing and when tracking is used or prohibited."),
    ("caps", "Capitalization", "Whether the script has case, and any language-specific casing rules."),
    ("hyphen", "End-of-line hyphenation", "Whether words are broken at line end and how the break is marked."),
    ("linespacing", "Line spacing", "Default line gap / line height, or stated need for more vertical space than Latin."),
    ("paraspacing", "Paragraph spacing", "Space between paragraphs and the paragraph-marking method (indent vs. space)."),
    ("linelength", "Line length", "Default or maximum characters per line."),
    ("padding", "Padding (text containers)", "Margins/padding around text blocks, including direction of layout."),
]

def c(status, short, details=(), src=()):
    return {
        "status": status,
        "short": short,
        "details": list(details),
        "sources": [{"key": k, "anchor": a} for k, a in src],
    }

ND = lambda: c("no-data", "No data")
UNICAMERAL = lambda: c("not-used", "No case", ["The script has no case mappings in the Unicode Character Database 15.1."], [("ucd", "")])
NO_CONTRAST = ND  # contrast: no ingested source defines script-specific contrast

SCRIPTS = []

def script(code, name, languages, notes_files, cells, exceptions=()):
    for k, _, _ in CHARACTERISTICS:
        cells.setdefault(k, ND())
    SCRIPTS.append({
        "code": code,
        "name": name,
        "languages": languages,
        "notes_files": notes_files,
        "cells": cells,
        "exceptions": list(exceptions),
    })

# ---------------------------------------------------------------- Adlam
script("Adlm", "Adlam", ["Fula"], ["n:adlm/fuf"], {
    "font": c("convention", "Bold and italic used; italic leans right",
        ["Adlam texts use both bolding and italics.",
         "After community consultation the first drawn Adlam italic leans to the right (the opposite of N’Ko)."],
        [("n:adlm/fuf", "fontstyle"), ("n:nkoo/nqo", "fontstyle")]),
    "aspect": c("convention", "Basic letters ≈ Latin x-height; marks exceed Latin ascenders",
        ["Basic lowercase Adlam letters are typically around the Latin x-height (Noto Sans Adlam).",
         "Diacritics reach well beyond Latin ascenders; capitals increase height further."],
        [("n:adlm/fuf", "baselines")]),
    "caps": c("convention", "Bicameral",
        ["The notes refer to capital letters increasing vertical height; Unicode 15.1 has case mappings for Adlam."],
        [("n:adlm/fuf", "baselines"), ("ucd", "")]),
    "hyphen": c("convention", "Hyphenation used",
        ["Breaks occur primarily at spaces; in-word breaks with hyphenation also occur.",
         "Long words may be hyphenated to reduce added space in justified text."],
        [("n:adlm/fuf", "linebreak"), ("n:adlm/fuf", "justification")]),
    "letterspacing": c("convention", "Interword spacing for justification; baseline stretching is historical",
        ["Modern preference is interword spacing for justification; stretching the baseline with ـ was used in the past."],
        [("n:adlm/fuf", "justification")]),
    "linespacing": c("convention", "Larger than Latin",
        ["Vertical resolution needed for readable Fula text is higher than for English; diacritics create a need for larger line spacing."],
        [("n:adlm/fuf", "baselines")]),
    "padding": c("convention", "Right-to-left page progression",
        ["Books are bound on the right; pages progress right to left. Layout direction mirrors left-to-right layouts."],
        [("n:adlm/fuf", "generallayout")]),
})

# ---------------------------------------------------------------- Arabic
script("Arab", "Arabic", ["Arabic", "Urdu", "Persian", "Pashto", "Sindhi", "Kurdish", "Saraiki", "Kashmiri", "Uighur"],
       ["n:arab/arb", "n:arab/ur", "n:arab/pes", "n:arab/ps", "n:arab/sd", "n:arab/ckb", "n:arab/skr", "n:arab/ks", "n:arab/ug"], {
    "font": c("convention", "Naskh default; Nastaʻlīq for Persian (Iran) and Urdu (Pakistan)",
        ["Naskh has become the default form of Arabic in most contexts and is the model for most text typefaces.",
         "In Iran and Pakistan, Nastaʻlīq remains the preferred style for Persian and Urdu respectively.",
         "ALReq lists accessibility (readability and visibility) and small-screen legibility (larger loops and teeth, small descenders) as font-selection considerations.",
         "Italic/oblique Arabic may slant to the left."],
        [("alreq", "h_writing_style"), ("alreq", "h_writing_styles"), ("n:arab/arb", "letterforms")]),
    "aspect": c("convention", "Ascenders/descenders extend much further than Latin",
        ["Arabic ascenders and descenders extend much further than those of Latin.",
         "Uighur: the basic part of most letters is less than Latin x-height, but extenders and marks reach Latin ascender/descender lines."],
        [("alreq", "h_baselines"), ("n:arab/ug", "baselines")]),
    "decoration": c("convention", "Underline further from baseline than Latin; avoid short ink-skip fragments",
        ["Underlines and overlines sit further from the baseline than in Latin text, typically clearing long descenders and their diacritics.",
         "If lines skip ink, very short line remnants must be avoided because they can look like dots or diacritics.",
         "The Qur’an tends to use overlines rather than underlines.",
         "Text borders must not expose the joins between letters; styling one letter must not break its joining."],
        [("n:arab/arb", "otherinline"), ("alreq", "h_joining_and_text_border"), ("alreq", "h_styling_individual_letters")]),
    "letterspacing": c("not-used", "No letter spacing (cursive); stretching via kashida instead",
        ["Spaces are not added between characters except micro-spacing at non-joining letters during justification.",
         "Stretching for headings, signs, or emphasis is done by elongating the baseline, unevenly, and does not correspond to Latin letter-spacing.",
         "CSS Text 3 classes Arabic as a cursive script that does not admit gaps between letters; authors should avoid letter-spacing on cursive scripts."],
        [("n:arab/arb", "spacing"), ("alreq", "h_spacing"), ("css-text-3", "cursive-tracking")]),
    "caps": UNICAMERAL(),
    "hyphen": c("not-used", "No hyphenation (Arabic, Persian); lines break between words",
        ["Lines are broken at word boundaries, not at gaps after non-joining letters.",
         "No hyphenation is used for Arabic script when used for Arabic and Persian."],
        [("alreq", "h_line_breaking"), ("n:arab/arb", "linebreak"), ("arfa-checklist", "")]),
    "linespacing": c("convention", "Larger than Latin; much larger for Nastaʻlīq",
        ["Ascenders and descenders travel further from the baseline than Latin; line height must allow for this.",
         "Nastaʻlīq’s cascading baselines can require quite large line heights compared with many other orthographies."],
        [("n:arab/arb", "baselines"), ("n:arab/ur", "baselines"), ("n:arab/ks", "baselines")]),
    "padding": c("convention", "Right-to-left page progression",
        ["Books are bound on the right and pages progress right to left (Arabic, Persian, Pashto, Sindhi, Saraiki, Kashmiri)."],
        [("n:arab/arb", "generallayout"), ("n:arab/pes", "generallayout")]),
}, exceptions=[
    ("Urdu, Kashmiri, Persian (Iran)", "linespacing", "Nastaʻlīq style needs much larger line height than Naskh.", [("n:arab/ur", "baselines"), ("alreq", "h_writing_style")]),
    ("Urdu", "letterspacing", "Interword spacing is a last resort for justification; U+0640 tatweel is not used and is ignored by some Nastaʻlīq fonts.", [("n:arab/ur", "justification")]),
    ("Uighur", "hyphen", "Lines may break at any point; kashida lengthening and hyphenation can occur in the same word.", [("n:arab/ug", "linebreak"), ("n:arab/ug", "justification")]),
    ("Uighur", "font", "Italic glyphs observed leaning in the direction of text (to the left).", [("n:arab/ug", "letterforms")]),
    ("Uighur", "linespacing", "Must also look right next to Chinese text, which has a lower baseline and larger characters than Latin.", [("n:arab/ug", "baselines")]),
])

# ---------------------------------------------------------------- Bengali
script("Beng", "Bengali", ["Bangla", "Assamese", "Manipuri"], ["n:beng/bn"], {
    "font": c("not-used", "Italic and bold not traditional",
        ["Italicisation, bolding, and underlining are not traditional features of Bengali text."], [("n:beng/bn", "emphasis")]),
    "decoration": c("not-used", "Underline not traditional", ["Underlining is not a traditional feature of Bengali text."], [("n:beng/bn", "emphasis")]),
    "aspect": c("convention", "Basic letters slightly above Latin x-height",
        ["Basic Bangla letters are typically slightly higher than Latin x-height; some letters and marks extend beyond Latin ascenders."],
        [("n:beng/bn", "baselines")]),
    "letterspacing": c("convention", "Applied per orthographic syllable; more prevalent than in Hindi",
        ["In Indian languages letter spacing is inserted after each orthographic syllable, not each character; ILReq says it is more prevalent in Bengali."],
        [("ilreq", "h_letter_spacing")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Possible but uncommon",
        ["Bengali can be hyphenated at line wrap, though it is not very common because most words are short; a hyphen is added at line end."],
        [("n:beng/bn", "linebreak")]),
    "linespacing": c("convention", "Slightly more than Latin",
        ["Bangla requires slightly more vertical space than Latin text."], [("n:beng/bn", "baselines")]),
})

# ---------------------------------------------------------------- Canadian Syllabics
script("Cans", "Canadian Aboriginal Syllabics", ["Inuktitut", "Plains Cree"], ["n:cans/ike", "n:cans/crk"], {
    "font": c("convention", "Italic observed; function unclear",
        ["Italicised text is used frequently on East Cree web pages but its function is not clear."], [("n:cans/crk", "fontstyle")]),
    "aspect": c("convention", "Basic letters ≈ Latin cap-height",
        ["Basic letter height is usually the Latin cap-height; no ascenders, descenders, or combining marks except the long-vowel dot."],
        [("n:cans/ike", "baselines"), ("n:cans/crk", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Hyphenation used; important for long Inuktitut words",
        ["Inuktitut uses hyphenation; it is important because words can be very long and helps justification in narrow columns.",
         "Plains Cree uses U+1400 CANADIAN SYLLABICS HYPHEN because a standard hyphen can be confused with U+1428."],
        [("n:cans/ike", "linebreak"), ("n:cans/ike", "justification"), ("n:cans/crk", "linebreak")]),
    "linespacing": c("convention", "Slightly more than Latin",
        ["The long-vowel dot sits above the Latin ascender line, creating a need for slightly larger line spacing."],
        [("n:cans/ike", "baselines")]),
}, exceptions=[
    ("Plains Cree", "hyphen", "Hyphen character is U+1400, not U+002D/U+2010.", [("n:cans/crk", "linebreak")]),
])

# ---------------------------------------------------------------- Cherokee
script("Cher", "Cherokee", ["Cherokee"], ["n:cher/chr"], {
    "font": c("convention", "Users want bold/italic; not yet common",
        ["Cherokee users would like fonts with italic and bold styles, used as for Latin; this is not currently common."],
        [("n:cher/chr", "fontstyle")]),
    "aspect": c("convention", "Upper = Latin cap-height; lower = Latin x-height",
        ["Uppercase Cherokee letters are at Latin cap-height and lowercase at Latin x-height (Noto Sans Cherokee). Glyphs rarely descend."],
        [("n:cher/chr", "baselines")]),
    "caps": c("convention", "Bicameral since Unicode 8; existing text is uppercase",
        ["Lowercase letters were added in Unicode 8.0. Traditional text is uppercase; mixed-case text uses lowercase for most body text.",
         "Cherokee case-folds to uppercase, not lowercase. Upper/lowercase shapes differ mainly in size."],
        [("n:cher/chr", "transforms"), ("n:cher/chr", "cs")]),
    "hyphen": c("no-data", "No data", ["Lines break at inter-word spaces; nothing is said about hyphenation."], [("n:cher/chr", "linebreak")]),
    "letterspacing": c("convention", "Justification by interword spacing", ["Justification is done principally by adjusting the space between words."], [("n:cher/chr", "justification")]),
    "linespacing": c("convention", "Similar to Latin", ["No combining marks in normal text; glyphs are generally the same height and rarely descend."], [("n:cher/chr", "baselines")]),
})

# ---------------------------------------------------------------- Cyrillic
script("Cyrl", "Cyrillic", ["Russian", "Ukrainian", "Uzbek", "Azerbaijani", "Bulgarian", "Serbian"], ["n:cyrl/ru", "n:cyrl/uk"], {
    "font": c("convention", "Italic letterforms can differ radically from regular; vary by language",
        ["There can be a significant difference in shape between regular and italic forms of the same character, and italic shapes can vary by language."],
        [("n:cyrl/ru", "fontstyle"), ("n:cyrl/uk", "fontstyle")]),
    "aspect": c("convention", "Same metrics as Latin",
        ["Font metrics are mostly the same as ASCII text; some diacritics on capitals rise above the ASCII ascender."],
        [("n:cyrl/ru", "baselines")]),
    "caps": c("convention", "Bicameral", ["Russian and Ukrainian are bicameral; applications may need case transforms."], [("n:cyrl/ru", "transforms"), ("n:cyrl/uk", "transforms")]),
    "hyphen": c("no-data", "No data", ["Spaces are the primary break opportunities; hyphenation is not described."], [("n:cyrl/ru", "linebreak")]),
    "letterspacing": c("convention", "Justification by interword spacing", ["Justification is done principally by adjusting the space between words."], [("n:cyrl/ru", "justification")]),
    "linespacing": c("convention", "Similar to Latin", ["Little in the way of ascenders/descenders beyond Latin; metrics mostly the same as ASCII."], [("n:cyrl/ru", "baselines")]),
})

# ---------------------------------------------------------------- Devanagari
script("Deva", "Devanagari", ["Hindi", "Marathi", "Bhojpuri", "Maithili", "Awadhi", "Nepali"], ["n:deva/hi"], {
    "font": c("not-used", "Italic and bold not traditional for highlighting",
        ["Italicisation and bolding are not traditionally used for highlighting text in Devanagari."], [("n:deva/hi", "emphasis")]),
    "decoration": c("not-used", "Underline not traditional", ["Underlining is not a traditional feature of Devanagari text."], [("iip-deva", "")]),
    "aspect": c("convention", "Basic letters / hanging baseline slightly above Latin x-height",
        ["Basic letters and the hanging baseline are just slightly higher than Latin x-height; vowel signs with tone marks go slightly beyond Latin ascenders/descenders."],
        [("n:deva/hi", "baselines")]),
    "letterspacing": c("convention", "Used decoratively; applied per syllable and breaks the top bar",
        ["Inter-character spacing is sometimes applied (banners, newspapers, name plates); the top bar then appears broken.",
         "Space is inserted after each orthographic syllable, not after each code point."],
        [("n:deva/hi", "spacing"), ("ilreq", "h_letter_spacing")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Possible but uncommon for Hindi",
        ["Devanagari can be hyphenated at line wrap, but it is not very common for Hindi (mostly short words); it is much more common for Sanskrit.",
         "A hyphen is added at the end of the line."],
        [("n:deva/hi", "linebreak")]),
    "linespacing": c("convention", "Slightly more than Latin",
        ["Ascenders and vowel signs, especially with tone marks, push slightly beyond Latin ascenders and descenders."], [("n:deva/hi", "baselines")]),
}, exceptions=[
    ("Marathi, Bhojpuri, Maithili, Awadhi, Nepali", "*", "No language-specific source found; script-level values are taken from Hindi notes and ILReq.", []),
])

# ---------------------------------------------------------------- Ethiopic
script("Ethi", "Ethiopic", ["Amharic", "Tigriña"], ["n:ethi/am"], {
    "font": c("convention", "Classic heavy typeface: avoid bold for emphasis",
        ["With the classic heavy typeface, bold should not be used for emphasis because it is hard to distinguish from regular; bold suits titles when designed for it.",
         "With modern thinner typefaces, bold and italic can be used effectively.",
         "When the rendering typeface is unknown, avoid bold in favour of underline or italics.",
         "Latin text set alongside Ethiopic is commonly made heavier to match Ethiopic weight."],
        [("elreq-sg", "h_emphasis_boldface"), ("elreq-sg", "h_emphasis_italic"), ("elreq", "relative_typeface_weights")]),
    "size": c("numeric", "Emphasis by +≈25% size (single-typeface works)",
        ["Where only one typeface is available, mid-sentence emphasis is sometimes shown by enlarging the font by around 25%. Use mainly when reproducing works that already do this."],
        [("elreq-sg", "h_emphasis_inline_size_change")]),
    "aspect": c("convention", "Variable letter heights: up to Latin ascender; some at cap-height",
        ["In the classic style letter heights vary. Letters with a top bar reach about the Latin ascender height; others are at cap-height. Nothing goes below the Latin descender.",
         "Relative letter heights change between typefaces."],
        [("n:ethi/am", "baselines"), ("elreq", "relative_character_heights")]),
    "decoration": c("convention", "Underline is preferred emphasis with classic typeface; often heavier; wordspace inherits it",
        ["Underline is the more appropriate emphasis for the classic heavy typeface and has historic precedence.",
         "Underlines are often made heavier to match the weight of Ethiopic letters; the gap analysis says they need to be thicker than in English text.",
         "A wordspace (፡) after an emphasised word should receive the same emphasis, including underline."],
        [("elreq-sg", "h_emphasis_underscore"), ("elreq", "emphasis_within_prose"), ("ethi-checklist", ""), ("elreq", "emphasis_with_wordspace")]),
    "letterspacing": c("convention", "Justify by interword spacing; ፡ width changes rather than adding spaces",
        ["Ethiopic is usually justified by adjusting interword spacing; when ፡ separates words, the wordspace width changes and no extra spaces are added."],
        [("n:ethi/am", "justification")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Traditionally none; open question for space-separated text",
        ["Classical text using ፡ did not need hyphenation; older text wraps wherever it hits the margin without hyphens.",
         "Whether to hyphenate when spaces separate words is an open question in ELReq."],
        [("elreq", "ethiopic_hyphenation"), ("n:ethi/am", "linebreak")]),
    "linespacing": c("convention", "Similar to Latin unless diacritics are added above",
        ["Height differences from Latin are small; diacritics above letters increase line height."], [("n:ethi/am", "baselines")]),
    "paraspacing": c("convention", "First-line indent is regular practice; amount not specified",
        ["Paragraph indentation is a regular practice in Ethiopic publishing; ELReq lists the indent amount as an open question."],
        [("elreq", "first_paragraph")]),
    "padding": c("numeric", "Ge’ez religious literature: margins ≈ 1 : 2 : 4 (gutter : top/fore-edge : bottom)",
        ["Top and fore-edge margins are commonly twice the gutter and half the bottom. ELReq notes this is not well understood and seeks expert input."],
        [("elreq", "h_page_margins")]),
})

# ---------------------------------------------------------------- Georgian
script("Geor", "Georgian", ["Georgian"], ["n:geor/ka"], {
    "font": c("convention", "Emphasis via mtavruli (all-caps style) rather than weight",
        ["Modern Georgian tends to use mtavruli for a word or phrase to show emphasis."], [("n:geor/ka", "emphasis")]),
    "aspect": c("convention", "Same metrics as Latin", ["Georgian metrics match Latin, including x-height, ascenders, descenders, cap-height (Noto)."], [("n:geor/ka", "baselines")]),
    "caps": c("convention", "Mtavruli applied to whole words only, never initial letter",
        ["Mtavruli characters are used like ALL-CAPS on whole words or phrases, never just the first letter of a word."], [("n:geor/ka", "emphasis"), ("ucd", "")]),
    "hyphen": c("convention", "Hyphenation used", ["Georgian uses hyphenation to fit text to lines better."], [("n:geor/ka", "linebreak")]),
    "linespacing": c("convention", "Same as Latin", ["No vowel or tone marks above or below base characters; metrics match Latin."], [("n:geor/ka", "baselines")]),
})

# ---------------------------------------------------------------- Greek
script("Grek", "Greek", ["Greek"], ["n:grek/el"], {
    "caps": c("convention", "Bicameral; all-caps drops tonos, keeps dialytika",
        ["When a whole word is capitalised the tonos is dropped; dialytika is kept. Diphthongs with tonos gain a dialytika in all-caps. Disjunctive ή keeps its tonos.",
         "Uppercase→lowercase cannot be done reliably because context determines where tonos is restored."],
        [("n:grek/el", "transforms")]),
    "hyphen": c("convention", "Hyphenation used; rules from official grammar",
        ["Hyphenation is a feature of modern Greek with consonant-cluster rules; certain vowel combinations and diphthongs are not split. The marker is a hyphen at line end."],
        [("n:grek/el", "linebreak")]),
    "letterspacing": c("convention", "Justification by interword spacing", ["The primary justification point is the space between words."], [("n:grek/el", "justification")]),
})

# ---------------------------------------------------------------- Gujarati
script("Gujr", "Gujarati", ["Gujarati"], ["n:gujr/gu"], {
    "caps": UNICAMERAL(),
    "letterspacing": c("convention", "Gaps between units are admissible (not a cursive script)",
        ["CSS Text 3 notes Indic scripts with baseline connectors such as Devanagari and Gujarati are not cursive and do admit gaps."],
        [("css-text-3", "cursive-script")]),
    "hyphen": c("no-data", "No data", ["Lines break on spaces between words; hyphenation is not described."], [("n:gujr/gu", "linebreak")]),
})

# ---------------------------------------------------------------- Gurmukhi
script("Guru", "Gurmukhi", ["Panjabi"], ["n:guru/pa"], {
    "font": c("convention", "Italic sets off blocks, not emphasis; bold occurs",
        ["Italic is not commonly used for emphasis; slanted text sets off blocks, by-lines, etc. Slanted text and bolding occur in modern texts."],
        [("n:guru/pa", "fontstyle")]),
    "aspect": c("convention", "Basic letters slightly above Latin x-height",
        ["Basic letters are typically slightly higher than Latin x-height; conjuncts and diacritics extend slightly below Latin descenders."], [("n:guru/pa", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("no-data", "No data", ["Lines break at inter-word spaces; hyphenation is not described."], [("n:guru/pa", "linebreak")]),
    "letterspacing": c("convention", "Justify by interword spacing; space before danda not stretched",
        ["Lines are justified by stretching inter-word spaces; the space before an end-of-sentence danda is not stretched."], [("n:guru/pa", "justification")]),
    "linespacing": c("convention", "Slightly more than Latin", ["Gurmukhi requires slightly more vertical space than Latin."], [("n:guru/pa", "baselines")]),
})

# ---------------------------------------------------------------- Korean
script("Hang/Kore", "Hangul (Korean, incl. mixed Hanja)", ["Korean"], ["n:kore/ko"], {
    "font": c("no-data", "No data",
        ["KLReq: both fixed-width and proportional Hangul fonts are used. Its section on bold/italic is marked ‘content is needed’."],
        [("klreq", "fonts-types"), ("klreq", "h_letterforms")]),
    "decoration": c("convention", "Underline below (horizontal) / right (vertical), with a gap from glyphs",
        ["Underlines appear below horizontal text and to the right of vertical text, low enough to leave a gap below the characters (text-underline-position: under right).",
         "Underlines may exclude the particle syllables at the end of a word. Emphasis dots go above syllables in horizontal text."],
        [("n:kore/ko", "textdecor"), ("n:kore/ko", "emphasis")]),
    "letterspacing": c("numeric", "Zero by default",
        ["Hangul, Hanja and Kana have zero space between characters by default; narrower/wider settings exist for justification.",
         "Unlike Chinese/Japanese, no extra gap is normally inserted between Hangul and Latin text."],
        [("klreq", "chartypes-intercharspace"), ("n:kore/ko", "spacing")]),
    "caps": c("not-used", "No case", ["There is no upper/lowercase distinction in Korean syllables."], [("klreq", "h_transforms")]),
    "hyphen": c("convention", "Break by syllable or by word; hyphen described only for English",
        ["Hangul lines break on a character or word basis by user choice; KLReq describes hyphens only for English text in Korean documents."],
        [("klreq", "line-break"), ("n:kore/ko", "linebreak")]),
    "linespacing": c("numeric", "Proportional line spacing; example 160% of character size",
        ["KLReq describes four methods (percentage of character size, fixed value, space only, minimum). Its example value for proportional spacing is 160%.",
         "160% is shown as an example setting, not stated as a standard."],
        [("klreq", "line-space")]),
    "paraspacing": c("convention", "First-line indent of one character width by default",
        ["The character width of the paragraph is the default indent unit. Indenting every paragraph is the most common mode; no indent suits shorter horizontal lines."],
        [("klreq", "line-head-indent")]),
    "padding": c("convention", "Page body position is defined by margin values; tables have inner padding",
        ["The page body is the area excluding the top/bottom/left/right margins; its position is linked to margin values.",
         "Tables and cells have inner padding; cell padding takes priority over table padding."],
        [("klreq", "page-body"), ("klreq", "inner-padding")]),
})

# ---------------------------------------------------------------- Han (Chinese)
script("Hani", "Han (Chinese)", ["Simplified Chinese", "Traditional Chinese"], ["n:hani/zh"], {
    "font": c("convention", "Song (Ming) for body; Hei or bold Song for headings",
        ["CLReq names four frequently used typeface styles: Song, Kai, Hei, Fangsong. Song is currently the most common in printing.",
         "Headings use Hei or bold Song; when Hei is used for low-level headings its weight is increased.",
         "Mainland China stipulates Fangsong in principle for government official documents."],
        [("clreq", "four_commonly_used_typefaces_for_chinese_composition"), ("clreq", "song"), ("clreq", "kai"), ("clreq", "hei"), ("clreq", "imitation_song"), ("clreq", "styling_of_headings")]),
    "size": c("numeric", "Body: Size 5 (10.5 pt); minimum Size 6 (≈7.875 pt, 2.8 mm)",
        ["Size 5 is usually used for body text. The acceptable minimum is Size 6 (7.875 pt ≈ 2.8 mm); smaller is hard to read because of the complex structure of Han characters.",
         "Headings 10–20% larger than body; e.g. 9 pt body → 10/12/14 pt headings."],
        [("clreq", "considerations_in_designing_type_area"), ("clreq", "styling_of_headings")]),
    "aspect": c("convention", "Square character frame; letter face smaller, centred",
        ["Han characters have square frames of equal size with a smaller centred character face. Font size is measured by the frame."],
        [("clreq", "h_baselines")]),
    "decoration": c("convention", "Lines mark proper nouns and titles, not emphasis; left side in vertical text",
        ["Straight or wavy side lines indicate proper nouns and book titles, not emphasis.",
         "Lines appear below horizontal text and to the left of vertical text; emphasis dots go below (horizontal) or right (vertical).",
         "Adjacent underlined items should have a break between their lines."],
        [("n:hani/zh", "text_decoration"), ("n:hani/zh", "emphasis"), ("clreq", "id84")]),
    "letterspacing": c("numeric", "Solid setting (0) for body; up to ¼ em gap next to Latin/numerals",
        ["Characters are set solid. Increased spacing (examples ¼, ⅓, ½, 1 em) is used for running heads, captions, short poetry, and children’s publications.",
         "A gap of up to ¼ em is suggested between Han and Latin/numerals."],
        [("clreq", "considerations_in_designing_type_area"), ("clreq", "increased_inter_character_spacing"), ("n:hani/zh", "letterspace")]),
    "caps": UNICAMERAL(),
    "hyphen": c("not-used", "No hyphenation; wraps between characters",
        ["Lines wrap between characters; there is no hyphenation."], [("n:hani/zh", "linebreak")]),
    "linespacing": c("numeric", "Line gap 50–100% of character frame; not above 100%",
        ["The line gap is commonly 50–100% of the character frame height; shorter for short lines or small sizes. Exceeding the font size does not improve reading.",
         "The line gap must accommodate interlinear decorations and emphasis dots and stay constant."],
        [("clreq", "considerations_in_designing_type_area"), ("n:hani/zh", "baselines")]),
    "paraspacing": c("numeric", "No extra space; 2 em first-line indent (1 em in narrow columns)",
        ["There is in principle no extra spacing between paragraphs; the gap equals the line gap. A blank line signals end of section.",
         "Publications usually use a 2 em first-line indent; multi-column magazines may use 1 em."],
        [("clreq", "first_line_indents")]),
    "linelength": c("numeric", "Books 17–40 chars; min 10; max 48 horizontal / 55 vertical",
        ["Most books use 17–40 characters per line. Body lines should not be less than 10 characters, and should not exceed 48 (horizontal) or 55 (vertical).",
         "Line length should be an integer multiple of the font size."],
        [("clreq", "considerations_in_designing_type_area")]),
    "padding": c("convention", "Type area defined on a character grid; shape similar to trim size",
        ["The type area’s dimensions consider trim size and margins; its shape can be similar to the trim size. The type area also defines a grid that characters align to."],
        [("clreq", "considerations_in_designing_type_area"), ("clreq", "main_elements_of_basic_composition")]),
}, exceptions=[
    ("Traditional Chinese (Taiwan, Hong Kong)", "hyphen", "Line start/end prohibition rules are sometimes not observed, especially in newsprint with narrow columns.", [("n:hani/zh", "linebreak")]),
    ("Traditional Chinese", "linespacing", "Pronunciation marks (Bopomofo) may be inserted between lines; the line gap must be sized to fit them.", [("clreq", "considerations_in_designing_type_area")]),
])

# ---------------------------------------------------------------- Hebrew
script("Hebr", "Hebrew", ["Hebrew"], ["n:hebr/he"], {
    "font": c("convention", "Bold (often light) for emphasis; italic controversial",
        ["Bold is used for emphasis and highlighting; the degree of bolding is often quite light. Bold-italic is mostly for display text.",
         "Use of italic in Hebrew is controversial; slant direction preference varies."],
        [("n:hebr/he", "fontstyle"), ("hlreq", "h_letterforms")]),
    "aspect": c("convention", "Slightly taller than Latin x-height", ["Hebrew characters are commonly slightly taller than Latin x-height."], [("n:hebr/he", "baselines")]),
    "decoration": c("convention", "Underline is an alternative emphasis", ["Alternatives to tracking for emphasis include a different typeface and/or underlining."], [("n:hebr/he", "emphasis")]),
    "letterspacing": c("convention", "Increased tracking is a common emphasis method",
        ["Increased tracking is a common way to express emphasis or highlight text (e.g. terms in a dictionary)."], [("n:hebr/he", "spacing"), ("hlreq", "h_spacing")]),
    "caps": UNICAMERAL(),
    "hyphen": c("no-data", "No data", ["Lines are normally broken at word boundaries; hyphenation is not described."], [("n:hebr/he", "linebreak")]),
    "padding": c("convention", "Right-to-left page progression", ["Books are bound on the right; pages progress right to left."], [("n:hebr/he", "generallayout")]),
})

# ---------------------------------------------------------------- Javanese
script("Java", "Javanese", ["Javanese"], ["n:java/jv"], {
    "font": c("convention", "Slant used for whole blocks, not inline",
        ["Slanted text (1933 publication) distinguishes blocks: panels, subheadings, captions, by-lines; not used inline."], [("n:java/jv", "fontstyle")]),
    "aspect": c("convention", "Basic letters ≈ Latin x-height; overall height 2–3× Latin",
        ["Basic letters are around Latin x-height but overall height is 2 to 3 times that of Latin letters."], [("n:java/jv", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("not-used", "Breaks after syllables; no hyphenation",
        ["Lines break after full orthographic syllables without splitting conjuncts; hyphenation as such is not used."], [("n:java/jv", "linebreak")]),
    "letterspacing": c("convention", "Slight inter-character stretch observed in justification",
        ["Justification observed in a 1933 publication stretches spaces and slightly stretches inter-character spaces (not stacks)."], [("n:java/jv", "justification")]),
    "linespacing": c("convention", "Far more than Latin", ["Javanese requires far more vertical space than Latin, creating a need for much larger line spacing."], [("n:java/jv", "baselines")]),
    "paraspacing": c("convention", "Paragraph indents observed", ["One article in the 1933 Kajawen publication uses paragraph indents."], [("n:java/jv", "justification")]),
})

# ---------------------------------------------------------------- Japanese
script("Jpan", "Japanese", ["Japanese"], ["n:jpan/ja"], {
    "font": c("convention", "Mincho (light, Hoso-mincho) for body; Gothic for headings/emphasis",
        ["Mincho is the most frequently used typeface for main text; body Mincho is usually light weight (Hoso-mincho).",
         "Headings use Mincho or Japanese Gothic, sometimes heavier weight. A Gothic face in Mincho text is a common emphasis method; italic and bold are not in the list of emphasis methods."],
        [("jlreq", "font_selection_and_font_size_of_heading"), ("jlreq", "terminology"), ("n:jpan/ja", "emphasis")]),
    "size": c("numeric", "Body 9 pt common; minimum 8 pt",
        ["Generally 9 pt (≈3.2 mm) is common; except for dictionaries etc., the minimum is 8 pt (≈2.8 mm).",
         "JLReq contrasts this with Western layout, where 10 or 12 pt is common, because of differences in letter design.",
         "Headings e.g. 10/12/14 pt for 9 pt body; or a constant 15–20% step."],
        [("jlreq", "considerations_in_designing_the_kihonhanmen"), ("jlreq", "font_selection_and_font_size_of_heading")]),
    "aspect": c("convention", "Square character frame; letter face smaller, centred",
        ["Kanji and kana share square frames of equal size; a smaller centred letter face holds the glyph. Size is measured by the frame. Small kana are offset within the frame."],
        [("jlreq", "kanji_hiragana_and_katakana")]),
    "decoration": c("convention", "Below (horizontal) / right (vertical), just outside the character box",
        ["Underlines may be used for emphasis. Lines appear below horizontal text and right of vertical text (unlike Chinese), immediately outside the character box.",
         "Boten (emphasis dots) go above characters in horizontal text and right in vertical text."],
        [("n:jpan/ja", "text_decoration"), ("n:jpan/ja", "emphasis")]),
    "letterspacing": c("numeric", "Solid setting (0) for body; ¼ em gap next to Latin/numerals",
        ["Body text is set solid (no extra space between character frames); this is the most reader-friendly approach.",
         "Fixed inter-character spacing is used for short running heads, headings, captions, short poetry. Tsumegumi (negative spacing) is rare in books, used for large headings.",
         "JLReq suggests a ¼ em gap between kanji/kana and Latin/numerals."],
        [("jlreq", "principles_of_arrangement_of_kanji_and_kana_characters"), ("n:jpan/ja", "letterspace")]),
    "caps": UNICAMERAL(),
    "hyphen": c("not-used", "No hyphenation; wraps between characters", ["There is no hyphenation at line-breaks for Japanese text."], [("n:jpan/ja", "linebreak")]),
    "linespacing": c("numeric", "Line gap ½–1 em; ≈1 em when line > 35 chars; not above 1 em",
        ["The line gap is commonly between half-em and one-em of the character frame. Half-em suits short lines; one em or close to it is better above 35 characters per line.",
         "A line gap larger than full-width decreases legibility unless ruby/annotations need the space.",
         "JLReq notes the Western standard line gap is said to be ⅓ em."],
        [("jlreq", "considerations_in_designing_the_kihonhanmen")]),
    "paraspacing": c("numeric", "Space between paragraphs = line gap; 1 em first-line indent",
        ["The space between paragraphs is usually the same as the line gap. Paragraphs are marked by a one-em first-line indent, used in nearly all books and magazines.",
         "Understanding 1.4.12 notes that Japanese does not use spacing following paragraphs."],
        [("jlreq", "processing_of_spaces_between_paragraphs"), ("jlreq", "line_head_indent_at_the_beginning_of_paragraphs"), ("u-1412", "")]),
    "linelength": c("numeric", "Max ≈40 chars horizontal / ≈52 vertical",
        ["The best line length is around 52 characters maximum (vertical) and 40 maximum (horizontal); use columns if the page would exceed this.",
         "Line length should be a multiple of the character size."],
        [("jlreq", "considerations_in_designing_the_kihonhanmen")]),
    "padding": c("convention", "Text area set in characters × lines; margins are what remains",
        ["Japanese text areas are usually defined by width and height in characters and lines; margins are determined from what remains of the page.",
         "The text area shape should be similar to the trim size."],
        [("n:jpan/ja", "generallayout"), ("jlreq", "considerations_in_designing_the_kihonhanmen"), ("jlreq", "elements_of_kihonhanmen")]),
})

# ---------------------------------------------------------------- Khmer
script("Khmr", "Khmer", ["Khmer"], ["n:khmr/km"], {
    "aspect": c("convention", "Basic letters between Latin x-height and ascender (font-dependent)",
        ["Basic letter height is around Latin ascender height in one Noto font and around x-height in the other; extenders and marks go well beyond Latin ascenders/descenders."],
        [("n:khmr/km", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Break at word boundaries; not at sub-word syllables",
        ["Line-breaks are expected at word boundaries (no spaces between words). Text is not broken at sub-word syllable boundaries. ZWSP/WJ control breaks."],
        [("n:khmr/km", "linebreak")]),
    "linespacing": c("convention", "Larger than Latin", ["Extenders and combining marks create a need for larger line spacing."], [("n:khmr/km", "baselines")]),
})

# ---------------------------------------------------------------- Kannada
script("Knda", "Kannada", ["Kannada"], [], {
    "caps": UNICAMERAL(),
})

# ---------------------------------------------------------------- Lao
script("Laoo", "Lao", ["Lao"], ["n:laoo/lo"], {
    "font": c("convention", "Italic for captions and quotations", ["Italicised text observed for figure captions and quotations."], [("n:laoo/lo", "fontstyle")]),
    "aspect": c("convention", "Basic letters slightly above Latin x-height", ["Basic height slightly above Latin x-height; stacked marks reach well beyond Latin ascenders/descenders."], [("n:laoo/lo", "baselines")]),
    "caps": UNICAMERAL(),
    "linespacing": c("convention", "Larger than Latin; Lao adds more interline spacing",
        ["Stacked vowel and tone marks need higher vertical resolution; Lao also tends to add more interline spacing than Latin."], [("n:laoo/lo", "baselines")]),
})

# ---------------------------------------------------------------- Latin
script("Latn", "Latin", ["English", "Spanish", "Portuguese", "German", "Javanese", "Malay", "Vietnamese", "French", "Turkish", "Italian", "Polish", "Hausa", "Tagalog", "Yoruba", "Uzbek", "Fula", "Romanian", "Oromo", "Igbo", "Azerbaijani", "Cebuano", "Dutch", "Kurdish", "Croatian", "Malagasy", "Hungarian", "Catalan"],
       ["n:latn/ff", "n:latn/ha", "n:latn/kmr"], {
    "size": c("numeric", "10–12 pt common in Western layout (per JLReq)",
        ["JLReq states that in Western text layout 10 pt (≈3.5 mm) or 12 pt (≈4.2 mm) type is common. No Latin-specific requirements document was found."],
        [("jlreq", "considerations_in_designing_the_kihonhanmen")]),
    "caps": c("convention", "Bicameral; language-specific casing rules exist",
        ["Turkish (and other Turkic languages using Turkish casing rules) map dotted/dotless i differently from English.",
         "Dutch capitalises word-initial ij as IJ."],
        [("css-text-3", "text-transform-property"), ("nl-checklist", "")]),
    "hyphen": c("convention", "Hyphenation used; practice varies by language",
        ["Hyphenation practices vary: hyphen before the break, after it, both, a different character, or spelling changes (CSS Text 3 examples: English, Dutch, Hungarian)."],
        [("css-text-3", "hyphenation")]),
    "linespacing": c("numeric", "Line gap ≈ ⅓ em (per JLReq)",
        ["JLReq: ‘It is said that the standard line-gap in Western text layout is one third em’. Kurmanji line height is the same as other simple Latin orthographies."],
        [("jlreq", "considerations_in_designing_the_kihonhanmen"), ("n:latn/kmr", "baselines")]),
    "letterspacing": c("convention", "Justification by interword spacing", ["Principal justification opportunities are inter-word spaces (Kurmanji)."], [("n:latn/kmr", "justification")]),
}, exceptions=[
    ("Dutch", "caps", "Word-initial ‘ij’ capitalises as ‘IJ’ (ijs → IJs).", [("nl-checklist", "")]),
    ("Dutch", "hyphen", "Hyphenation can change spelling (cafeetje → café-tje).", [("css-text-3", "hyphenation"), ("nl-checklist", "hyphenation")]),
    ("Hungarian", "hyphen", "Hyphenation can change spelling (Összeg → Ösz-szeg).", [("css-text-3", "hyphenation")]),
    ("Turkish (and Turkic languages using Turkish casing)", "caps", "I/ı and İ/i case mappings replace the English I/i mapping.", [("css-text-3", "text-transform-property")]),
    ("English, Spanish, Portuguese, German, Malay, Vietnamese, French, Italian, Polish, Tagalog, Yoruba, Romanian, Oromo, Igbo, Cebuano, Croatian, Malagasy, Catalan", "*", "No language-specific source ingested; script-level Latin values apply only where cited.", []),
])

# ---------------------------------------------------------------- Malayalam
script("Mlym", "Malayalam", ["Malayalam"], ["n:mlym/ml"], {
    "aspect": c("convention", "Basic letters ≈ Latin x-height", ["Basic letter height around Latin x-height; extenders slightly beyond Latin ascenders/descenders."], [("n:mlym/ml", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "In-word breaks very common; usually no visible marker",
        ["Long agglutinative words make in-word breaks very common, especially in newsprint. Breaks are mostly at syllable boundaries and usually have no visual marker."],
        [("n:mlym/ml", "linebreak")]),
    "linespacing": c("convention", "Slightly more than Latin", ["Creates a need for slightly larger line spacing."], [("n:mlym/ml", "baselines")]),
})

# ---------------------------------------------------------------- Mongolian
script("Mong", "Mongolian", ["Mongolian"], ["n:mong/mn"], {
    "font": c("not-used", "No italics", ["Mongolian has no concept of italics. If synthesised, vertical text tilts clockwise."], [("mlreq", "h_letterforms")]),
    "aspect": c("convention", "Smaller than Chinese/Japanese at the same font size",
        ["At the same font size Mongolian appears smaller than Chinese or Japanese; numbers appear slightly larger than Mongolian."],
        [("mlreq", "mixed_arrangement_cjk"), ("mlreq", "mixed_arrangement_alphanum")]),
    "decoration": c("convention", "Right line = underline; left line = overline; centred strikethrough",
        ["In vertical text the ‘right line’ functions like an underline and the ‘left line’ like an overline; strikethrough is baseline-centred.",
         "Lines may skip inter-word spaces but must not skip the gaps before suffixes (U+202F, U+180E)."],
        [("mlreq", "h_text_decor")]),
    "letterspacing": c("not-used", "Cursive script: no letter spacing",
        ["CSS Text 3 lists Mongolian as a cursive script that does not admit gaps between letters."], [("css-text-3", "cursive-script")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Words not broken; hyphenated compounds break with the hyphen moved to the next line",
        ["Words are not normally broken. Compounds may break at a hyphen, which moves to the next line; Unicode provides U+1806 for this."],
        [("n:mong/mn", "linebreak"), ("mlreq", "h_line_breaking")]),
    "paraspacing": c("convention", "Indent or paragraph leading; no standard amount",
        ["A new paragraph may be signalled by first-line indentation or by paragraph leading. MLReq: there is no clear standard for indentation amount."],
        [("n:mong/mn", "justification"), ("mlreq", "first_line_indents")]),
    "padding": c("convention", "Bound on the left; columns run horizontally; landscape pages common",
        ["Books are bound on the left. Columns run horizontally. Landscape orientation is common."], [("n:mong/mn", "generallayout")]),
})

# ---------------------------------------------------------------- Myanmar
script("Mymr", "Myanmar", ["Burmese", "Shan"], ["n:mymr/my", "n:mymr/shn"], {
    "font": c("convention", "Italic for quotations and titles", ["Italicisation observed in Wikipedia for quotations and publication titles."], [("n:mymr/my", "fontstyle")]),
    "aspect": c("convention", "Basic letters ≈ Latin x-height", ["Basic height around Latin x-height; overall height and marks extend beyond Latin."], [("n:mymr/my", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Break at syllable boundaries outside words, or at phrases",
        ["Breaks can occur at syllable boundaries but not within a word; a common approach breaks at phrase boundaries."], [("n:mymr/my", "linebreak")]),
    "letterspacing": c("convention", "Justification starts with inter-phrase spacing", ["Justification may begin by adjusting inter-phrase spacing."], [("n:mymr/my", "justification")]),
    "linespacing": c("convention", "Larger than Latin", ["Burmese requires more vertical space than Latin."], [("n:mymr/my", "baselines")]),
}, exceptions=[
    ("Shan", "*", "Orthography notes sections are marked ‘tbd’; no Shan-specific values.", [("n:mymr/shn", "linebreak")]),
])

# ---------------------------------------------------------------- N'Ko
script("Nkoo", "N’Ko", ["N’Ko"], ["n:nkoo/nqo"], {
    "font": c("convention", "Bold common for emphasis; italic leans left",
        ["Authors commonly use bold and sometimes italics for emphasis. The community chose a left-leaning italic."], [("n:nkoo/nqo", "fontstyle"), ("n:nkoo/nqo", "emphasis")]),
    "aspect": c("convention", "Basic letters ≈ Latin cap-height", ["Letters are relatively uniform in height with no descenders, around Latin cap-height."], [("n:nkoo/nqo", "baselines")]),
    "letterspacing": c("not-used", "Cursive: stretch with U+07FA, not letter spacing",
        ["Text may be stretched like Arabic using ߺ (U+07FA) for fitting or headings. CSS Text 3 lists N’Ko as a cursive script."],
        [("n:nkoo/nqo", "spacing"), ("css-text-3", "cursive-script")]),
    "caps": c("not-used", "No case", ["There is no upper vs. lowercase distinction."], [("n:nkoo/nqo", "baselines")]),
    "hyphen": c("convention", "In-word breaks with U+002D at line end", ["Lines can break inside a word, adding U+002D HYPHEN-MINUS at line end."], [("n:nkoo/nqo", "linebreak")]),
    "linespacing": c("convention", "Larger than Latin", ["Combining marks and the dorome sign reach beyond Latin ascenders."], [("n:nkoo/nqo", "baselines")]),
    "padding": c("convention", "Mirror of left-to-right layouts", ["An N’Ko web page should be the mirror image of a page in, say, French, including navigation and panels."], [("n:nkoo/nqo", "generallayout")]),
})

# ---------------------------------------------------------------- Odia
script("Orya", "Odia", ["Odia"], ["n:orya/or"], {
    "caps": UNICAMERAL(),
    "hyphen": c("no-data", "No data", ["Lines are mostly broken at inter-word spaces; hyphenation is not described."], [("n:orya/or", "linebreak")]),
})

# ---------------------------------------------------------------- Osage
script("Osge", "Osage", ["Osage"], ["n:osge/osa"], {
    "aspect": c("convention", "Same metrics as Latin", ["All metrics are about the same as Latin (Noto Sans Osage)."], [("n:osge/osa", "baselines")]),
    "caps": c("convention", "Bicameral", ["Osage is bicameral."], [("n:osge/osa", "transforms")]),
    "linespacing": c("convention", "Same as Latin", ["Metrics match Latin."], [("n:osge/osa", "baselines")]),
})

# ---------------------------------------------------------------- Sinhala
script("Sinh", "Sinhala", ["Sinhalese"], ["n:sinh/si"], {
    "aspect": c("convention", "Basic letters just above Latin x-height", ["Basic height marginally higher than Latin x-height; tall letters may be reshaped to avoid large extensions."], [("n:sinh/si", "baselines")]),
    "caps": UNICAMERAL(),
    "linespacing": c("convention", "Slightly more than Latin", ["Combining marks reach a little beyond Latin ascenders."], [("n:sinh/si", "baselines")]),
})

# ---------------------------------------------------------------- Sundanese
script("Sund", "Sundanese", ["Sundanese"], ["n:sund/su"], {
    "aspect": c("convention", "Basic letters ≈ Latin cap-height", ["Basic height around Latin cap-height; marks above exceed Latin ascenders."], [("n:sund/su", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Hyphenation after full syllables (no details)", ["According to Everson, hyphenation can occur after any full orthographic syllable; no further details."], [("n:sund/su", "linebreak")]),
    "linespacing": c("convention", "Larger than Latin", ["Marks above reach beyond Latin ascenders."], [("n:sund/su", "baselines")]),
})

# ---------------------------------------------------------------- Tamil
script("Taml", "Tamil", ["Tamil"], ["n:taml/ta"], {
    "font": c("not-used", "Italic and bold not traditional", ["Italics and bold are not traditional features of Tamil text; some fonts are slightly slanted."], [("n:taml/ta", "fontstyle")]),
    "decoration": c("not-used", "Underline not traditional", ["Underlining is not a traditional feature of Tamil text."], [("n:taml/ta", "emphasis")]),
    "aspect": c("convention", "Basic letters = Latin x-height", ["Basic Tamil letter height is the same as Latin x-height (Noto Serif)."], [("n:taml/ta", "baselines")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Useful for long words; at syllable boundaries; hyphen usually not shown",
        ["Hyphenation must be at syllable boundaries; a hyphen is not usually added at line end."], [("n:taml/ta", "linebreak")]),
    "linespacing": c("convention", "Slightly more than Latin", ["Extenders go slightly beyond Latin, creating a need for slightly larger line heights."], [("n:taml/ta", "baselines")]),
})

# ---------------------------------------------------------------- Telugu
script("Telu", "Telugu", ["Telugu"], ["n:telu/te"], {
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "In-word breaks very common; hyphen observed (InDesign)",
        ["In-word breaks are very common, especially in newsprint, mostly at syllable boundaries. InDesign adds a hyphen at line end."], [("n:telu/te", "linebreak")]),
})

# ---------------------------------------------------------------- Thai
script("Thai", "Thai", ["Thai"], ["n:thai/th"], {
    "font": c("convention", "Bold for inline emphasis; italic for whole blocks (captions, by-lines)",
        ["Bold is used for emphasis and names; italic is applied to whole paragraphs (captions, by-lines, standfirsts) and direct speech."], [("n:thai/th", "fontstyle")]),
    "aspect": c("convention", "Basic letters ≈ Latin x-height (Noto) or between x- and cap-height",
        ["Basic height around Latin x-height in Noto; in other fonts between x-height and cap-height."], [("n:thai/th", "baselines")]),
    "letterspacing": c("convention", "Inter-character spacing used in justification of narrow columns",
        ["Justification primarily adjusts spaces between phrases; inter-character spacing is used mostly in narrow columns."], [("n:thai/th", "justification")]),
    "caps": UNICAMERAL(),
    "hyphen": c("convention", "Wraps at word boundaries (dictionary); hyphenation not described", ["Thai wraps at word boundaries found by dictionary lookup; the notes do not describe hyphenation."], [("n:thai/th", "linebreak")]),
    "linespacing": c("convention", "Larger than Latin; Thai adds more interline spacing",
        ["Stacked marks need higher vertical resolution; Thai tends to add more interline spacing than Latin."], [("n:thai/th", "baselines")]),
})

# ---------------------------------------------------------------- Tibetan
script("Tibt", "Tibetan", ["Tibetan", "Dzongkha"], ["n:tibt/bo"], {
    "font": c("convention", "Bold/italic not traditional; bold now seen",
        ["Tibetan never had bold or italic until bold was introduced for books; modern texts appear to use bolding."], [("n:tibt/bo", "fontstyle"), ("n:tibt/bo", "emphasis")]),
    "size": c("numeric", "Pecha: smaller text ≥ 20 pt; standard 27–30 pt",
        ["Traditional pechas have two sizes: the smaller does not usually go below 20 pt; the larger (standard) is around 27–30 pt."], [("n:tibt/bo", "generallayout")]),
    "aspect": c("convention", "Hanging baseline between Latin x-height and ascender", ["The hanging baseline falls between Latin ascender and x-height."], [("n:tibt/bo", "baselines")]),
    "letterspacing": c("convention", "Equal inter-character spacing is a justification method",
        ["One justification method adapts spacing between all characters equally; another pads with tsheg."], [("n:tibt/bo", "justification")]),
    "caps": UNICAMERAL(),
    "hyphen": c("not-used", "No hyphenation; breaks after tsheg", ["Tibetan never breaks inside a syllable and has no hyphenation; lines break after ་."], [("n:tibt/bo", "linebreak")]),
    "linespacing": c("convention", "Larger than Latin", ["Stacked consonants and marks need higher vertical resolution than English."], [("n:tibt/bo", "baselines")]),
    "paraspacing": c("convention", "First-line indent may be used", ["Modern publications use paragraphs; the first line may be indented."], [("n:tibt/bo", "generallayout")]),
    "padding": c("convention", "Pecha text sits in a (visible or invisible) box defining the margin",
        ["In pechas text is written inside a visible box defining the page margin; in recent publications it may be invisible."], [("n:tibt/bo", "generallayout")]),
})

# ---------------------------------------------------------------- Contrast column: identical everywhere
for s in SCRIPTS:
    s["cells"]["contrast"] = NO_CONTRAST()

CONTRAST_NOTES = [
    {"text": "No ingested language-enablement source (lreq documents, gap analyses, orthography notes) defines a contrast value or contrast rule for any script or language.",
     "sources": [("matrix", "")]},
    {"text": "WCAG 2.2 ‘large scale text’ includes ‘font size that would yield equivalent size for Chinese, Japanese and Korean (CJK) fonts’ but does not state that size.",
     "sources": [("wcag22-large", "")]},
    {"text": "WCAG 2.2 notes that fonts with extraordinarily thin strokes or unusual features are harder to read at lower contrast. Several sources describe script-specific stroke weight (e.g. Hebrew bold ‘often quite light’; Japanese body Mincho is light; Ethiopic classic typeface is heavy and Latin is thickened to match). These are related to contrast perception but none states a contrast requirement.",
     "sources": [("wcag22-large", ""), ("n:hebr/he", "fontstyle"), ("jlreq", "font_selection_and_font_size_of_heading"), ("elreq", "relative_typeface_weights")]},
]

WCAG2_REFERENCE = [
    {"text": "SC 1.4.12 Text Spacing (AA): line height ≥ 1.5× font size, paragraph spacing ≥ 2×, letter spacing ≥ 0.12×, word spacing ≥ 0.16×. Exception: languages/scripts that do not use a property conform using only the properties that exist for them.",
     "sources": [("wcag22-1412", "")]},
    {"text": "Understanding 1.4.12: Japanese does not use spacing following paragraphs; word spacing has no effect in languages without spaces between words. About 480 languages/scripts were tested with no adverse effects.",
     "sources": [("u-1412", "")]},
    {"text": "SC 1.4.8 Visual Presentation (AAA): width ≤ 80 characters or glyphs (40 if CJK); not justified; line spacing ≥ 1.5 within paragraphs; paragraph spacing ≥ 1.5× line spacing. Presentation aspects not used in a writing system need not be applied.",
     "sources": [("wcag22-148", ""), ("u-148", "")]},
    {"text": "These WCAG 2 values are user-adjustment targets or mechanisms, not authoring defaults. They are listed for comparison and are not used in the matrix cells.",
     "sources": []},
]
