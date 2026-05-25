import pickle
import pandas as pd
import streamlit as st
from pathlib import Path

# src/logic/prediction.py → parent = logic/ → parent = src/ → parent = project root
BASE_DIR   = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pkl"
DATA_PATH  = BASE_DIR / "data"   / "processed_matches.csv"

TOURNAMENT = "FIFA World Cup 2026"

OUTCOME_LABELS = {"home_win": "Home Win", "draw": "Draw", "away_win": "Away Win"}
OUTCOME_EMOJI  = {"home_win": "🏆", "draw": "🤝", "away_win": "🏆"}

FEATURE_COLS = [
    "home_team", "away_team", "tournament",
    "home_elo", "away_elo", "elo_diff",
    "home_recent_winrate", "away_recent_winrate",
    "home_recent_gd", "away_recent_gd",
    "form_diff", "h2h_winrate", "home_advantage",
]


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


def build_input_row(
    home_team: str, away_team: str, tournament: str,
    neutral: bool, team_stats: dict, h2h: float
) -> pd.DataFrame:
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
    return {
        "total": total, "home_wins": home_wins,
        "draws": draws, "away_wins": away_wins, "last5": last5,
    }


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


def generate_preview(
    home_team: str, away_team: str,
    h_stats: dict, a_stats: dict, h2h_data: dict,
    p_home: float, p_draw: float, p_away: float,
    neutral: bool, prediction: str,
) -> str:
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
