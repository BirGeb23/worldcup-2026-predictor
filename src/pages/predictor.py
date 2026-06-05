import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import base64
import streamlit as st

from styles import inject_css
from logic.prediction import (
    load_model, load_data, build_team_stats,
    get_h2h_winrate, get_h2h_stats, get_team_form,
    build_input_row, generate_preview,
    TOURNAMENT, FEATURE_COLS, MODEL_PATH, DATA_PATH,
)
from data.team_logos import TEAM_LOGOS
from components.countdown import render_countdown
from components.team_selector import render_team_selector
from components.strength_meter import animate_prediction_reveal

BASE_DIR    = Path(__file__).resolve().parent.parent.parent
EMBLEM_PATH = BASE_DIR / "assets" / "worldcup2026.png"


def _emblem_img_tag() -> str:
    if EMBLEM_PATH.exists():
        raw  = EMBLEM_PATH.read_bytes()
        b64  = base64.b64encode(raw).decode()
        mime = "svg+xml" if EMBLEM_PATH.suffix == ".svg" else "png"
        return (
            f'<img src="data:image/{mime};base64,{b64}" '
            f'class="hero-emblem" alt="FIFA World Cup 2026 emblem" />'
        )
    return (
        '<p style="color:#E8112D;font-size:0.72rem;text-align:center;'
        'position:relative;z-index:1;margin-bottom:14px;">'
        '[ add assets/worldcup2026.png ]</p>'
    )


render_countdown()
inject_css()

st.markdown(f"""
<div class="wc-hero">
    <div class="hero-eyebrow">FIFA World Cup™</div>
    {_emblem_img_tag()}
    <h1 class="hero-title">2026 Match Predictor</h1>
    <p class="hero-sub">USA &nbsp;·&nbsp; Canada &nbsp;·&nbsp; Mexico</p>
</div>
""", unsafe_allow_html=True)

if not MODEL_PATH.exists():
    st.error("Model not found. Run `python src/train_model.py` first.")
    st.stop()
if not DATA_PATH.exists():
    st.error("Data not found. Run `python src/preprocess.py` first.")
    st.stop()

pipeline   = load_model()
df         = load_data()
team_stats = build_team_stats(df)

render_team_selector()
home_team = st.session_state["home_team"]
away_team = st.session_state["away_team"]

st.markdown('<hr style="margin:1.25rem 0 0.85rem;">', unsafe_allow_html=True)
neutral = st.toggle("🌐 Neutral Venue", value=True)
st.markdown(
    f'<p style="font-size:0.75rem;color:#94a3b8;margin:0.2rem 0 0;">Tournament: {TOURNAMENT}</p>',
    unsafe_allow_html=True,
)

if home_team == away_team:
    st.warning("Home and away teams must be different.")
    st.stop()

predict = st.button("⚽  Predict Match Outcome", type="primary", use_container_width=True)

if predict:
    h2h       = get_h2h_winrate(df, home_team, away_team)
    h2h_data  = get_h2h_stats(df, home_team, away_team)
    home_form = get_team_form(df, home_team)
    away_form = get_team_form(df, away_team)
    X_input   = build_input_row(home_team, away_team, TOURNAMENT, neutral, team_stats, h2h)

    assert list(X_input.columns) == FEATURE_COLS, (
        f"Column mismatch!\nExpected: {FEATURE_COLS}\nGot: {list(X_input.columns)}"
    )

    prediction    = pipeline.predict(X_input)[0]
    probabilities = pipeline.predict_proba(X_input)[0]
    classes       = list(pipeline.classes_)
    prob_map      = {cls: float(p) for cls, p in zip(classes, probabilities)}

    winner_line = (
        f"{home_team} wins" if prediction == "home_win"
        else f"{away_team} wins" if prediction == "away_win"
        else "Draw"
    )

    flag_url = TEAM_LOGOS.get(home_team if prediction == "home_win" else away_team, "")
    pred_icon_html = (
        f'<img src="{flag_url}" '
        f'style="width:40px;height:auto;border-radius:5px;'
        f'box-shadow:0 3px 14px rgba(0,0,0,0.45);'
        f'display:block;margin:0 auto 0.5rem;position:relative;z-index:1;" />'
    ) if flag_url else '<div class="pred-emoji">🤝</div>'

    p_home     = prob_map.get("home_win", 0.0)
    p_draw     = prob_map.get("draw",     0.0)
    p_away     = prob_map.get("away_win", 0.0)
    h_stats    = team_stats.get(home_team, {"elo": 1500, "wr": 0.33, "gd": 0.0})
    a_stats    = team_stats.get(away_team, {"elo": 1500, "wr": 0.33, "gd": 0.0})
    elo_diff   = h_stats["elo"] - a_stats["elo"]
    form_diff  = h_stats["wr"]  - a_stats["wr"]
    adv_text   = "None" if neutral else "Active"
    adv_color  = "#94a3b8" if neutral else "#f1f5f9"
    elo_color  = "#f1f5f9" if elo_diff  >= 0 else "#E8112D"
    form_color = "#f1f5f9" if form_diff >= 0 else "#E8112D"
    preview_text = generate_preview(
        home_team, away_team, h_stats, a_stats,
        h2h_data, p_home, p_draw, p_away, neutral, prediction,
    )

    ph_flags    = st.empty()
    ph_winner   = st.empty()
    ph_probs    = st.empty()
    ph_insights = st.empty()

    animate_prediction_reveal(ph_flags, ph_winner, ph_probs, ph_insights, {
        "home_team":      home_team,
        "away_team":      away_team,
        "home_flag":      TEAM_LOGOS.get(home_team, ""),
        "away_flag":      TEAM_LOGOS.get(away_team, ""),
        "pred_icon_html": pred_icon_html,
        "winner_line":    winner_line,
        "p_home":         p_home,
        "p_draw":         p_draw,
        "p_away":         p_away,
        "elo_diff":       elo_diff,
        "form_diff":      form_diff,
        "h2h":            h2h,
        "elo_color":      elo_color,
        "form_color":     form_color,
        "adv_text":       adv_text,
        "adv_color":      adv_color,
        "h2h_data":       h2h_data,
        "home_form":      home_form,
        "away_form":      away_form,
        "preview_text":   preview_text,
    })

st.markdown("""
<div style="text-align:center; padding:2rem 0 0.5rem; border-top:1px solid #e4eaf3; margin-top:1rem;
            color:#94a3b8; font-size:0.8rem; font-weight:500; letter-spacing:0.03em;">
    2026 World Cup Edition &nbsp;·&nbsp; Version 1.0
</div>
""", unsafe_allow_html=True)
