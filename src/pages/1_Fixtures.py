import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import streamlit as st

# Add src/ to path so sibling packages resolve correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from styles import inject_css
from data.team_logos import TEAM_LOGOS
from data.fixtures_2026 import get_fixtures

inject_css()

# ── Page-specific CSS ─────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Page hero ── */
.fx-hero {
    background: linear-gradient(175deg, #06090f 0%, #0d1424 55%, #111827 100%);
    border-radius: 20px; padding: 2rem 1.5rem 1.75rem;
    margin-bottom: 1.5rem; text-align: center;
    border: 1px solid rgba(232,17,45,0.18);
    box-shadow: 0 8px 32px rgba(6,9,15,0.25);
}
.fx-hero-title {
    font-size: 1.65rem; font-weight: 900; color: #fff;
    letter-spacing: -0.02em; margin: 0 0 0.3rem;
}
.fx-hero-sub {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: rgba(255,255,255,0.38);
}

/* ── Date separator ── */
.fx-date-sep {
    display: flex; align-items: center; gap: 0.75rem;
    margin: 1.6rem 0 0.75rem;
}
.fx-date-label {
    font-size: 0.82rem; font-weight: 800; color: #1e293b;
    white-space: nowrap; letter-spacing: 0.01em;
}
.fx-date-rule {
    flex: 1; height: 1px;
    background: linear-gradient(90deg, #dde3ef 0%, transparent 100%);
}

/* ── Fixture card ── */
.fx-card {
    background: linear-gradient(160deg, #12182b 0%, #0d1020 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-bottom: 2px solid rgba(232,17,45,0.4);
    border-radius: 16px;
    padding: 0.9rem 1.35rem 0.8rem;
    margin-bottom: 0.55rem;
}
.fx-card-meta {
    font-size: 0.64rem; color: rgba(255,255,255,0.35);
    font-weight: 500; letter-spacing: 0.05em;
    display: flex; align-items: center; gap: 0.4rem;
    justify-content: center; margin-bottom: 0.75rem;
    flex-wrap: wrap;
}
.fx-meta-dot  { color: rgba(232,17,45,0.5); }
.fx-meta-grp  { color: #E8112D; font-weight: 700; }

.fx-teams {
    display: flex; align-items: center; gap: 0.6rem;
}
.fx-team-home {
    flex: 1; display: flex; align-items: center;
    gap: 0.65rem; justify-content: flex-end;
}
.fx-team-away {
    flex: 1; display: flex; align-items: center;
    gap: 0.65rem; justify-content: flex-start;
}
.fx-flag {
    width: 44px; height: 29px; object-fit: cover;
    border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.5);
    flex-shrink: 0;
}
.fx-team-name {
    font-size: 0.88rem; font-weight: 800; color: #f1f5f9;
    line-height: 1.2; text-align: right;
}
.fx-team-away .fx-team-name { text-align: left; }

.fx-center {
    text-align: center; flex-shrink: 0; min-width: 96px;
}
.fx-kickoff-time {
    font-size: 1.05rem; font-weight: 900; color: #fff;
    letter-spacing: 0.01em; line-height: 1;
}
.fx-kickoff-tz {
    font-size: 0.58rem; font-weight: 700;
    color: rgba(232,17,45,0.85); letter-spacing: 0.1em;
    text-transform: uppercase; margin-top: 0.15rem;
}

/* ── Split score row: digit · separator · digit ── */
.fx-split-scores {
    display: flex; align-items: center;
    justify-content: center; gap: 0.45rem;
}
.fx-score-digit {
    font-size: 1.35rem; font-weight: 900; color: #fff;
    line-height: 1; min-width: 1ch; text-align: center;
}
.fx-sep-ft {
    font-size: 0.52rem; font-weight: 700;
    color: rgba(255,255,255,0.32); letter-spacing: 0.14em;
    text-transform: uppercase;
}
.fx-live-badge {
    display: inline-block;
    font-size: 0.5rem; font-weight: 800;
    background: #E8112D; color: #fff;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 0.12rem 0.5rem; border-radius: 999px;
    animation: livePulse 1.4s ease-in-out infinite;
}
@keyframes livePulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.45; }
}

/* ── No results ── */
.fx-empty {
    text-align: center; color: #94a3b8;
    font-size: 0.88rem; padding: 2.5rem 0;
    font-weight: 500;
}

/* ── Predict button — fused to the bottom of pending fixture cards only ── */
.fx-card-pending {
    border-bottom-left-radius: 0 !important;
    border-bottom-right-radius: 0 !important;
    margin-bottom: 0 !important;
    border-bottom: 1px solid rgba(232,17,45,0.18) !important;
}
[data-testid="element-container"]:has(.fx-card-pending) {
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
}
[data-testid="element-container"]:has(.stButton) {
    margin-top: 0 !important;
    padding-top: 0 !important;
}
.stButton > button {
    background: rgba(10,13,24,0.92) !important;
    color: rgba(232,17,45,0.85) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1rem !important;
    margin-bottom: 0.8rem !important;
    transition: background 0.15s, color 0.15s !important;
}
.stButton > button:hover {
    background: rgba(232,17,45,0.14) !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="fx-hero">
    <div class="fx-hero-title">📅 2026 World Cup Fixtures</div>
    <div class="fx-hero-sub">Group Stage &nbsp;·&nbsp; 72 Matches &nbsp;·&nbsp; 11 June – 4 July 2026</div>
</div>
""", unsafe_allow_html=True)

# ── Group by date ─────────────────────────────────────────────────────────────

filtered = get_fixtures()

by_date: dict[str, list[dict]] = defaultdict(list)
for fx in filtered:
    by_date[fx["date"]].append(fx)

sorted_dates = sorted(by_date.keys())

# ── Render ────────────────────────────────────────────────────────────────────

def _center_html(fx: dict) -> str:
    status = fx.get("status", "upcoming")
    score  = fx.get("score", "")

    if status == "finished" and score:
        parts = score.split("-", 1)
        hg, ag = (parts[0], parts[1]) if len(parts) == 2 else (score, "")
        return (
            f'<div class="fx-split-scores">'
            f'<span class="fx-score-digit">{hg}</span>'
            f'<span class="fx-sep-ft">FT</span>'
            f'<span class="fx-score-digit">{ag}</span>'
            f'</div>'
        )

    if status == "live":
        parts = score.split("-", 1) if score else []
        hg = parts[0] if len(parts) == 2 else "·"
        ag = parts[1] if len(parts) == 2 else "·"
        return (
            f'<div class="fx-split-scores">'
            f'<span class="fx-score-digit">{hg}</span>'
            f'<span class="fx-live-badge">LIVE</span>'
            f'<span class="fx-score-digit">{ag}</span>'
            f'</div>'
        )

    return (
        f'<div class="fx-kickoff-time">{fx["kickoff"]}</div>'
        f'<div class="fx-kickoff-tz">{fx["kickoff_tz"]}</div>'
    )


def _fixture_card(fx: dict) -> str:
    home_flag = TEAM_LOGOS.get(fx["home"], "")
    away_flag = TEAM_LOGOS.get(fx["away"], "")
    home_img  = f'<img src="{home_flag}" class="fx-flag" />' if home_flag else ""
    away_img  = f'<img src="{away_flag}" class="fx-flag" />' if away_flag else ""
    card_class = "fx-card" if fx.get("status") == "finished" else "fx-card fx-card-pending"
    return f"""
<div class="{card_class}">
  <div class="fx-card-meta">
    <span>Matchday {fx["matchday"]}</span>
    <span class="fx-meta-dot">·</span>
    <span class="fx-meta-grp">{fx["group"]}</span>
    <span class="fx-meta-dot">·</span>
    <span>{fx["stadium"]}, {fx["city"]}</span>
  </div>
  <div class="fx-teams">
    <div class="fx-team-home">
      <span class="fx-team-name">{fx["home"]}</span>
      {home_img}
    </div>
    <div class="fx-center">
      {_center_html(fx)}
    </div>
    <div class="fx-team-away">
      {away_img}
      <span class="fx-team-name">{fx["away"]}</span>
    </div>
  </div>
</div>"""


if not sorted_dates:
    st.markdown('<div class="fx-empty">No fixtures available.</div>',
                unsafe_allow_html=True)
else:
    match_count = sum(len(by_date[d]) for d in sorted_dates)
    st.caption(f"{match_count} match{'es' if match_count != 1 else ''} shown")

    for date_str in sorted_dates:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        label = dt.strftime("%A, %d %B %Y")

        st.markdown(f"""
        <div class="fx-date-sep">
          <span class="fx-date-label">📅 {label}</span>
          <div class="fx-date-rule"></div>
        </div>""", unsafe_allow_html=True)

        for fx in by_date[date_str]:
            st.markdown(_fixture_card(fx), unsafe_allow_html=True)
            if fx.get("status") == "finished":
                pass  # score is already displayed on the card
            else:
                if st.button(
                    "⚽  Predict Outcome",
                    key=f"predict_{fx['id']}",
                    use_container_width=True,
                ):
                    st.query_params["home"] = fx["home"]
                    st.query_params["away"] = fx["away"]
                    st.query_params["go"]   = "1"
                    st.switch_page("pages/predictor.py")
