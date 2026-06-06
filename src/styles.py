import streamlit as st
import streamlit.components.v1 as components

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,800&display=swap');

:root {
    --red:    #E8112D;
    --black:  #06090f;
    --silver: #94a3b8;
    --card:   #ffffff;
    --border: rgba(218,224,236,0.85);
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background:
        radial-gradient(ellipse 110% 55% at 50% -8%, rgba(255,255,255,0.90) 0%, transparent 100%),
        radial-gradient(ellipse 50% 30% at 95% 85%, rgba(232,17,45,0.06)    0%, transparent 55%),
        radial-gradient(ellipse 40% 25% at 50% 110%, rgba(0,0,0,0.05)       0%, transparent 55%),
        linear-gradient(180deg, #edf0f8 0%, #f2f4f9 100%) !important;
}

/* Hide Streamlit chrome */
#MainMenu { display: none !important; }
footer    { display: none !important; }
[data-testid="stDeployButton"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stDecoration"]   { display: none !important; }

/* Remove Streamlit's header bar — countdown bar is the only top bar */
header[data-testid="stHeader"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    height: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
}

/* Page content — top padding clears the ~3.75rem absolute Streamlit header */
.block-container {
    max-width: 780px !important;
    padding: 4.5rem 1.25rem 4rem 1.25rem !important;
}

/* ═══════════════════════ HERO BANNER ═══════════════════════ */
.wc-hero {
    background:
        radial-gradient(ellipse 90% 60% at 50% -10%, rgba(255,255,255,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 45% 35% at 90%  85%, rgba(232,17,45,0.16)   0%, transparent 55%),
        linear-gradient(175deg, #06090f 0%, #0d1424 55%, #111827 100%);
    border-radius: 24px;
    padding: 3rem 2rem 2.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 1.75rem;
    box-shadow: 0 12px 48px rgba(6,9,15,0.35), 0 2px 8px rgba(6,9,15,0.2);
}
.wc-hero::before {
    content: '';
    position: absolute; top: -50%; left: 50%;
    transform: translateX(-50%);
    width: 160%; height: 120%;
    background: radial-gradient(ellipse at 50% 0%,
        rgba(255,255,255,0.11) 0%,
        rgba(255,255,255,0.04) 30%,
        transparent 65%);
    pointer-events: none;
}
.wc-hero::after {
    content: '';
    position: absolute; bottom: 0; left: 10%; right: 10%; height: 2px;
    background: linear-gradient(90deg, transparent, var(--red) 30%, var(--red) 70%, transparent);
    opacity: 0.7;
}
.hero-eyebrow {
    font-size: 0.64rem; font-weight: 700; letter-spacing: 0.22em;
    text-transform: uppercase; color: rgba(255,255,255,0.38);
    margin-bottom: 0.55rem; position: relative; z-index: 1;
}
.hero-emblem {
    display: block; margin: 0 auto 18px; width: 185px; height: auto;
    position: relative; z-index: 1;
}
.hero-title {
    font-size: 2.4rem; font-weight: 900; color: #ffffff !important;
    letter-spacing: -0.03em; line-height: 1.08;
    margin: 0 0 8px; position: relative; z-index: 1;
}
.hero-sub {
    font-size: 0.82rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: #d4d4d8 !important;
    margin: 0; position: relative; z-index: 1;
}

/* ═══════════════════════ CARDS ═══════════════════════ */
.wc-card {
    background: var(--card);
    border-radius: 20px;
    padding: 1.75rem;
    margin: 0 0 1.25rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.07);
    border: 1px solid var(--border);
}
.wc-card-label {
    display: block; font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #94a3b8; margin-bottom: 1.1rem;
}

/* ═══════════════════════ TEAM CREST ═══════════════════════ */
.team-crest {
    background: linear-gradient(160deg, #f8fafc 0%, #edf0f7 100%);
    border-radius: 20px;
    padding: 1.4rem 1rem 1.2rem;
    text-align: center;
    border: 1px solid #dde3ef;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05), 0 6px 20px rgba(0,0,0,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.team-crest:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(0,0,0,0.12); }
.team-crest img {
    border-radius: 7px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.22);
    display: block; margin: 0 auto 0.8rem;
    width: 96px; height: auto;
}
.crest-name {
    font-size: 0.92rem; font-weight: 800; color: #0f172a;
    margin-bottom: 0.35rem; line-height: 1.2;
}
.crest-elo {
    display: inline-block;
    background: var(--black); color: #ffffff;
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.09em;
    padding: 0.18rem 0.55rem; border-radius: 999px;
}

/* ═══════════════════════ VS BADGE ═══════════════════════ */
.vs-col {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 200px; gap: 0.45rem;
}
.vs-line-top, .vs-line-bot {
    width: 1px; flex: 1; max-height: 44px;
    background: linear-gradient(180deg, transparent, #d1d9e6);
}
.vs-line-bot { background: linear-gradient(180deg, #d1d9e6, transparent); }
.vs-circle {
    width: 50px; height: 50px;
    background: linear-gradient(135deg, var(--red) 0%, #9b0e1c 100%);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 18px rgba(232,17,45,0.45);
    flex-shrink: 0;
}
.vs-circle span {
    font-size: 0.78rem; font-weight: 900; color: #fff; letter-spacing: 0.04em;
}

/* ═══════════════════════ BUTTON ═══════════════════════ */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--red) 0%, #9b0e1c 100%) !important;
    color: #fff !important; border: none !important;
    border-radius: 14px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important; font-weight: 800 !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    padding: 0.8rem 0 !important;
    box-shadow: 0 4px 20px rgba(232,17,45,0.32) !important;
    transition: transform 0.16s ease, box-shadow 0.16s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(232,17,45,0.48) !important;
}
.stButton > button[kind="primary"]:active { transform: translateY(0) !important; }

/* ═══════════════════════ COUNTDOWN BAR ═══════════════════════ */
/* ── Countdown pinned to the top navbar ── */
.countdown-bar {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999999;
    height: 3.25rem;
    display: flex; align-items: center; justify-content: center;
    gap: 1rem; flex-wrap: nowrap;
    background: linear-gradient(135deg, #06090f 0%, #0d1424 100%);
    border-bottom: 1px solid rgba(232,17,45,0.28);
    border-radius: 0;
    padding: 0 1.5rem;
    margin-bottom: 0;
    box-shadow: 0 2px 12px rgba(6,9,15,0.22);
}
.cd-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.11em;
    text-transform: uppercase; color: rgba(255,255,255,0.45);
    white-space: nowrap;
}
.cd-units { display: flex; align-items: center; gap: 0.35rem; }
.cd-unit  { display: flex; flex-direction: column; align-items: center; min-width: 36px; }
.cd-num   {
    font-size: 1.2rem; font-weight: 900; color: #ffffff;
    line-height: 1; letter-spacing: -0.02em;
}
.cd-name  {
    font-size: 0.48rem; font-weight: 700; letter-spacing: 0.11em;
    text-transform: uppercase; color: rgba(255,255,255,0.38);
    margin-top: 0.08rem;
}
.cd-sep   {
    font-size: 1rem; font-weight: 900; color: var(--red);
    line-height: 1; margin-bottom: 0.45rem; align-self: flex-start; padding-top: 0.05rem;
}

/* Push sidebar content below the fixed countdown bar */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 3.25rem !important;
}

/* Hide native sidebar toggle buttons — custom JS button handles toggling */
[data-testid="stSidebarCollapseButton"],
[data-testid="stExpandSidebarButton"] {
    display: none !important;
}

/* ═══════════════════════ TEAM SLOT LABELS ═══════════════════════ */
.team-slot-label {
    font-size: 0.65rem; font-weight: 800;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: #64748b; text-align: center;
    margin: 0 0 0.45rem; line-height: 1;
}

/* ═══════════════════════ SELECTBOX / TOGGLE ═══════════════════════ */
.stSelectbox > label {
    font-size: 0.72rem !important; font-weight: 700 !important;
    letter-spacing: 0.11em !important; text-transform: uppercase !important;
    color: #64748b !important;
}
.stSelectbox [data-baseweb="select"] > div:first-child {
    border-radius: 11px !important; border-color: #dde3ef !important;
    background: #f8fafc !important;
    font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
}
.stToggle > label { font-weight: 600 !important; color: #1e293b !important; }

hr { border: none !important; border-top: 1px solid #e4eaf3 !important; margin: 1rem 0 !important; }

/* ═══════════════════════ PREDICTION HERO ═══════════════════════ */
.pred-hero {
    background:
        radial-gradient(ellipse 80% 50% at 50% -5%, rgba(232,17,45,0.18) 0%, transparent 65%),
        linear-gradient(175deg, #06090f 0%, #0e1525 60%, #111224 100%);
    border-radius: 20px; padding: 2.5rem 2rem;
    text-align: center; position: relative; overflow: hidden;
    border: 1px solid rgba(232,17,45,0.18);
    box-shadow: 0 10px 44px rgba(6,9,15,0.28), 0 0 0 1px rgba(255,255,255,0.04);
}
.pred-hero::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent, var(--red) 40%, var(--red) 60%, transparent);
}
.pred-emoji  { font-size: 4.2rem; line-height: 1; margin-bottom: 0.5rem; position: relative; z-index: 1; }
.pred-title  {
    color: #f8fafc; font-size: 1.85rem; font-weight: 900;
    letter-spacing: -0.02em; margin: 0.25rem 0;
    position: relative; z-index: 1;
}
.pred-sub { color: rgba(255,255,255,0.38); font-size: 0.9rem; position: relative; z-index: 1; }

/* ═══════════════════════ PROB BARS ═══════════════════════ */
.prob-row   { display: flex; align-items: center; gap: 0.85rem; margin: 0.75rem 0; }
.prob-label { min-width: 158px; font-size: 0.87rem; font-weight: 700; color: #1e293b; }
.prob-track { flex: 1; height: 11px; background: #edf0f7; border-radius: 999px; overflow: hidden; }
.prob-fill  { height: 100%; border-radius: 999px; animation: barFill 0.9s cubic-bezier(0.22,1,0.36,1) both; }
.prob-home  { background: linear-gradient(90deg, #1e293b, #475569); }
.prob-draw  { background: linear-gradient(90deg, #94a3b8, #64748b); }
.prob-away  { background: linear-gradient(90deg, var(--red), #9b0e1c); }
.prob-pct   { min-width: 3rem; text-align: right; font-size: 0.9rem; font-weight: 800; color: #0f172a; }

/* ═══════════════════════ INSIGHT GRID ═══════════════════════ */
.insight-grid {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 0.9rem; margin-top: 0.25rem;
}
@media (max-width:600px) { .insight-grid { grid-template-columns: repeat(2,1fr); } }

.insight-cell {
    background: linear-gradient(160deg,#f8fafc,#edf0f7);
    border-radius: 16px; padding: 1rem 0.7rem; text-align: center;
    border: 1px solid #dde3ef;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05), 0 4px 14px rgba(0,0,0,0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.insight-cell:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.10); }
.insight-value { font-size: 1.35rem; font-weight: 900; color: #0f172a; line-height: 1.2; }
.insight-label {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.09em;
    text-transform: uppercase; color: #94a3b8; margin-top: 0.3rem;
}

/* ═══════════════════════ ANIMATIONS ═══════════════════════ */
@keyframes fadeInUp   { from { opacity:0; transform:translateY(26px); }           to { opacity:1; transform:translateY(0); } }
@keyframes predReveal { from { opacity:0; transform:translateY(28px) scale(0.96);} to { opacity:1; transform:translateY(0)  scale(1); } }
@keyframes barFill    { from { width:0 !important; } }

.anim-fade-up    { animation: fadeInUp   0.5s  cubic-bezier(0.22,1,0.36,1) both; }
.anim-pred-reveal{ animation: predReveal 0.55s cubic-bezier(0.22,1,0.36,1) both; }
.anim-d1 { animation-delay: 0.05s; }
.anim-d2 { animation-delay: 0.13s; }
.anim-d3 { animation-delay: 0.22s; }
.anim-d4 { animation-delay: 0.32s; }
.anim-d5 { animation-delay: 0.42s; }
.anim-d6 { animation-delay: 0.52s; }

/* ═══════════════════════ H2H HISTORY ═══════════════════════ */
.h2h-breakdown {
    display: flex; align-items: stretch;
    background: linear-gradient(160deg, #f8fafc, #edf0f7);
    border-radius: 14px; border: 1px solid #dde3ef;
    overflow: hidden; margin: 0.6rem 0 1rem;
}
.h2h-team-block { flex: 1; padding: 1rem 0.75rem; text-align: center; }
.h2h-team-name {
    font-size: 0.62rem; font-weight: 800; letter-spacing: 0.1em;
    text-transform: uppercase; color: #64748b; margin-bottom: 0.35rem;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.h2h-count-big  { font-size: 2.5rem; font-weight: 900; line-height: 1; margin-bottom: 0.2rem; }
.h2h-count-label {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #94a3b8;
}
.h2h-divider { width: 1px; background: #dde3ef; flex-shrink: 0; }
.meetings-title {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #94a3b8; margin-bottom: 0.5rem;
}
.meetings-list  { margin-top: 0.6rem; }
.meeting-row {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.42rem 0; border-bottom: 1px solid #f1f5f9;
}
.meeting-row:last-child { border-bottom: none; }
.meeting-date  { font-size: 0.72rem; font-weight: 600; color: #94a3b8; min-width: 62px; flex-shrink: 0; }
.meeting-score { font-size: 0.9rem; font-weight: 800; color: #0f172a; flex: 1; text-align: center; }
.meeting-badge {
    font-size: 0.6rem; font-weight: 800; letter-spacing: 0.06em;
    padding: 0.18rem 0.52rem; border-radius: 999px; flex-shrink: 0;
}
.badge-w { background: #1e293b; color: #fff; }
.badge-d { background: #e2e8f0; color: #475569; }
.badge-l { background: var(--red); color: #fff; }

/* ═══════════════════════ TEAM FORM ═══════════════════════ */
.form-section   { display: flex; flex-direction: column; gap: 0.7rem; margin-top: 0.25rem; }
.form-team-row  { display: flex; align-items: center; gap: 0.75rem; }
.form-team-label {
    min-width: 105px; font-size: 0.82rem; font-weight: 700; color: #1e293b;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.form-dots { display: flex; gap: 0.38rem; }
.dot {
    width: 30px; height: 30px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.66rem; font-weight: 800; flex-shrink: 0;
}
.dot-w { background: var(--red);  color: #fff; }
.dot-d { background: #cbd5e1;     color: #475569; }
.dot-l { background: #1e293b;     color: #f1f5f9; }

/* ═══════════════════════ KEY PLAYERS ═══════════════════════ */
.players-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 0.5rem; }
.players-col-title {
    font-size: 0.65rem; font-weight: 800; letter-spacing: 0.12em;
    text-transform: uppercase; color: #94a3b8;
    margin-bottom: 0.6rem; padding-bottom: 0.4rem; border-bottom: 2px solid #f1f5f9;
}
.player-item {
    display: flex; align-items: center; gap: 0.55rem;
    padding: 0.38rem 0; border-bottom: 1px solid #f8fafc;
}
.player-item:last-child { border-bottom: none; }
.player-num {
    width: 22px; height: 22px; border-radius: 50%;
    background: #f1f5f9; border: 1px solid #dde3ef;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.6rem; font-weight: 800; color: #64748b; flex-shrink: 0;
}
.player-name { font-size: 0.84rem; font-weight: 600; color: #1e293b; }

/* ═══════════════════════ MATCH PREVIEW ═══════════════════════ */
.preview-box {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border-left: 3px solid var(--red);
    border-radius: 0 14px 14px 0;
    padding: 1.1rem 1.25rem;
    font-size: 0.88rem; font-style: italic; color: #334155; line-height: 1.72;
    margin-top: 0.25rem;
}

/* ═══════════════════════ WORLD CUP GROUPS ═══════════════════════ */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 20px !important;
    background: var(--card) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.07) !important;
    overflow: hidden;
}
[data-testid="stExpander"] summary {
    font-size: 0.9rem !important; font-weight: 700 !important;
    color: #1e293b !important; padding: 1rem 1.5rem !important;
}
[data-testid="stExpander"] summary:hover { background: #f8fafc !important; }
[data-testid="stExpander"] > div:last-child { padding: 0 1rem 1rem !important; }
.group-card {
    background: linear-gradient(160deg, #f8fafc, #f1f5f9);
    border-radius: 16px; padding: 1rem 1.1rem;
    border: 1px solid var(--border);
    box-shadow: 0 1px 4px rgba(0,0,0,0.05), 0 4px 14px rgba(0,0,0,0.04);
    margin-bottom: 0.75rem;
}
.group-header {
    font-size: 0.6rem; font-weight: 800; letter-spacing: 0.18em;
    text-transform: uppercase; color: var(--red);
    padding-bottom: 0.55rem; margin-bottom: 0.55rem;
    border-bottom: 1px solid #dde3ef;
}
.group-team {
    display: flex; align-items: center; gap: 0.55rem;
    padding: 0.38rem 0; border-bottom: 1px solid rgba(221,227,239,0.5);
}
.group-team:last-child { border-bottom: none; }
.group-flag {
    width: 24px; height: auto; border-radius: 3px; flex-shrink: 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.18);
}
.group-team-name { font-size: 0.84rem; font-weight: 600; color: #1e293b; }

/* ═══════════════════════ REVEAL ANIMATION ═══════════════════════ */
@keyframes slideFromLeft  { from { opacity:0; transform:translateX(-52px); } to { opacity:1; transform:translateX(0); } }
@keyframes slideFromRight { from { opacity:0; transform:translateX( 52px); } to { opacity:1; transform:translateX(0); } }

.reveal-flags {
    display: flex; align-items: center; justify-content: center; gap: 2rem;
    padding: 1.5rem 2rem; margin: 1.25rem 0 0;
    background: var(--card); border-radius: 20px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 30px rgba(0,0,0,0.07);
}
.reveal-flag      { display: flex; flex-direction: column; align-items: center; gap: 0.55rem; }
.reveal-flag img  { width: 64px; height: auto; border-radius: 6px; box-shadow: 0 4px 14px rgba(0,0,0,0.22); }
.reveal-flag-name {
    font-size: 0.85rem; font-weight: 700; color: #1e293b;
    text-align: center; max-width: 100px; line-height: 1.2;
}
.reveal-flag-home { animation: slideFromLeft  0.5s cubic-bezier(0.22,1,0.36,1) both; }
.reveal-flag-away { animation: slideFromRight 0.5s cubic-bezier(0.22,1,0.36,1) both; }
.reveal-vs-badge  { animation: fadeInUp 0.4s cubic-bezier(0.22,1,0.36,1) 0.15s both; }

/* ═══════════════════════ NATION PICKER MODAL ═══════════════════════ */
.modal-flag-cell {
    background: linear-gradient(160deg, #f8fafc, #f1f5f9);
    border-radius: 12px; padding: 0.7rem 0.4rem 0.4rem;
    text-align: center; border: 1.5px solid transparent;
    transition: border-color 0.15s, box-shadow 0.15s;
    margin-bottom: 0.15rem;
}
.modal-flag-selected {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 3px rgba(232,17,45,0.12) !important;
}
.modal-flag-img {
    width: 100%; max-width: 62px; height: auto;
    border-radius: 6px; box-shadow: 0 3px 10px rgba(0,0,0,0.22);
}
.modal-flag-btn .stButton button {
    background: white !important; color: #1e293b !important;
    border: 1px solid #e2e8f0 !important; border-radius: 7px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.7rem !important; font-weight: 700 !important;
    text-transform: none !important; letter-spacing: 0 !important;
    box-shadow: none !important; padding: 0.25rem 0.15rem !important;
    line-height: 1.2 !important;
}
.modal-flag-btn .stButton button:hover {
    border-color: var(--red) !important; color: var(--red) !important;
    background: #fff5f5 !important;
}
</style>
"""


_SIDEBAR_TOGGLE_JS = """<script>
(function() {
    var doc = window.parent.document;
    if (doc.getElementById('st-sidebar-toggle')) return;
    var btn = doc.createElement('button');
    btn.id = 'st-sidebar-toggle';
    btn.title = 'Toggle sidebar';
    btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
        + 'stroke="rgba(255,255,255,0.85)" stroke-width="2.5" stroke-linecap="round">'
        + '<line x1="3" y1="6" x2="21" y2="6"/>'
        + '<line x1="3" y1="12" x2="21" y2="12"/>'
        + '<line x1="3" y1="18" x2="21" y2="18"/>'
        + '</svg>';
    btn.style.cssText = [
        'position:fixed', 'top:0.5rem', 'left:0.55rem',
        'z-index:999999999', 'background:transparent', 'border:none',
        'cursor:pointer', 'padding:0.3rem 0.4rem', 'border-radius:6px',
        'line-height:0', 'display:flex', 'align-items:center', 'justify-content:center'
    ].join(';');
    btn.addEventListener('mouseenter', function() {
        btn.style.background = 'rgba(255,255,255,0.12)';
    });
    btn.addEventListener('mouseleave', function() {
        btn.style.background = 'transparent';
    });
    btn.addEventListener('click', function() {
        var cb = doc.querySelector('[data-testid="stSidebarCollapseButton"] button');
        if (cb) { cb.click(); return; }
        var eb = doc.querySelector('[data-testid="stExpandSidebarButton"] button');
        if (eb) { eb.click(); }
    });
    doc.body.appendChild(btn);
})();
</script>"""


def inject_css() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)
    components.html(_SIDEBAR_TOGGLE_JS, height=0)
