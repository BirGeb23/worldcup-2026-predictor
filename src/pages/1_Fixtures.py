import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import streamlit as st

# Add src/ to path so sibling packages resolve correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from styles import inject_css
from data.team_logos import TEAM_LOGOS
from data.fixtures_2026 import FIXTURES

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
    text-align: center; flex-shrink: 0; min-width: 68px;
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
.fx-vs-label {
    font-size: 0.52rem; font-weight: 700;
    color: rgba(255,255,255,0.2); letter-spacing: 0.12em;
    text-transform: uppercase; margin-top: 0.18rem;
}

/* ── No results ── */
.fx-empty {
    text-align: center; color: #94a3b8;
    font-size: 0.88rem; padding: 2.5rem 0;
    font-weight: 500;
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

filtered = FIXTURES

by_date: dict[str, list[dict]] = defaultdict(list)
for fx in filtered:
    by_date[fx["date"]].append(fx)

sorted_dates = sorted(by_date.keys())

# ── Render ────────────────────────────────────────────────────────────────────

def _fixture_card(fx: dict) -> str:
    home_flag = TEAM_LOGOS.get(fx["home"], "")
    away_flag = TEAM_LOGOS.get(fx["away"], "")
    home_img  = f'<img src="{home_flag}" class="fx-flag" />' if home_flag else ""
    away_img  = f'<img src="{away_flag}" class="fx-flag" />' if away_flag else ""
    return f"""
<div class="fx-card">
  <div class="fx-card-meta">
    <span>{fx["stadium"]}, {fx["city"]}</span>
    <span class="fx-meta-dot">·</span>
    <span class="fx-meta-grp">{fx["group"]}</span>
    <span class="fx-meta-dot">·</span>
    <span>Matchday {fx["matchday"]}</span>
  </div>
  <div class="fx-teams">
    <div class="fx-team-home">
      <span class="fx-team-name">{fx["home"]}</span>
      {home_img}
    </div>
    <div class="fx-center">
      <div class="fx-kickoff-time">{fx["kickoff"]}</div>
      <div class="fx-kickoff-tz">{fx["kickoff_tz"]}</div>
      <div class="fx-vs-label">vs</div>
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

        cards_html = "".join(_fixture_card(fx) for fx in by_date[date_str])
        st.markdown(cards_html, unsafe_allow_html=True)
