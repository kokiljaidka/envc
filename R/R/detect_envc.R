#' @title Detect Electronic Nonverbal Cues in Text
#'
#' @description
#' Detects kinesic and paralinguistic eNVCs in text strings using
#' regex patterns aligned with nonverbal communication theory.
#'
#' Taxonomy based on Ahmed et al. (2026), ICWSM.
#'
#' @name envc-patterns
NULL

# ── Pattern definitions ──────────────────────────────────────────

# Kinesics
.p_stage_direction <- paste0(
  "\\*(",
  paste(c(
    "hug", "hugs", "wave", "waves", "thumbs up", "thumbs down",
    "facepalm", "facepalms", "heart", "hearts", "clap", "claps",
    "shrug", "shrugs", "high five", "high fives", "fist bump",
    "fist bumps", "dance", "dances", "wink", "winks", "laugh",
    "laughs", "smile", "smiles", "frown", "frowns", "cry", "cries",
    "angry", "confused", "surprised", "shocked", "kiss", "kisses",
    "blush", "blushes", "roll eyes", "rolls eyes", "nod", "nods",
    "sigh", "sighs", "scream", "screams", "gasp", "gasps",
    "pout", "pouts", "squint", "squints"
  ), collapse = "|"),
  ")\\*"
)

.p_emoji_faces <- paste0(
  "[",
  "\U0001F600-\U0001F64F",
  "\U0001F910-\U0001F96B",
  "\U0001F970-\U0001F976",
  "\U0001F97A",
  "\U0001FAE0-\U0001FAE8",
  "]"
)

.p_emoji_body <- paste0(
  "[",
  "\U0001F440-\U0001F4FF",
  "\U0001F9B0-\U0001F9BF",
  "\U0001F9D0-\U0001F9DF",
  "\U0001F90C-\U0001F90F",
  "\U0001FAF0-\U0001FAF8",
  "\U0000270A-\U0000270D",
  "\U0001F91A-\U0001F92F",
  "\U0001F930-\U0001F939",
  "]"
)

.p_emoji_emotion <- paste0(
  "[",
  "\U00002764",
  "\U0001F493-\U0001F49F",
  "\U0001F525",
  "\U00002728",
  "\U0001F4A5",
  "\U0001F4A2",
  "\U0001F4A6",
  "\U0001F4A8",
  "\U0001F389",
  "\U0001F38A",
  "\U0001F3B5-\U0001F3B6",
  "\U0001F4AB",
  "\U0001F4AF",
  "\U00002B50",
  "\U0001F31F",
  "\U0001F480",
  "\U0001F4A3",
  "\U0001F4A9",
  "\U0001F940",
  "\U0001F339",
  "\U0001F33A-\U0001F33E",
  "]"
)

.p_kaomoji <- "[\\(\\[\\{<][\\^;>T=\\-'\""][_\\.\\-\\s,oOvV]?[\\^;>T=\\-'\""][\\)\\]\\}>]"

# Paralinguistics
.p_vocalics <- paste0(
  "\\b(",
  paste(c(
    "l+o+l+", "lmao", "lmfao", "rofl",
    "ha(ha)+", "he(he)+", "hi(hi)+", "ho(ho)+",
    "baha(ha)*", "muaha(ha)*",
    "sigh", "yawn", "groan", "moan", "gasp",
    "argh+", "ugh+", "oof+", "gah+", "bah+",
    "ah+", "oh+", "eh+", "uh+", "hmm+", "huh+",
    "ooh+", "aah+", "eek+", "eep+",
    "alas", "bravo", "brr+", "doh", "geez+", "jeez+",
    "phew+", "psst+", "shh+", "shush+",
    "tsk-?tsk", "pfft+", "pff+", "meh+",
    "whee+", "whew+", "woah+", "whoa+", "wow+",
    "yoo-?hoo", "yikes+", "yay+", "yep+", "nah+", "nope+",
    "omg+", "omfg+", "wtf+", "smh+",
    "aww+", "eww+",
    "heh+", "haha", "tehe+",
    "um+", "erm+", "uhh+"
  ), collapse = "|"),
  ")\\b"
)

.p_intensity_caps <- "\\b[A-Z]{2,}\\b"

.acronym_allowlist <- c(
 "I", "A", "OK", "US", "UK", "EU", "UN", "TV", "ID", "AM", "PM",
 "HR", "IT", "AI", "ML", "NLP", "API", "URL", "CEO", "CTO",
 "PhD", "MD", "BA", "MA", "NY", "LA", "DC", "CA", "TX", "FL",
 "FBI", "CIA", "NASA", "NATO", "ADHD", "HIV", "AIDS", "DNA", "RNA",
 "USB", "PDF", "HTML", "CSS", "FAQ", "DIY", "ASAP", "FYI",
 "RSVP", "WiFi", "WIFI", "HDMI", "GPS", "ATM"
)

.p_intensity_punct <- "[!]{2,}|[?]{2,}|[!?]{2,}|[?!]{2,}"

.p_elongation <- "\\b\\w*(\\w)\\1{2,}\\w*\\b"

.p_alternating_case <- "(?=[a-zA-Z]*[a-z])(?=[a-zA-Z]*[A-Z])(?:[a-z][A-Z]|[A-Z][a-z][A-Z])[a-zA-Z]{4,}"

.p_ellipsis <- "\\.{2,}|\u2026"


# ── Helper: true caps (not acronyms) ─────────────────────────────

.has_true_caps <- function(text) {
  caps <- stringr::str_extract_all(text, .p_intensity_caps)
  vapply(caps, function(x) any(!x %in% .acronym_allowlist), logical(1))
}

.count_true_caps <- function(text) {
  caps <- stringr::str_extract_all(text, .p_intensity_caps)
  vapply(caps, function(x) sum(!x %in% .acronym_allowlist), integer(1))
}


#' Detect eNVCs in a text string
#'
#' @param text Character vector of texts to analyze.
#' @return A tibble with one row per input text and boolean columns for
#'   each eNVC subcategory, plus domain rollups and `any_envc`.
#' @export
#' @examples
#' detect_envc("OMG I loooove this!! \U0001F60D\U0001F60D")
#' detect_envc(c("hello!!", "AMAZING \U0001F389", "plain text"))
detect_envc <- function(text) {
  tibble::tibble(
    # Kinesics
    stage_direction      = stringr::str_detect(text, stringr::regex(.p_stage_direction, ignore_case = TRUE)),
    emoji_faces          = stringr::str_detect(text, .p_emoji_faces),
    emoji_body           = stringr::str_detect(text, .p_emoji_body),
    emoji_emotion        = stringr::str_detect(text, .p_emoji_emotion),
    kaomoji              = stringr::str_detect(text, .p_kaomoji),
    kinesics             = stage_direction | emoji_faces | emoji_body | emoji_emotion | kaomoji,
    # Paralinguistics
    vocalics             = stringr::str_detect(text, stringr::regex(.p_vocalics, ignore_case = TRUE)),
    intensity_caps       = .has_true_caps(text),
    intensity_punctuation = stringr::str_detect(text, .p_intensity_punct),
    elongation           = stringr::str_detect(text, .p_elongation),
    alternating_case     = stringr::str_detect(text, .p_alternating_case),
    ellipsis             = stringr::str_detect(text, .p_ellipsis),
    paralinguistics      = vocalics | intensity_caps | intensity_punctuation | elongation | alternating_case | ellipsis,
    # Overall
    any_envc             = kinesics | paralinguistics
  )
}


#' Count eNVC occurrences in text
#'
#' @param text Character vector of texts.
#' @return A tibble with integer counts per subcategory.
#' @export
detect_envc_counts <- function(text) {
  tibble::tibble(
    stage_direction       = stringr::str_count(text, stringr::regex(.p_stage_direction, ignore_case = TRUE)),
    emoji_faces           = stringr::str_count(text, .p_emoji_faces),
    emoji_body            = stringr::str_count(text, .p_emoji_body),
    emoji_emotion         = stringr::str_count(text, .p_emoji_emotion),
    kaomoji               = stringr::str_count(text, .p_kaomoji),
    vocalics              = stringr::str_count(text, stringr::regex(.p_vocalics, ignore_case = TRUE)),
    intensity_caps        = .count_true_caps(text),
    intensity_punctuation = stringr::str_count(text, .p_intensity_punct),
    elongation            = stringr::str_count(text, .p_elongation),
    alternating_case      = stringr::str_count(text, .p_alternating_case),
    ellipsis              = stringr::str_count(text, .p_ellipsis)
  )
}


#' Annotate a data frame with eNVC columns
#'
#' @param df A data frame.
#' @param text_col Name of the text column (default: "text").
#' @param counts If TRUE, return counts instead of booleans.
#' @return The input data frame with eNVC columns appended.
#' @export
annotate_envc <- function(df, text_col = "text", counts = FALSE) {
  func <- if (counts) detect_envc_counts else detect_envc
  annotations <- func(df[[text_col]])
  dplyr::bind_cols(df, annotations)
}
