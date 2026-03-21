"""
Shared regex patterns for eNVC detection.

Taxonomy aligned with:
  Ahmed et al. (2026). Reading Between the Lines: How Electronic
  Nonverbal Cues Shape Emotion Decoding.

Two domains:
  - Kinesics: textual gestures, touch, eye movement, facial emoji,
              emotion-conveying emoji
  - Paralinguistics: vocalics, intensity cues, patterned stylization
"""

import re

# ── Kinesics ────────────────────────────────────────────────────────

# Stage-direction actions: *hugs*, *cries*, *kicks*, etc.
STAGE_DIRECTION = re.compile(
    r"\*("
    r"hug|hugs|wave|waves|thumbs up|thumbs down|facepalm|facepalms|"
    r"heart|hearts|clap|claps|shrug|shrugs|high five|high fives|"
    r"fist bump|fist bumps|dance|dances|wink|winks|laugh|laughs|"
    r"smile|smiles|frown|frowns|cry|cries|angry|confused|"
    r"surprised|shocked|kiss|kisses|blush|blushes|roll eyes|"
    r"rolls eyes|nod|nods|sigh|sighs|scream|screams|"
    r"gasp|gasps|pout|pouts|squint|squints"
    r")\*",
    re.IGNORECASE,
)

# Facial emoji (Unicode Emoticons block + supplemental face ranges)
EMOJI_FACES = re.compile(
    r"["
    r"\U0001F600-\U0001F64F"  # emoticons
    r"\U0001F910-\U0001F96B"  # supplemental faces
    r"\U0001F970-\U0001F976"  # smiling/hot/cold/pleading
    r"\U0001F97A"             # pleading face
    r"\U0001FAE0-\U0001FAE8"  # face extras (melting, dotted line, etc.)
    r"]"
)

# Body / gesture emoji (hands, people, body parts)
EMOJI_BODY = re.compile(
    r"["
    r"\U0001F440-\U0001F4FF"  # eyes, hands, misc objects (broad)
    r"\U0001F9B0-\U0001F9BF"  # body parts (ear, leg, etc.)
    r"\U0001F9D0-\U0001F9DF"  # people/roles
    r"\U0001F90C-\U0001F90F"  # pinched fingers, etc.
    r"\U0001FAF0-\U0001FAF8"  # hand gestures (Unicode 14+)
    r"\U0000270A-\U0000270D"  # raised fist, hand, pencil
    r"\U0001F91A-\U0001F92F"  # hand/face gestures
    r"\U0001F930-\U0001F939"  # person roles
    r"]"
)

# Emotion-conveying non-facial emoji (hearts, sparkles, fire, etc.)
EMOJI_EMOTION = re.compile(
    r"["
    r"\U00002764"             # red heart
    r"\U0001F493-\U0001F49F"  # heart variants
    r"\U0001F525"             # fire
    r"\U00002728"             # sparkles
    r"\U0001F4A5"             # collision/boom
    r"\U0001F4A2"             # anger symbol
    r"\U0001F4A6"             # sweat droplets
    r"\U0001F4A8"             # dashing away
    r"\U0001F389"             # party popper
    r"\U0001F38A"             # confetti ball
    r"\U0001F3B5-\U0001F3B6"  # musical notes
    r"\U0001F4AB"             # dizzy
    r"\U0001F4AF"             # 100
    r"\U00002B50"             # star
    r"\U0001F31F"             # glowing star
    r"\U0001F480"             # skull
    r"\U0001F4A3"             # bomb
    r"\U0001F4A9"             # poo
    r"\U0001F940"             # wilted flower
    r"\U0001F339"             # rose
    r"\U0001F33A-\U0001F33E"  # flowers
    r"]"
)

# Kaomoji — common patterns like (^.^) (T_T) (>_<) etc.
KAOMOJI = re.compile(
    r"[\(\[\{<]"
    r"[\^;>T=\-\'\"]"
    r"[_.\-\s,oOvV]?"
    r"[\^;>T=\-\'\"]"
    r"[\)\]\}>]"
)


# ── Paralinguistics ────────────────────────────────────────────────

# Vocalics: interjections, laughter, vocal sounds
VOCALICS = re.compile(
    r"\b("
    # laughter
    r"l+o+l+|lmao|lmfao|rofl|"
    r"ha(ha)+|he(he)+|hi(hi)+|ho(ho)+|"
    r"baha(ha)*|muaha(ha)*|"
    # interjections
    r"sigh|yawn|groan|moan|gasp|"
    r"argh+|ugh+|oof+|gah+|bah+|"
    r"ah+|oh+|eh+|uh+|hmm+|huh+|"
    r"ooh+|aah+|eek+|eep+|"
    r"alas|bravo|brr+|doh|geez+|jeez+|"
    r"phew+|psst+|shh+|shush+|"
    r"tsk[\-]?tsk|pfft+|pff+|meh+|"
    r"whee+|whew+|woah+|whoa+|wow+|"
    r"yoo[\-]?hoo|yikes+|yay+|yep+|nah+|nope+|"
    r"omg+|omfg+|wtf+|smh+|"
    # onomatopoeia
    r"aww+|ew+w|eww+|"
    r"heh+|haha|tehe+|"
    # vocal fillers
    r"um+|erm+|uhh+"
    r")\b",
    re.IGNORECASE,
)

# Intensity: ALL CAPS words (>=2 chars, excludes common acronyms)
_ACRONYM_ALLOWLIST = {
    "I", "A", "OK", "US", "UK", "EU", "UN", "TV", "ID", "AM", "PM",
    "HR", "IT", "AI", "ML", "NLP", "API", "URL", "CEO", "CTO",
    "PhD", "MD", "BA", "MA", "NY", "LA", "DC", "CA", "TX", "FL",
    "FBI", "CIA", "NASA", "NATO", "ADHD", "HIV", "AIDS", "DNA", "RNA",
    "USB", "PDF", "HTML", "CSS", "FAQ", "DIY", "ASAP", "FYI",
    "RSVP", "WiFi", "WIFI", "HDMI", "GPS", "ATM",
}

INTENSITY_CAPS = re.compile(r"\b[A-Z]{2,}\b")

INTENSITY_PUNCTUATION = re.compile(
    r"[!]{2,}|[?]{2,}|[!?]{2,}|[?!]{2,}"
)

# Elongation: repeated letters (3+ of same char) inside a word
ELONGATION = re.compile(r"\b\w*(\w)\1{2,}\w*\b")

# Patterned stylization: alternating case (sPoNgEbOb), mixed emphasis
ALTERNATING_CASE = re.compile(
    r"\b"
    r"(?=[a-zA-Z]*[a-z])"   # has lowercase
    r"(?=[a-zA-Z]*[A-Z])"   # has uppercase
    r"(?:"
    r"[a-z][A-Z]|[A-Z][a-z][A-Z]"  # at least one case switch
    r")"
    r"[a-zA-Z]{4,}"         # minimum 4 chars
    r"\b"
)

# Ellipsis patterns (meaningful trailing dots)
ELLIPSIS = re.compile(r"\.{2,}|…")
