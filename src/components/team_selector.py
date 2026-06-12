import streamlit as st
from data.team_logos import TEAM_LOGOS
from data.qualified_teams import QUALIFIED_2026


@st.dialog("🌍  Select a Nation", width="large")
def nation_picker_modal(team_key: str) -> None:
    st.markdown("""
    <style>
    .nation-flag-wrap {
        text-align: center;
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
        border-bottom: none;
        border-radius: 12px 12px 0 0;
        padding: 0.55rem 0.4rem 0.3rem;
    }
    .nation-flag-wrap img {
        width: 80px; height: 54px;
        object-fit: cover;
        border-radius: 4px;
        display: block; margin: 0 auto;
        box-shadow: 0 2px 6px rgba(0,0,0,0.18);
    }
    [data-testid="stMarkdownContainer"]:has(.nation-flag-wrap) {
        margin-bottom: -8px !important;
    }
    [data-testid="stMarkdownContainer"]:has(.nation-flag-wrap)
      + [data-testid="stButton"] button {
        border-radius: 0 0 12px 12px !important;
        border-top: none !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        white-space: normal !important;
        line-height: 1.3 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "search", placeholder="Search nations…",
        label_visibility="collapsed", key=f"modal_search_{team_key}",
    )
    teams = (
        [t for t in QUALIFIED_2026 if query.lower() in t.lower()]
        if query else QUALIFIED_2026
    )
    if not teams:
        st.caption("No nations match your search.")
        return

    current = st.session_state.get(team_key, "")

    for i in range(0, len(teams), 4):
        chunk = teams[i:i+4]
        cols = st.columns(4, gap="small")
        for j, team in enumerate(chunk):
            with cols[j]:
                flag_url = TEAM_LOGOS.get(team, "")
                st.markdown(
                    f'<div class="nation-flag-wrap">'
                    f'<img src="{flag_url}" alt="{team}" />'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    team,
                    key=f"nation_{team_key}_{team}",
                    use_container_width=True,
                    type="primary" if team == current else "secondary",
                ):
                    st.session_state[team_key] = team
                    st.rerun()


def render_team_selector() -> None:
    """Renders the HOME / AWAY team cards with browse buttons.

    Reads and writes st.session_state["home_team"] and st.session_state["away_team"].
    Call st.session_state["home_team"] / ["away_team"] after this to get the selections.
    """
    if "team1" not in st.session_state:
        st.session_state["team1"] = "Brazil"
    if "team2" not in st.session_state:
        st.session_state["team2"] = "Argentina"

    st.markdown('<span class="wc-card-label">⚽ Select Teams</span>', unsafe_allow_html=True)

    c_home, c_vs, c_away = st.columns([10, 3, 10])

    with c_home:
        home_team = st.session_state["team1"]
        home_flag = TEAM_LOGOS.get(home_team, "")
        st.markdown('<p class="team-slot-label">HOME</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="team-crest">
            <img src="{home_flag}" alt="{home_team}" />
            <div class="crest-name">{home_team}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔍  Browse all nations", key="browse_home", use_container_width=True):
            nation_picker_modal("team1")

    with c_vs:
        st.markdown("""
        <div class="vs-col">
            <div class="vs-line-top"></div>
            <div class="vs-circle"><span>VS</span></div>
            <div class="vs-line-bot"></div>
        </div>""", unsafe_allow_html=True)

    with c_away:
        away_team = st.session_state["team2"]
        away_flag = TEAM_LOGOS.get(away_team, "")
        st.markdown('<p class="team-slot-label">AWAY</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="team-crest">
            <img src="{away_flag}" alt="{away_team}" />
            <div class="crest-name">{away_team}</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔍  Browse all nations", key="browse_away", use_container_width=True):
            nation_picker_modal("team2")
