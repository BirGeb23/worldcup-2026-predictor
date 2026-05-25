from datetime import datetime, timezone
import streamlit as st

_KICKOFF = datetime(2026, 6, 11, 18, 0, 0, tzinfo=timezone.utc)


def _cd_html() -> str:
    delta = _KICKOFF - datetime.now(tz=timezone.utc)
    if delta.total_seconds() <= 0:
        return (
            '<div class="countdown-bar">'
            '<span class="cd-label">⚽ The 2026 FIFA World Cup has begun!</span>'
            '</div>'
        )
    total = int(delta.total_seconds())
    days  = delta.days
    hours = (total % 86400) // 3600
    mins  = (total % 3600)  // 60
    secs  = total % 60
    return (
        '<div class="countdown-bar">'
        '<span class="cd-label">World Cup kicks off in</span>'
        '<div class="cd-units">'
        f'<div class="cd-unit"><span class="cd-num">{days}</span><span class="cd-name">days</span></div>'
        '<div class="cd-sep">·</div>'
        f'<div class="cd-unit"><span class="cd-num">{hours:02d}</span><span class="cd-name">hours</span></div>'
        '<div class="cd-sep">·</div>'
        f'<div class="cd-unit"><span class="cd-num">{mins:02d}</span><span class="cd-name">minutes</span></div>'
        '<div class="cd-sep">·</div>'
        f'<div class="cd-unit"><span class="cd-num">{secs:02d}</span><span class="cd-name">seconds</span></div>'
        '</div>'
        '</div>'
    )


@st.fragment(run_every=1)
def _live_countdown() -> None:
    st.markdown(_cd_html(), unsafe_allow_html=True)


def render_countdown() -> None:
    _live_countdown()
