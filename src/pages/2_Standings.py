import sys
from pathlib import Path

import streamlit as st

# Add src/ to path so sibling packages resolve correctly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from styles import inject_css
from data.team_logos import TEAM_LOGOS
from data.qualified_teams import GROUPS

inject_css()

# ── Page-specific CSS ─────────────────────────────────────────────────────────

st.markdown("""
<style>
/* ── Page hero ── */
.std-hero {
    background: linear-gradient(175deg, #06090f 0%, #0d1424 55%, #111827 100%);
    border-radius: 20px; padding: 2rem 1.5rem 1.75rem;
    margin-bottom: 1.5rem; text-align: center;
    border: 1px solid rgba(232,17,45,0.18);
    box-shadow: 0 8px 32px rgba(6,9,15,0.25);
}
.std-hero-title {
    font-size: 1.65rem; font-weight: 900; color: #fff;
    letter-spacing: -0.02em; margin: 0 0 0.3rem;
}
.std-hero-sub {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: rgba(255,255,255,0.38);
}

/* ── Group card ── */
.std-card {
    background: #fff;
    border-radius: 20px;
    padding: 1.25rem 1.4rem 1rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.07);
    border: 1px solid rgba(218,224,236,0.85);
}
.std-group-label {
    font-size: 0.58rem; font-weight: 800; letter-spacing: 0.2em;
    text-transform: uppercase; color: #E8112D;
    padding-bottom: 0.65rem; margin-bottom: 0.5rem;
    border-bottom: 1px solid rgba(218,224,236,0.85);
}

/* ── Table ── */
.std-table {
    width: 100%; border-collapse: collapse;
    font-family: 'Inter', -apple-system, sans-serif;
}
.std-table thead th {
    font-size: 0.58rem; font-weight: 700; letter-spacing: 0.09em;
    text-transform: uppercase; color: #94a3b8;
    padding: 0.2rem 0.35rem 0.45rem;
    text-align: center; border-bottom: 1px solid #f1f5f9;
}
.std-table thead th.std-th-team { text-align: left; padding-left: 0; }
.std-table tbody td {
    padding: 0.48rem 0.35rem;
    text-align: center;
    font-size: 0.82rem; font-weight: 600; color: #334155;
    border-bottom: 1px solid #f8fafc;
}
.std-table tbody tr:last-child td { border-bottom: none; }
.std-table tbody td:first-child   { text-align: left; padding-left: 0; }

/* highlight top-2 rows (qualification places) */
.std-table tbody tr:nth-child(1) td,
.std-table tbody tr:nth-child(2) td {
    background: rgba(232,17,45,0.03);
}

/* ── Team cell ── */
.std-team-cell {
    display: flex; align-items: center; gap: 0.5rem;
}
.std-flag {
    width: 26px; height: 17px; object-fit: cover;
    border-radius: 3px; box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    flex-shrink: 0;
}
.std-team-name {
    font-size: 0.82rem; font-weight: 700; color: #1e293b;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    max-width: 110px;
}

/* ── Points column ── */
.std-pts {
    font-weight: 900 !important;
    font-size: 0.9rem !important;
    color: #0f172a !important;
}

/* ── Placeholder badge ── */
.std-placeholder-note {
    font-size: 0.65rem; color: #94a3b8; font-weight: 500;
    text-align: center; margin-bottom: 1rem; letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="std-hero">
    <div class="std-hero-title">📊 2026 World Cup Standings</div>
    <div class="std-hero-sub">Group Stage &nbsp;·&nbsp; 12 Groups &nbsp;·&nbsp; 48 Nations</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="std-placeholder-note">'
    'Standings will update as group stage results come in. '
    'Top 2 teams from each group advance to the Round of 32.'
    '</p>',
    unsafe_allow_html=True,
)

# ── Standings data ────────────────────────────────────────────────────────────
# Structure: { team_name: { "p": 0, "w": 0, "d": 0, "l": 0,
#                           "gf": 0, "ga": 0, "gd": 0, "pts": 0 } }
# Replace zeros with live results to update the page.

def _initial_row() -> dict:
    return {"p": 0, "w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0, "gd": 0, "pts": 0}


def get_standings() -> dict[str, dict]:
    """Return standings dict. Update this function to pull live results."""
    return {team: _initial_row() for group_teams in GROUPS.values() for team in group_teams}


STANDINGS = get_standings()

# ── Sort logic ────────────────────────────────────────────────────────────────

def _sort_key(row: dict) -> tuple:
    """FIFA tiebreaker order: pts → gd → gf (simplified)."""
    return (row["pts"], row["gd"], row["gf"])


# ── Render helpers ────────────────────────────────────────────────────────────

def _team_cell(team: str) -> str:
    flag_url = TEAM_LOGOS.get(team, "")
    img      = f'<img src="{flag_url}" class="std-flag" />' if flag_url else ""
    return (
        f'<div class="std-team-cell">'
        f'{img}'
        f'<span class="std-team-name">{team}</span>'
        f'</div>'
    )


def _group_table(group_name: str, teams: list[str]) -> str:
    rows_html = ""
    sorted_teams = sorted(teams, key=lambda t: _sort_key(STANDINGS[t]), reverse=True)
    for team in sorted_teams:
        s = STANDINGS[team]
        gd_str = f"+{s['gd']}" if s["gd"] > 0 else str(s["gd"])
        rows_html += f"""
        <tr>
          <td>{_team_cell(team)}</td>
          <td>{s['p']}</td>
          <td>{s['w']}</td>
          <td>{s['d']}</td>
          <td>{s['l']}</td>
          <td>{s['gf']}</td>
          <td>{s['ga']}</td>
          <td>{gd_str}</td>
          <td class="std-pts">{s['pts']}</td>
        </tr>"""

    return f"""
<div class="std-card">
  <div class="std-group-label">{group_name}</div>
  <table class="std-table">
    <thead>
      <tr>
        <th class="std-th-team">Team</th>
        <th title="Played">P</th>
        <th title="Wins">W</th>
        <th title="Draws">D</th>
        <th title="Losses">L</th>
        <th title="Goals For">GF</th>
        <th title="Goals Against">GA</th>
        <th title="Goal Difference">GD</th>
        <th title="Points">PTS</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>"""


# ── Layout: 2 groups per row ──────────────────────────────────────────────────

group_items = list(GROUPS.items())

for i in range(0, len(group_items), 2):
    col_left, col_right = st.columns(2, gap="medium")
    name_l, teams_l = group_items[i]
    col_left.markdown(_group_table(name_l, teams_l), unsafe_allow_html=True)
    if i + 1 < len(group_items):
        name_r, teams_r = group_items[i + 1]
        col_right.markdown(_group_table(name_r, teams_r), unsafe_allow_html=True)
