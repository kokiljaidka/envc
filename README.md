# envc — Electronic Nonverbal Cue Detection

Detect **electronic nonverbal cues (eNVCs)** in text-based communication. Implements a taxonomy grounded in nonverbal communication theory, covering two domains:

| Domain | Subcategories |
|---|---|
| **Kinesics** | Stage directions (`*hugs*`), facial emoji, body/gesture emoji, emotion-conveying emoji, kaomoji |
| **Paralinguistics** | Vocalics (`lol`, `ugh`, `sigh`), intensity caps (`AMAZING`), intensity punctuation (`!!!`), elongation (`loooove`), alternating case (`sPoNgEbOb`), ellipsis (`...`) |

Based on: Ahmed et al. (2026). *Reading Between the Lines: How Electronic Nonverbal Cues Shape Emotion Decoding.* ICWSM.

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
devtools::install_github("YOURUSER/envc", subdir = "R")
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

## Taxonomy

The detection categories map directly to the eNVC taxonomy in the paper:

### Kinesics (textual body language)
- **Stage directions**: `*hugs*`, `*cries*`, `*facepalm*`
- **Facial emoji**: 😊 😢 😍 🤔
- **Body/gesture emoji**: 👍 🤝 👋 🙏
- **Emotion-conveying emoji**: ❤️ ✨ 🔥 🎉
- **Kaomoji**: `(^.^)` `(T_T)` `(>_<)`

### Paralinguistics (digital prosody)
- **Vocalics**: `lol`, `ugh`, `sigh`, `omg`, `haha`
- **Intensity (caps)**: `AMAZING`, `YES` (excludes common acronyms like NASA, IT)
- **Intensity (punctuation)**: `!!`, `???`, `?!?!`
- **Elongation**: `loooove`, `nooooo`, `sooooo`
- **Alternating case**: `sPoNgEbOb` style
- **Ellipsis**: `...`, `…`

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
