"""
Core detection functions for electronic nonverbal cues (eNVCs).

Usage:
    from envc import detect_envc, annotate_df

    # Single text
    result = detect_envc("OMG I loooove this!! 😍😍")
    print(result)

    # DataFrame
    import pandas as pd
    df = pd.DataFrame({"text": ["hello!!", "AMAZING 🎉", "meh"]})
    annotated = annotate_df(df, text_col="text")
"""

from __future__ import annotations

import re
from typing import Optional

from .patterns import (
    ALTERNATING_CASE,
    ELLIPSIS,
    ELONGATION,
    EMOJI_BODY,
    EMOJI_EMOTION,
    EMOJI_FACES,
    INTENSITY_CAPS,
    INTENSITY_PUNCTUATION,
    KAOMOJI,
    STAGE_DIRECTION,
    VOCALICS,
    _ACRONYM_ALLOWLIST,
)


def _has_true_caps(text: str) -> bool:
    """Return True if text contains ALL-CAPS words that aren't common acronyms."""
    for match in INTENSITY_CAPS.finditer(text):
        word = match.group()
        if word not in _ACRONYM_ALLOWLIST:
            return True
    return False


def detect_envc(text: str) -> dict:
    """
    Detect electronic nonverbal cues in a single text string.

    Parameters
    ----------
    text : str
        The input text (e.g., a tweet or microblog post).

    Returns
    -------
    dict
        Boolean flags for each eNVC subcategory, plus domain-level
        rollups (``kinesics``, ``paralinguistics``, ``any_envc``).

    Example
    -------
    >>> detect_envc("I loooove this!! 😍😍 *hugs*")
    {'stage_direction': True, 'emoji_faces': True, 'emoji_body': False,
     'emoji_emotion': False, 'kaomoji': False, 'kinesics': True,
     'vocalics': False, 'intensity_caps': False,
     'intensity_punctuation': True, 'elongation': True,
     'alternating_case': False, 'ellipsis': False,
     'paralinguistics': True, 'any_envc': True}
    """
    # ── Kinesics ──
    stage_direction = bool(STAGE_DIRECTION.search(text))
    emoji_faces = bool(EMOJI_FACES.search(text))
    emoji_body = bool(EMOJI_BODY.search(text))
    emoji_emotion = bool(EMOJI_EMOTION.search(text))
    kaomoji = bool(KAOMOJI.search(text))

    kinesics = any([stage_direction, emoji_faces, emoji_body,
                    emoji_emotion, kaomoji])

    # ── Paralinguistics ──
    vocalics = bool(VOCALICS.search(text))
    intensity_caps = _has_true_caps(text)
    intensity_punctuation = bool(INTENSITY_PUNCTUATION.search(text))
    elongation = bool(ELONGATION.search(text))
    alt_case = bool(ALTERNATING_CASE.search(text))
    ellipsis = bool(ELLIPSIS.search(text))

    paralinguistics = any([vocalics, intensity_caps, intensity_punctuation,
                           elongation, alt_case, ellipsis])

    return {
        # Kinesics subcategories
        "stage_direction": stage_direction,
        "emoji_faces": emoji_faces,
        "emoji_body": emoji_body,
        "emoji_emotion": emoji_emotion,
        "kaomoji": kaomoji,
        "kinesics": kinesics,
        # Paralinguistics subcategories
        "vocalics": vocalics,
        "intensity_caps": intensity_caps,
        "intensity_punctuation": intensity_punctuation,
        "elongation": elongation,
        "alternating_case": alt_case,
        "ellipsis": ellipsis,
        "paralinguistics": paralinguistics,
        # Overall
        "any_envc": kinesics or paralinguistics,
    }


def detect_envc_counts(text: str) -> dict:
    """
    Count occurrences of each eNVC subcategory in a text.

    Returns
    -------
    dict
        Integer counts for each subcategory.
    """
    return {
        "stage_direction": len(STAGE_DIRECTION.findall(text)),
        "emoji_faces": len(EMOJI_FACES.findall(text)),
        "emoji_body": len(EMOJI_BODY.findall(text)),
        "emoji_emotion": len(EMOJI_EMOTION.findall(text)),
        "kaomoji": len(KAOMOJI.findall(text)),
        "vocalics": len(VOCALICS.findall(text)),
        "intensity_caps": len([m for m in INTENSITY_CAPS.finditer(text)
                               if m.group() not in _ACRONYM_ALLOWLIST]),
        "intensity_punctuation": len(INTENSITY_PUNCTUATION.findall(text)),
        "elongation": len(ELONGATION.findall(text)),
        "alternating_case": len(ALTERNATING_CASE.findall(text)),
        "ellipsis": len(ELLIPSIS.findall(text)),
    }


def annotate_df(df, text_col: str = "text", counts: bool = False):
    """
    Add eNVC annotation columns to a pandas DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    text_col : str
        Name of the column containing text to analyze.
    counts : bool
        If True, return integer counts instead of boolean flags.

    Returns
    -------
    pandas.DataFrame
        Copy of ``df`` with eNVC columns appended.
    """
    import pandas as pd

    func = detect_envc_counts if counts else detect_envc
    annotations = df[text_col].apply(func).apply(pd.Series)
    return pd.concat([df, annotations], axis=1)
