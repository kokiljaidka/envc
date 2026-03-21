"""
envc — Detect Electronic Nonverbal Cues in text.

Taxonomy based on:
  Ahmed et al. (2026). Reading Between the Lines: How Electronic
  Nonverbal Cues Shape Emotion Decoding. ICWSM.

Quick start:
    >>> from envc import detect_envc, annotate_df
    >>> detect_envc("OMG I loooove this!! 😍😍")
"""

__version__ = "0.1.0"

from .detect import annotate_df, detect_envc, detect_envc_counts

__all__ = ["detect_envc", "detect_envc_counts", "annotate_df"]
