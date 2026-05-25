import streamlit as st
from data.team_logos import TEAM_LOGOS
from data.qualified_teams import GROUPS


def _group_card_html(group_name: str, teams: list[str]) -> str:
    letter = group_name.split()[-1]
    rows = ""
    for team in teams:
        flag = TEAM_LOGOS.get(team, "")
        flag_img = f'<img src="{flag}" class="group-flag" />' if flag else ""
        rows += (
            f'<div class="group-team">'
            f'{flag_img}'
            f'<span class="group-team-name">{team}</span>'
            f'</div>'
        )
    return (
        f'<div class="group-card">'
        f'<div class="group-header">Group {letter}</div>'
        f'{rows}'
        f'</div>'
    )


def render_groups() -> None:
    with st.expander("🌍  2026 World Cup Groups", expanded=False):
        group_items = list(GROUPS.items())
        for row_start in range(0, len(group_items), 2):
            col_left, col_right = st.columns(2, gap="medium")
            name, teams = group_items[row_start]
            col_left.markdown(_group_card_html(name, teams), unsafe_allow_html=True)
            if row_start + 1 < len(group_items):
                name, teams = group_items[row_start + 1]
                col_right.markdown(_group_card_html(name, teams), unsafe_allow_html=True)
