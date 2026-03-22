# envc — Electronic Nonverbal Cue Detection

Detect **electronic nonverbal cues (eNVCs)** in text-based communication. Implements a taxonomy grounded in nonverbal communication theory, covering two domains:

| Domain | Subcategories |
|---|---|
| **Kinesics** | Stage directions (`*hugs*`), facial emoji, body/gesture emoji, emotion-conveying emoji, kaomoji |
| **Paralinguistics** | Vocalics (`lol`, `ugh`, `sigh`), intensity caps (`AMAZING`), intensity punctuation (`!!!`), elongation (`loooove`), alternating case (`sPoNgEbOb`), ellipsis (`...`) |

From: Kumar & Jaidka (2026). *Reading Between the Lines: How Electronic Nonverbal Cues Shape Emotion Decoding.* ICWSM.

Please cite us!
@inproceedings{kumarjaidka2026envc,
  author    = {Taara Kumar and Kokil Jaidka},
  title     = {Reading Between the Lines: How Electronic Nonverbal Cues Shape Emotion Decoding},
  booktitle = {Proceedings of the International AAAI Conference on Web and Social Media},
  year      = {2026}
}

## Python

### Install

```bash
pip install envc
# or from source:
cd python && pip install -e ".[dev]"
```

### Usage

```python
from envc import detect_envc, annotate_df

# Single text
result = detect_envc("OMG I loooove this!! 😍😍")
print(result)
# {'stage_direction': False, 'emoji_faces': True, ..., 'elongation': True, 'any_envc': True}

# Count occurrences
from envc import detect_envc_counts
counts = detect_envc_counts("😍😍😍 wow!!")
print(counts)
# {'emoji_faces': 3, 'intensity_punctuation': 1, ...}

# Annotate a DataFrame
import pandas as pd
df = pd.DataFrame({"text": ["hello!!", "AMAZING 🎉", "meh"]})
annotated = annotate_df(df)
print(annotated[["text", "any_envc"]])
```

### Run tests

```bash
cd python && pip install -e ".[dev]" && pytest
```

## R

### Install

```r
# From GitHub (requires devtools):
devtools::install_github("kokiljaidka/envc", subdir = "R")
```

### Usage

```r
library(envc)

# Single text or vector
detect_envc("OMG I loooove this!! 😍😍")
detect_envc(c("hello!!", "AMAZING 🎉", "plain text"))

# Count occurrences
detect_envc_counts("😍😍😍 wow!!")

# Annotate a data frame
df <- data.frame(text = c("hello!!", "OMG 😍", "plain"))
annotate_envc(df)
```

### Run tests

```r
devtools::test("R")
```

## Taxonomy → Regex → Output Mapping

Each detection category maps from nonverbal communication theory to a regex pattern to an output column in the results. This table mirrors Table 1 in the paper.

| Domain | Subcategory | Regex Pattern | Example Matches | Output Column |
|---|---|---|---|---|
| **Kinesics** | Body / Touch | `\*(hug\|wave\|frown\|smile\|clap)\*` | *hug*, *frowns* | `stage_direction` |
| | Facial / Eye emoji | `[\U0001F600-\U0001F64F]` | 😀 😂 😍 | `emoji_faces` |
| | Body-part emoji | `[\U0001F400-\U0001F4FF]` | 🙌 👏 💪 | `emoji_body` |
| | Emotion-conveying emoji | `[\U0001F490-\U0001F9E1]` | ❤️ ✨ 🎉 | `emoji_emotion` |
| | Kaomoji | `\([^\w\s]{1,3}[._][^\w\s]{1,3}\)` | (^.^) (T_T) | `kaomoji` |
| **Paralinguistics** | Vocalics | `\b(lol\|yawn\|ugh+\|hmmm+)\b` | lol, yawn, ughhh | `vocalics` |
| | Volume (caps) | `\b[A-Z]{2,}\b` | THIS, STOP | `intensity_caps` |
| | Volume (punctuation) | `!!+` or `\?\?+` | !!!, ??? | `intensity_punctuation` |
| | Pitch (elongation) | `(\w)\1{2,}` | soooo, noooo | `elongation` |
| | Pitch (alt. case) | `\b([A-Z][a-z]){2,}\b` | HiYa, LoL | `alternating_case` |
| | Ellipsis | `\.{3,}\|…` | ..., … | `ellipsis` |

All functions return one boolean (or count) per column. The `any_envc` column is `True` if any category fires.

## Citation

If you use this package, please cite:

```bibtex
@inproceedings{ahmed2026envc,
  title={Reading Between the Lines: How Electronic Nonverbal Cues Shape Emotion Decoding},
  author={Ahmed, Saif and Jaidka, Kokil},
  booktitle={Proceedings of the International AAAI Conference on Web and Social Media (ICWSM)},
  year={2026}
}
```

## License

MIT
