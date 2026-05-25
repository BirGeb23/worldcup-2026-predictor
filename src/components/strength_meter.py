import time
import streamlit as st
from data.world_rankings import KEY_PLAYERS
from logic.prediction import TOURNAMENT


def animate_prediction_reveal(
    ph_flags, ph_winner, ph_probs, ph_insights, ctx: dict
) -> None:
    """Sequentially reveals prediction cards via st.empty() placeholders."""
    ht = ctx["home_team"];  at = ctx["away_team"]
    hf = ctx["home_flag"];  af = ctx["away_flag"]
    p_home     = ctx["p_home"];   p_draw = ctx["p_draw"];  p_away = ctx["p_away"]
    elo_diff   = ctx["elo_diff"]; form_diff = ctx["form_diff"]
    h2h_val    = ctx["h2h"]
    elo_color  = ctx["elo_color"];  form_color = ctx["form_color"]
    adv_color  = ctx["adv_color"];  adv_text   = ctx["adv_text"]
    h2h_data   = ctx["h2h_data"]
    home_form  = ctx["home_form"];  away_form  = ctx["away_form"]
    preview_text = ctx["preview_text"]

    # Step 1: Both team flags slide in from opposite sides
    ph_flags.markdown(f"""
    <div class="reveal-flags">
        <div class="reveal-flag reveal-flag-home">
            <img src="{hf}" alt="{ht}" />
            <span class="reveal-flag-name">{ht}</span>
        </div>
        <div class="reveal-vs-badge">
            <div class="vs-circle"><span>VS</span></div>
        </div>
        <div class="reveal-flag reveal-flag-away">
            <img src="{af}" alt="{at}" />
            <span class="reveal-flag-name">{at}</span>
        </div>
    </div>""", unsafe_allow_html=True)
    time.sleep(0.28)

    # Step 2: Winner announcement fades in
    ph_winner.markdown(f"""
    <div class="pred-hero anim-pred-reveal">
        {ctx["pred_icon_html"]}
        <div class="pred-title">{ctx["winner_line"]}</div>
        <div class="pred-sub">{ht} &nbsp;·&nbsp; {TOURNAMENT} &nbsp;·&nbsp; {at}</div>
    </div>""", unsafe_allow_html=True)
    time.sleep(0.22)

    # Step 3: Probability bars + insights grid
    ph_probs.markdown(f"""
    <div class="wc-card anim-fade-up">
        <span class="wc-card-label">📊 Win Probabilities</span>
        <div class="prob-row">
            <span class="prob-label">🏠 {ht}</span>
            <div class="prob-track"><div class="prob-fill prob-home" style="width:{p_home*100:.1f}%"></div></div>
            <span class="prob-pct">{p_home:.0%}</span>
        </div>
        <div class="prob-row">
            <span class="prob-label">🤝 Draw</span>
            <div class="prob-track"><div class="prob-fill prob-draw" style="width:{p_draw*100:.1f}%"></div></div>
            <span class="prob-pct">{p_draw:.0%}</span>
        </div>
        <div class="prob-row">
            <span class="prob-label">✈️ {at}</span>
            <div class="prob-track"><div class="prob-fill prob-away" style="width:{p_away*100:.1f}%"></div></div>
            <span class="prob-pct">{p_away:.0%}</span>
        </div>
    </div>
    <div class="wc-card anim-fade-up anim-d1">
        <span class="wc-card-label">🔍 Match Insights</span>
        <div class="insight-grid">
            <div class="insight-cell">
                <div class="insight-value" style="color:{elo_color};">{elo_diff:+.0f}</div>
                <div class="insight-label">Elo Edge</div>
            </div>
            <div class="insight-cell">
                <div class="insight-value" style="color:{form_color};">{form_diff:+.0%}</div>
                <div class="insight-label">Form Edge</div>
            </div>
            <div class="insight-cell">
                <div class="insight-value">{h2h_val:.0%}</div>
                <div class="insight-label">H2H Win Rate</div>
            </div>
            <div class="insight-cell">
                <div class="insight-value" style="color:{adv_color};">{adv_text}</div>
                <div class="insight-label">Home Advantage</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    time.sleep(0.18)

    # Step 4: H2H history, form, key players, match preview
    total  = h2h_data["total"]
    hw_cnt = h2h_data["home_wins"]
    d_cnt  = h2h_data["draws"]
    aw_cnt = h2h_data["away_wins"]

    if h2h_data["last5"]:
        rows = ""
        for m in h2h_data["last5"]:
            bc = {"W": "badge-w", "D": "badge-d", "L": "badge-l"}[m["result"]]
            bt = {"W": "WIN",     "D": "DRAW",    "L": "LOSS"}[m["result"]]
            rows += (
                f'<div class="meeting-row">'
                f'<span class="meeting-date">{m["date"]}</span>'
                f'<span class="meeting-score">{m["score"]}</span>'
                f'<span class="meeting-badge {bc}">{bt}</span>'
                f'</div>'
            )
        last5_html = (
            f'<div class="meetings-list">'
            f'<div class="meetings-title">Last {len(h2h_data["last5"])} meetings</div>'
            f'{rows}</div>'
        )
    else:
        last5_html = (
            '<p style="color:#94a3b8;font-size:0.82rem;text-align:center;padding:0.5rem 0;">'
            'No head-to-head records found.</p>'
        )

    no_h2h = (
        "" if total > 0
        else '<p style="color:#94a3b8;font-size:0.82rem;text-align:center;">'
             'First ever meeting between these sides.</p>'
    )

    def _dots(form: list[str]) -> str:
        if not form:
            return '<span style="color:#94a3b8;font-size:0.8rem;">No data</span>'
        cls_map = {"W": "dot-w", "D": "dot-d", "L": "dot-l"}
        return "".join(f'<span class="dot {cls_map[r]}">{r}</span>' for r in form)

    def _players_html(team: str) -> str:
        players = KEY_PLAYERS.get(team, [f"Player {i}" for i in range(1, 6)])
        return "".join(
            f'<div class="player-item"><span class="player-num">{i}</span>'
            f'<span class="player-name">{p}</span></div>'
            for i, p in enumerate(players, 1)
        )

    ph_insights.markdown(f"""
    <div class="wc-card anim-fade-up">
        <span class="wc-card-label">⚔️ Head-to-Head History</span>
        <div class="h2h-breakdown">
            <div class="h2h-team-block">
                <div class="h2h-team-name">{ht}</div>
                <div class="h2h-count-big" style="color:#1e293b;">{hw_cnt}</div>
                <div class="h2h-count-label">Wins</div>
            </div>
            <div class="h2h-divider"></div>
            <div class="h2h-team-block">
                <div class="h2h-team-name">Draws</div>
                <div class="h2h-count-big" style="color:#94a3b8;">{d_cnt}</div>
                <div class="h2h-count-label">from {total} matches</div>
            </div>
            <div class="h2h-divider"></div>
            <div class="h2h-team-block">
                <div class="h2h-team-name">{at}</div>
                <div class="h2h-count-big" style="color:var(--red);">{aw_cnt}</div>
                <div class="h2h-count-label">Wins</div>
            </div>
        </div>
        {no_h2h}{last5_html}
    </div>
    <div class="wc-card anim-fade-up anim-d1">
        <span class="wc-card-label">📈 Recent Form — Last 5 Matches</span>
        <div class="form-section">
            <div class="form-team-row">
                <span class="form-team-label">{ht}</span>
                <div class="form-dots">{_dots(home_form)}</div>
            </div>
            <div class="form-team-row">
                <span class="form-team-label">{at}</span>
                <div class="form-dots">{_dots(away_form)}</div>
            </div>
        </div>
    </div>
    <div class="wc-card anim-fade-up anim-d2">
        <span class="wc-card-label">⭐ Key Players</span>
        <div class="players-grid">
            <div>
                <div class="players-col-title">{ht}</div>
                {_players_html(ht)}
            </div>
            <div>
                <div class="players-col-title">{at}</div>
                {_players_html(at)}
            </div>
        </div>
    </div>
    <div class="wc-card anim-fade-up anim-d3">
        <span class="wc-card-label">📝 Match Preview</span>
        <div class="preview-box">{preview_text}</div>
    </div>""", unsafe_allow_html=True)
