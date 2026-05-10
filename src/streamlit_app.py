import base64
import pickle
import pandas as pd
import streamlit as st
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pkl"
DATA_PATH  = BASE_DIR / "data"   / "processed_matches.csv"

OUTCOME_LABELS = {"home_win": "Home Win", "draw": "Draw", "away_win": "Away Win"}
OUTCOME_EMOJI  = {"home_win": "🏆", "draw": "🤝", "away_win": "🏆"}

TOURNAMENT = "FIFA World Cup 2026"

FEATURE_COLS = [
    "home_team", "away_team", "tournament",
    "home_elo", "away_elo", "elo_diff",
    "home_recent_winrate", "away_recent_winrate",
    "home_recent_gd", "away_recent_gd",
    "form_diff", "h2h_winrate", "home_advantage",
]

QUALIFIED_2026 = sorted([
    "Australia", "Iran", "Iraq", "Japan", "Qatar", "Saudi Arabia", "South Korea", "Uzbekistan",
    "Algeria", "Cameroon", "Cape Verde", "Egypt", "Ghana", "Mali", "Morocco", "Nigeria", "Senegal",
    "Canada", "Costa Rica", "Honduras", "Jamaica", "Mexico", "United States",
    "Argentina", "Brazil", "Chile", "Colombia", "Ecuador", "Uruguay",
    "New Zealand",
    "Albania", "Austria", "Belgium", "Croatia", "Czech Republic", "Denmark", "England", "France",
    "Germany", "Hungary", "Italy", "Netherlands", "Poland", "Portugal", "Scotland", "Spain",
])

TEAM_LOGOS: dict[str, str] = {
    "Albania":        "https://flagcdn.com/w160/al.png",
    "Algeria":        "https://flagcdn.com/w160/dz.png",
    "Argentina":      "https://flagcdn.com/w160/ar.png",
    "Australia":      "https://flagcdn.com/w160/au.png",
    "Austria":        "https://flagcdn.com/w160/at.png",
    "Belgium":        "https://flagcdn.com/w160/be.png",
    "Brazil":         "https://flagcdn.com/w160/br.png",
    "Cameroon":       "https://flagcdn.com/w160/cm.png",
    "Canada":         "https://flagcdn.com/w160/ca.png",
    "Cape Verde":     "https://flagcdn.com/w160/cv.png",
    "Chile":          "https://flagcdn.com/w160/cl.png",
    "Colombia":       "https://flagcdn.com/w160/co.png",
    "Costa Rica":     "https://flagcdn.com/w160/cr.png",
    "Croatia":        "https://flagcdn.com/w160/hr.png",
    "Czech Republic": "https://flagcdn.com/w160/cz.png",
    "Denmark":        "https://flagcdn.com/w160/dk.png",
    "Ecuador":        "https://flagcdn.com/w160/ec.png",
    "Egypt":          "https://flagcdn.com/w160/eg.png",
    "England":        "https://flagcdn.com/w160/gb-eng.png",
    "France":         "https://flagcdn.com/w160/fr.png",
    "Germany":        "https://flagcdn.com/w160/de.png",
    "Ghana":          "https://flagcdn.com/w160/gh.png",
    "Honduras":       "https://flagcdn.com/w160/hn.png",
    "Hungary":        "https://flagcdn.com/w160/hu.png",
    "Iran":           "https://flagcdn.com/w160/ir.png",
    "Iraq":           "https://flagcdn.com/w160/iq.png",
    "Italy":          "https://flagcdn.com/w160/it.png",
    "Jamaica":        "https://flagcdn.com/w160/jm.png",
    "Japan":          "https://flagcdn.com/w160/jp.png",
    "Mali":           "https://flagcdn.com/w160/ml.png",
    "Mexico":         "https://flagcdn.com/w160/mx.png",
    "Morocco":        "https://flagcdn.com/w160/ma.png",
    "Netherlands":    "https://flagcdn.com/w160/nl.png",
    "New Zealand":    "https://flagcdn.com/w160/nz.png",
    "Nigeria":        "https://flagcdn.com/w160/ng.png",
    "Poland":         "https://flagcdn.com/w160/pl.png",
    "Portugal":       "https://flagcdn.com/w160/pt.png",
    "Qatar":          "https://flagcdn.com/w160/qa.png",
    "Saudi Arabia":   "https://flagcdn.com/w160/sa.png",
    "Scotland":       "https://flagcdn.com/w160/gb-sct.png",
    "Senegal":        "https://flagcdn.com/w160/sn.png",
    "South Korea":    "https://flagcdn.com/w160/kr.png",
    "Spain":          "https://flagcdn.com/w160/es.png",
    "United States":  "https://flagcdn.com/w160/us.png",
    "Uruguay":        "https://flagcdn.com/w160/uy.png",
    "Uzbekistan":     "https://flagcdn.com/w160/uz.png",
}

KEY_PLAYERS: dict[str, list[str]] = {
    "Albania":        ["A. Broja", "T. Bajrami", "K. Asllani", "M. Gjasula", "T. Berisha (GK)"],
    "Algeria":        ["R. Mahrez", "I. Bennacer", "A. Slimani", "R. Bensebaini", "R. Mbolhi (GK)"],
    "Argentina":      ["L. Messi", "J. Álvarez", "R. De Paul", "Enzo Fernández", "E. Martínez (GK)"],
    "Australia":      ["A. Hrustic", "M. Leckie", "J. Irvine", "A. Kuol", "M. Ryan (GK)"],
    "Austria":        ["M. Sabitzer", "D. Alaba", "C. Baumgartner", "M. Arnautovic", "P. Pentz (GK)"],
    "Belgium":        ["K. De Bruyne", "R. Lukaku", "L. Trossard", "J. Doku", "K. Casteels (GK)"],
    "Brazil":         ["Vinícius Jr.", "Rodrygo", "Bruno Guimarães", "Raphinha", "Alisson (GK)"],
    "Cameroon":       ["V. Aboubakar", "A. Anguissa", "E. Choupo-Moting", "K. Toko Ekambi", "A. Onana (GK)"],
    "Canada":         ["A. Davies", "J. David", "C. Larin", "J. Hoilett", "M. Borjan (GK)"],
    "Cape Verde":     ["R. Andrade", "W. Tavares", "D. Semedo", "K. Rodrigues", "V. Mendes (GK)"],
    "Chile":          ["A. Sánchez", "E. Vargas", "G. Medel", "C. Aranguiz", "C. Bravo (GK)"],
    "Colombia":       ["L. Díaz", "R. Falcao", "D. Arias", "J. Cuadrado", "D. Ospina (GK)"],
    "Costa Rica":     ["J. Campbell", "Y. Tejeda", "C. Calvo", "A. Contreras", "K. Navas (GK)"],
    "Croatia":        ["L. Modric", "M. Kovacic", "I. Perisic", "A. Kramaric", "D. Livakovic (GK)"],
    "Czech Republic": ["P. Schick", "T. Soucek", "M. Kuchta", "L. Provod", "T. Vaclik (GK)"],
    "Denmark":        ["C. Eriksen", "R. Hojlund", "J. Maehle", "T. Delaney", "K. Schmeichel (GK)"],
    "Ecuador":        ["M. Caicedo", "E. Valencia", "G. Plata", "J. Sarmiento", "H. Galíndez (GK)"],
    "Egypt":          ["M. Salah", "A. Trezeguet", "T. El-Nenni", "A. Hegazi", "M. El-Shenawy (GK)"],
    "England":        ["J. Bellingham", "H. Kane", "B. Saka", "P. Foden", "J. Pickford (GK)"],
    "France":         ["K. Mbappé", "A. Griezmann", "A. Tchouaméni", "E. Camavinga", "M. Maignan (GK)"],
    "Germany":        ["T. Müller", "K. Havertz", "J. Kimmich", "S. Gnabry", "M. Neuer (GK)"],
    "Ghana":          ["A. Ayew", "M. Kudus", "T. Partey", "A. Sulemana", "L. Ati-Zigi (GK)"],
    "Honduras":       ["R. Lozano", "R. Bengtson", "M. Quioto", "J. Arriaga", "L. López (GK)"],
    "Hungary":        ["D. Szoboszlai", "B. Varga", "L. Nego", "R. Sallai", "P. Gulácsi (GK)"],
    "Iran":           ["M. Taremi", "A. Jahanbakhsh", "S. Ansarifard", "A. Gholizadeh", "A. Beiranvand (GK)"],
    "Iraq":           ["Aymen Hussein", "Mohanad Ali", "Ali Adnan", "Amjad Radhi", "Jalal Hassan (GK)"],
    "Italy":          ["F. Chiesa", "N. Barella", "S. Tonali", "M. Verratti", "G. Donnarumma (GK)"],
    "Jamaica":        ["L. Bailey", "M. Antonio", "D. Nicholson", "D. Thompson", "A. Blake (GK)"],
    "Japan":          ["T. Minamino", "H. Doan", "H. Tanaka", "W. Endo", "S. Gonda (GK)"],
    "Mali":           ["M. Traoré", "I. Kone", "M. Diallo", "B. Doumbia", "D. Mounkoro (GK)"],
    "Mexico":         ["H. Lozano", "R. Jiménez", "H. Moreno", "A. Guardado", "G. Ochoa (GK)"],
    "Morocco":        ["A. Hakimi", "Y. En-Nesyri", "S. Boufal", "A. Ounahi", "Y. Bono (GK)"],
    "Netherlands":    ["V. Van Dijk", "F. De Jong", "C. Gakpo", "M. Depay", "M. Flekken (GK)"],
    "New Zealand":    ["C. Wood", "M. McGlinchey", "M. Waine", "L. Rojas", "O. Old (GK)"],
    "Nigeria":        ["V. Osimhen", "K. Iheanacho", "T. Aina", "W. Ndidi", "F. Uzoho (GK)"],
    "Poland":         ["R. Lewandowski", "P. Zielinski", "S. Szymanski", "K. Swiderski", "W. Szczesny (GK)"],
    "Portugal":       ["C. Ronaldo", "B. Fernandes", "R. Leão", "Vitinha", "D. Costa (GK)"],
    "Qatar":          ["Almoez Ali", "A. Afif", "K. Boudiaf", "H. Hatem", "S. Al Sheeb (GK)"],
    "Saudi Arabia":   ["S. Al-Shehri", "F. Al-Dawsari", "M. Kanno", "A. Al-Malki", "M. Al-Owais (GK)"],
    "Scotland":       ["A. Robertson", "S. McTominay", "L. Adams", "R. Christie", "A. Gunn (GK)"],
    "Senegal":        ["S. Mané", "I. Gueye", "I. Diatta", "I. Sarr", "E. Mendy (GK)"],
    "South Korea":    ["Son Heung-min", "Hwang Hee-chan", "Lee Kang-in", "Kim Min-jae", "Kim Seung-gyu (GK)"],
    "Spain":          ["Pedri", "A. Morata", "Rodri", "L. Yamal", "Unai Simón (GK)"],
    "United States":  ["C. Pulisic", "G. Reyna", "S. Dest", "T. Adams", "M. Turner (GK)"],
    "Uruguay":        ["L. Suárez", "E. Cavani", "F. Valverde", "R. Bentancur", "S. Rochet (GK)"],
    "Uzbekistan":     ["E. Shomurodov", "O. Tursunov", "J. Sidikov", "U. Khamdamov", "U. Nishonov (GK)"],
}


# ── Model logic (unchanged) ───────────────────────────────────────────────────

@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


@st.cache_data
def build_team_stats(df: pd.DataFrame) -> dict:
    stats: dict = {}
    for _, row in df.sort_values("date").iterrows():
        stats[row["home_team"]] = {
            "elo": row.get("home_elo", 1500),
            "wr":  row.get("home_recent_winrate", 0.33),
            "gd":  row.get("home_recent_gd", 0.0),
        }
        stats[row["away_team"]] = {
            "elo": row.get("away_elo", 1500),
            "wr":  row.get("away_recent_winrate", 0.33),
            "gd":  row.get("away_recent_gd", 0.0),
        }
    return stats


def get_h2h_winrate(df: pd.DataFrame, home_team: str, away_team: str) -> float:
    mask = (
        ((df["home_team"] == home_team) & (df["away_team"] == away_team)) |
        ((df["home_team"] == away_team) & (df["away_team"] == home_team))
    )
    past = df[mask]
    if past.empty:
        return 0.5
    home_wins = (
        ((past["home_team"] == home_team) & (past["home_score"] > past["away_score"])) |
        ((past["away_team"] == home_team) & (past["away_score"] > past["home_score"]))
    ).sum()
    return float(home_wins / len(past))


def build_input_row(home_team, away_team, tournament, neutral, team_stats, h2h) -> pd.DataFrame:
    h = team_stats.get(home_team, {"elo": 1500, "wr": 0.33, "gd": 0.0})
    a = team_stats.get(away_team, {"elo": 1500, "wr": 0.33, "gd": 0.0})
    row = {
        "home_team":           home_team,
        "away_team":           away_team,
        "tournament":          tournament,
        "home_elo":            h["elo"],
        "away_elo":            a["elo"],
        "elo_diff":            h["elo"] - a["elo"],
        "home_recent_winrate": h["wr"],
        "away_recent_winrate": a["wr"],
        "home_recent_gd":      h["gd"],
        "away_recent_gd":      a["gd"],
        "form_diff":           h["wr"] - a["wr"],
        "h2h_winrate":         h2h,
        "home_advantage":      0 if neutral else 1,
    }
    return pd.DataFrame([row])[FEATURE_COLS]


def get_h2h_stats(df: pd.DataFrame, home_team: str, away_team: str) -> dict:
    mask = (
        ((df["home_team"] == home_team) & (df["away_team"] == away_team)) |
        ((df["home_team"] == away_team) & (df["away_team"] == home_team))
    )
    past = df[mask].sort_values("date", ascending=False)
    total = len(past)
    if total == 0:
        return {"total": 0, "home_wins": 0, "draws": 0, "away_wins": 0, "last5": []}
    home_wins = int((
        ((past["home_team"] == home_team) & (past["home_score"] > past["away_score"])) |
        ((past["away_team"] == home_team) & (past["away_score"] > past["home_score"]))
    ).sum())
    away_wins = int((
        ((past["home_team"] == away_team) & (past["home_score"] > past["away_score"])) |
        ((past["away_team"] == away_team) & (past["away_score"] > past["home_score"]))
    ).sum())
    draws = total - home_wins - away_wins
    last5 = []
    for _, row in past.head(5).iterrows():
        if row["home_team"] == home_team:
            ht_score, at_score = int(row["home_score"]), int(row["away_score"])
        else:
            ht_score, at_score = int(row["away_score"]), int(row["home_score"])
        result = "W" if ht_score > at_score else ("D" if ht_score == at_score else "L")
        last5.append({
            "date":   pd.to_datetime(row["date"]).strftime("%b %Y"),
            "score":  f"{ht_score}–{at_score}",
            "result": result,
        })
    return {"total": total, "home_wins": home_wins, "draws": draws, "away_wins": away_wins, "last5": last5}


def get_team_form(df: pd.DataFrame, team: str, n: int = 5) -> list[str]:
    mask = (df["home_team"] == team) | (df["away_team"] == team)
    past = df[mask].sort_values("date", ascending=False).head(n)
    results = []
    for _, row in past.iterrows():
        if row["home_team"] == team:
            gf, ga = int(row["home_score"]), int(row["away_score"])
        else:
            gf, ga = int(row["away_score"]), int(row["home_score"])
        results.append("W" if gf > ga else ("D" if gf == ga else "L"))
    return results


def generate_preview(home_team, away_team, h_stats, a_stats, h2h_data,
                     p_home, p_draw, p_away, neutral, prediction) -> str:
    elo_diff   = h_stats["elo"] - a_stats["elo"]
    stronger   = home_team if elo_diff >= 0 else away_team
    elo_margin = abs(elo_diff)
    venue      = "a neutral venue" if neutral else f"{home_team}'s home ground"
    conf       = max(p_home, p_draw, p_away)

    if prediction == "home_win":
        outcome_phrase = f"{home_team} are the model's pick to win"
    elif prediction == "away_win":
        outcome_phrase = f"{away_team} are favoured to take all three points"
    else:
        outcome_phrase = "the model expects a tightly contested draw"

    if elo_margin > 100:
        elo_line = f"{stronger} carry a commanding Elo advantage of {elo_margin:.0f} points. "
    elif elo_margin > 40:
        elo_line = f"{stronger} hold a meaningful Elo edge of {elo_margin:.0f} points. "
    else:
        elo_line = "Elo ratings paint an evenly matched picture. "

    h_wr, a_wr = h_stats["wr"] * 100, a_stats["wr"] * 100
    if abs(h_wr - a_wr) < 10:
        form_line = f"Both sides arrive in similar form ({home_team} {h_wr:.0f}% · {away_team} {a_wr:.0f}% recent win rate). "
    elif h_wr > a_wr:
        form_line = f"{home_team} are in stronger recent form at {h_wr:.0f}% versus {away_team}'s {a_wr:.0f}%. "
    else:
        form_line = f"{away_team} come in hotter at {a_wr:.0f}% versus {home_team}'s {h_wr:.0f}% recent win rate. "

    total = h2h_data["total"]
    if total == 0:
        h2h_line = "These teams have no recorded head-to-head history — an open book."
    elif total < 5:
        h2h_line = f"With only {total} prior encounter(s) on record, historical data offers limited guidance."
    else:
        hw, d, aw = h2h_data["home_wins"], h2h_data["draws"], h2h_data["away_wins"]
        if hw > aw:
            h2h_line = f"History leans toward {home_team} across {total} meetings ({hw}W–{d}D–{aw}L)."
        elif aw > hw:
            h2h_line = f"{away_team} have the historical edge, winning {aw} of {total} meetings."
        else:
            h2h_line = f"Their {total} meetings are evenly split — another unpredictable contest awaits."

    return (
        f"On {venue}, {outcome_phrase} with {conf:.0%} model confidence. "
        f"{elo_line}{form_line}{h2h_line}"
    )


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="2026 World Cup Predictor", page_icon="🏆", layout="centered")

# ── Global CSS ────────────────────────────────────────────────────────────────

st.markdown("""
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

/* Soft stadium-light background — white overhead, red accent, no green */
.stApp {
    background:
        radial-gradient(ellipse 110% 55% at 50% -8%, rgba(255,255,255,0.90) 0%, transparent 100%),
        radial-gradient(ellipse 50% 30% at 95% 85%, rgba(232,17,45,0.06)    0%, transparent 55%),
        radial-gradient(ellipse 40% 25% at 50% 110%, rgba(0,0,0,0.05)       0%, transparent 55%),
        linear-gradient(180deg, #edf0f8 0%, #f2f4f9 100%) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 780px !important;
    padding: 0 1.25rem 4rem 1.25rem !important;
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
/* stadium-light cone from top */
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
/* single red accent line at base of hero */
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
.stToggle > label { font-weight: 500 !important; color: #475569 !important; }

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
</style>
""", unsafe_allow_html=True)


# ── Hero banner ───────────────────────────────────────────────────────────────

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

st.markdown(f"""
<div class="wc-hero">
    <div class="hero-eyebrow">FIFA World Cup™</div>
    {_emblem_img_tag()}
    <h1 class="hero-title">2026 Match Predictor</h1>
    <p class="hero-sub">USA &nbsp;·&nbsp; Canada &nbsp;·&nbsp; Mexico</p>
</div>
""", unsafe_allow_html=True)

# ── Guards ────────────────────────────────────────────────────────────────────

if not MODEL_PATH.exists():
    st.error("Model not found. Run `python src/train_model.py` first.")
    st.stop()
if not DATA_PATH.exists():
    st.error("Data not found. Run `python src/preprocess.py` first.")
    st.stop()

pipeline   = load_model()
df         = load_data()
team_stats = build_team_stats(df)

# ── Team Selection Card ───────────────────────────────────────────────────────

st.markdown('<div class="wc-card">', unsafe_allow_html=True)
st.markdown('<span class="wc-card-label">⚽ Select Teams</span>', unsafe_allow_html=True)

c_home, c_vs, c_away = st.columns([10, 3, 10])

with c_home:
    home_team = st.selectbox("🏠 Home Team", QUALIFIED_2026,
                             index=QUALIFIED_2026.index("Brazil") if "Brazil" in QUALIFIED_2026 else 0)
    h_elo_val = team_stats.get(home_team, {}).get("elo", 1500)
    home_flag = TEAM_LOGOS.get(home_team, "")
    st.markdown(f"""
    <div class="team-crest">
        <img src="{home_flag}" alt="{home_team}" />
        <div class="crest-name">{home_team}</div>
    </div>""", unsafe_allow_html=True)

with c_vs:
    st.markdown("""
    <div class="vs-col">
        <div class="vs-line-top"></div>
        <div class="vs-circle"><span>VS</span></div>
        <div class="vs-line-bot"></div>
    </div>""", unsafe_allow_html=True)

with c_away:
    away_team = st.selectbox("✈️ Away Team", QUALIFIED_2026,
                             index=QUALIFIED_2026.index("Argentina") if "Argentina" in QUALIFIED_2026 else 1)
    a_elo_val = team_stats.get(away_team, {}).get("elo", 1500)
    away_flag = TEAM_LOGOS.get(away_team, "")
    st.markdown(f"""
    <div class="team-crest">
        <img src="{away_flag}" alt="{away_team}" />
        <div class="crest-name">{away_team}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr style="margin:1.25rem 0 0.85rem;">', unsafe_allow_html=True)
neutral = st.toggle("🌐 Neutral Venue", value=True)
st.markdown(f'<p style="font-size:0.75rem;color:#94a3b8;margin:0.2rem 0 0;">Tournament: {TOURNAMENT}</p>',
            unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if home_team == away_team:
    st.warning("Home and away teams must be different.")
    st.stop()

predict = st.button("⚽  Predict Match Outcome", type="primary", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────

if predict:
    h2h      = get_h2h_winrate(df, home_team, away_team)
    h2h_data = get_h2h_stats(df, home_team, away_team)
    home_form = get_team_form(df, home_team)
    away_form = get_team_form(df, away_team)
    X_input  = build_input_row(home_team, away_team, TOURNAMENT, neutral, team_stats, h2h)

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

    if prediction == "home_win":
        flag_url = TEAM_LOGOS.get(home_team, "")
    elif prediction == "away_win":
        flag_url = TEAM_LOGOS.get(away_team, "")
    else:
        flag_url = ""

    if flag_url:
        pred_icon_html = (
            f'<img src="{flag_url}" '
            f'style="width:40px;height:auto;border-radius:5px;'
            f'box-shadow:0 3px 14px rgba(0,0,0,0.45);'
            f'display:block;margin:0 auto 0.5rem;position:relative;z-index:1;" />'
        )
    else:
        pred_icon_html = '<div class="pred-emoji">🤝</div>'

    # Prediction card
    st.markdown(f"""
    <div class="pred-hero anim-pred-reveal" style="margin:1.25rem 0 1.25rem;">
        {pred_icon_html}
        <div class="pred-title">{winner_line}</div>
        <div class="pred-sub">{home_team} &nbsp;·&nbsp; {TOURNAMENT} &nbsp;·&nbsp; {away_team}</div>
    </div>""", unsafe_allow_html=True)

    # Probability bars card
    p_home = prob_map.get("home_win", 0.0)
    p_draw = prob_map.get("draw",     0.0)
    p_away = prob_map.get("away_win", 0.0)

    st.markdown(f"""
    <div class="wc-card anim-fade-up anim-d1">
        <span class="wc-card-label">📊 Win Probabilities</span>
        <div class="prob-row">
            <span class="prob-label">🏠 {home_team}</span>
            <div class="prob-track"><div class="prob-fill prob-home" style="width:{p_home*100:.1f}%"></div></div>
            <span class="prob-pct">{p_home:.0%}</span>
        </div>
        <div class="prob-row">
            <span class="prob-label">🤝 Draw</span>
            <div class="prob-track"><div class="prob-fill prob-draw" style="width:{p_draw*100:.1f}%"></div></div>
            <span class="prob-pct">{p_draw:.0%}</span>
        </div>
        <div class="prob-row">
            <span class="prob-label">✈️ {away_team}</span>
            <div class="prob-track"><div class="prob-fill prob-away" style="width:{p_away*100:.1f}%"></div></div>
            <span class="prob-pct">{p_away:.0%}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Match Insights card
    h_stats   = team_stats.get(home_team, {"elo": 1500, "wr": 0.33, "gd": 0.0})
    a_stats   = team_stats.get(away_team, {"elo": 1500, "wr": 0.33, "gd": 0.0})
    elo_diff  = h_stats["elo"] - a_stats["elo"]
    form_diff = h_stats["wr"]  - a_stats["wr"]
    adv_text  = "None" if neutral else "Active"
    adv_color  = "#94a3b8" if neutral else "#f1f5f9"
    elo_color  = "#f1f5f9" if elo_diff  >= 0 else "#E8112D"
    form_color = "#f1f5f9" if form_diff >= 0 else "#E8112D"

    st.markdown(f"""
    <div class="wc-card anim-fade-up anim-d2">
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
                <div class="insight-value">{h2h:.0%}</div>
                <div class="insight-label">H2H Win Rate</div>
            </div>
            <div class="insight-cell">
                <div class="insight-value" style="color:{adv_color};">{adv_text}</div>
                <div class="insight-label">Home Advantage</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── H2H History card ──────────────────────────────────────────────────────
    total   = h2h_data["total"]
    hw_cnt  = h2h_data["home_wins"]
    d_cnt   = h2h_data["draws"]
    aw_cnt  = h2h_data["away_wins"]

    if h2h_data["last5"]:
        meetings_rows = ""
        for m in h2h_data["last5"]:
            bc = {"W": "badge-w", "D": "badge-d", "L": "badge-l"}[m["result"]]
            bt = {"W": "WIN",     "D": "DRAW",    "L": "LOSS"}[m["result"]]
            meetings_rows += (
                f'<div class="meeting-row">'
                f'<span class="meeting-date">{m["date"]}</span>'
                f'<span class="meeting-score">{m["score"]}</span>'
                f'<span class="meeting-badge {bc}">{bt}</span>'
                f'</div>'
            )
        last5_html = (
            f'<div class="meetings-list">'
            f'<div class="meetings-title">Last {len(h2h_data["last5"])} meetings</div>'
            f'{meetings_rows}</div>'
        )
    else:
        last5_html = '<p style="color:#94a3b8;font-size:0.82rem;text-align:center;padding:0.5rem 0;">No head-to-head records found.</p>'

    no_h2h_note = "" if total > 0 else '<p style="color:#94a3b8;font-size:0.82rem;text-align:center;padding:0.25rem 0 0;">First ever meeting between these sides.</p>'

    st.markdown(f"""
    <div class="wc-card anim-fade-up anim-d3">
        <span class="wc-card-label">⚔️ Head-to-Head History</span>
        <div class="h2h-breakdown">
            <div class="h2h-team-block">
                <div class="h2h-team-name">{home_team}</div>
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
                <div class="h2h-team-name">{away_team}</div>
                <div class="h2h-count-big" style="color:var(--red);">{aw_cnt}</div>
                <div class="h2h-count-label">Wins</div>
            </div>
        </div>
        {no_h2h_note}{last5_html}
    </div>""", unsafe_allow_html=True)

    # ── Team Form card ────────────────────────────────────────────────────────
    def _dots(form):
        if not form:
            return '<span style="color:#94a3b8;font-size:0.8rem;">No data</span>'
        cls = {"W": "dot-w", "D": "dot-d", "L": "dot-l"}
        return "".join(f'<span class="dot {cls[r]}">{r}</span>' for r in form)

    st.markdown(f"""
    <div class="wc-card anim-fade-up anim-d4">
        <span class="wc-card-label">📈 Recent Form — Last 5 Matches</span>
        <div class="form-section">
            <div class="form-team-row">
                <span class="form-team-label">{home_team}</span>
                <div class="form-dots">{_dots(home_form)}</div>
            </div>
            <div class="form-team-row">
                <span class="form-team-label">{away_team}</span>
                <div class="form-dots">{_dots(away_form)}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Key Players card ──────────────────────────────────────────────────────
    def _players_html(team):
        players = KEY_PLAYERS.get(team, [f"Player {i}" for i in range(1, 6)])
        return "".join(
            f'<div class="player-item">'
            f'<span class="player-num">{i}</span>'
            f'<span class="player-name">{p}</span>'
            f'</div>'
            for i, p in enumerate(players, 1)
        )

    st.markdown(f"""
    <div class="wc-card anim-fade-up anim-d5">
        <span class="wc-card-label">⭐ Key Players</span>
        <div class="players-grid">
            <div>
                <div class="players-col-title">{home_team}</div>
                {_players_html(home_team)}
            </div>
            <div>
                <div class="players-col-title">{away_team}</div>
                {_players_html(away_team)}
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Match Preview card ────────────────────────────────────────────────────
    preview_text = generate_preview(
        home_team, away_team, h_stats, a_stats,
        h2h_data, p_home, p_draw, p_away, neutral, prediction
    )

    st.markdown(f"""
    <div class="wc-card anim-fade-up anim-d6">
        <span class="wc-card-label">📝 Match Preview</span>
        <div class="preview-box">{preview_text}</div>
    </div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; padding:2rem 0 0.5rem; border-top:1px solid #e4eaf3; margin-top:1rem;
            color:#94a3b8; font-size:0.8rem; font-weight:500; letter-spacing:0.03em;">
    Made by <strong style="color:#475569;">Biruk</strong>
    &nbsp;·&nbsp; 2026 World Cup Edition &nbsp;·&nbsp; Version 1.0
</div>
""", unsafe_allow_html=True)
