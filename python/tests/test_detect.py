"""Tests for envc.detect."""

import pytest
from envc import detect_envc, detect_envc_counts


# ── Kinesics ──

def test_stage_direction():
    assert detect_envc("*hugs* you're the best")["stage_direction"] is True
    assert detect_envc("hello there")["stage_direction"] is False


def test_emoji_faces():
    assert detect_envc("love this 😊")["emoji_faces"] is True
    assert detect_envc("love this")["emoji_faces"] is False


def test_emoji_body():
    assert detect_envc("good job 👍")["emoji_body"] is True


def test_emoji_emotion():
    assert detect_envc("amazing ❤️✨")["emoji_emotion"] is True
    assert detect_envc("amazing")["emoji_emotion"] is False


def test_kaomoji():
    assert detect_envc("hi (^.^)")["kaomoji"] is True
    assert detect_envc("hi there")["kaomoji"] is False


def test_kinesics_rollup():
    result = detect_envc("*waves* hello 😊")
    assert result["kinesics"] is True
    assert detect_envc("plain text")["kinesics"] is False


# ── Paralinguistics ──

def test_vocalics_lol():
    assert detect_envc("lol that's funny")["vocalics"] is True


def test_vocalics_interjection():
    assert detect_envc("ugh not again")["vocalics"] is True
    assert detect_envc("sigh...")["vocalics"] is True


def test_vocalics_omg():
    assert detect_envc("omg really")["vocalics"] is True


def test_intensity_caps():
    assert detect_envc("THIS IS AMAZING")["intensity_caps"] is True
    # Common acronyms should NOT trigger
    assert detect_envc("I work in IT at NASA")["intensity_caps"] is False


def test_intensity_punctuation():
    assert detect_envc("what!! no way!!")["intensity_punctuation"] is True
    assert detect_envc("oh???")["intensity_punctuation"] is True
    assert detect_envc("hello.")["intensity_punctuation"] is False


def test_elongation():
    assert detect_envc("I loooove this")["elongation"] is True
    assert detect_envc("nooooo")["elongation"] is True
    assert detect_envc("I love this")["elongation"] is False


def test_alternating_case():
    assert detect_envc("sPoNgEbOb")["alternating_case"] is True


def test_ellipsis():
    assert detect_envc("well... okay")["ellipsis"] is True
    assert detect_envc("well okay")["ellipsis"] is False


def test_paralinguistics_rollup():
    result = detect_envc("YESSS!!! omg")
    assert result["paralinguistics"] is True
    assert detect_envc("okay sure")["paralinguistics"] is False


# ── Overall ──

def test_any_envc():
    assert detect_envc("loooool 😂🔥")["any_envc"] is True
    assert detect_envc("The meeting is at 3pm.")["any_envc"] is False


def test_plain_text_all_false():
    result = detect_envc("The meeting is at 3pm.")
    assert not any(v for v in result.values())


# ── Counts ──

def test_counts_emoji():
    result = detect_envc_counts("😍😍😍 love it")
    assert result["emoji_faces"] == 3


def test_counts_punctuation():
    result = detect_envc_counts("what!! no!!! really????")
    assert result["intensity_punctuation"] >= 2


# ── Paper examples ──

def test_paper_friday():
    text = "Today is Friday!!!!!!! thannkkkk gooood"
    r = detect_envc(text)
    assert r["intensity_punctuation"] is True
    assert r["elongation"] is True


def test_paper_exams():
    text = "EXAAAAAAAAAMS 😢"
    r = detect_envc(text)
    assert r["intensity_caps"] is True
    assert r["elongation"] is True
    assert r["emoji_faces"] is True


def test_paper_damn():
    text = "Just finished reading Fahrenheit 451... DAMN... I really enjoyed it 👌"
    r = detect_envc(text)
    assert r["intensity_caps"] is True
    assert r["ellipsis"] is True
    assert r["emoji_body"] is True


def test_paper_tired():
    text = "Oh I am soo tiiiired ughh wow..."
    r = detect_envc(text)
    assert r["elongation"] is True
    assert r["vocalics"] is True
    assert r["ellipsis"] is True


# ── DataFrame ──

def test_annotate_df():
    pd = pytest.importorskip("pandas")
    from envc import annotate_df

    df = pd.DataFrame({"text": ["hello!!", "OMG 😍", "plain"]})
    result = annotate_df(df)
    assert "any_envc" in result.columns
    assert result.loc[0, "intensity_punctuation"] is True
    assert result.loc[2, "any_envc"] is False


def test_annotate_df_counts():
    pd = pytest.importorskip("pandas")
    from envc import annotate_df

    df = pd.DataFrame({"text": ["😍😍😍 wow!!"]})
    result = annotate_df(df, counts=True)
    assert result.loc[0, "emoji_faces"] == 3
