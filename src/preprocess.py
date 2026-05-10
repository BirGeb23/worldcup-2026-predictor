import pandas as pd
from pathlib import Path

DATA_DIR = Path("./data")
ELO_K = 32
DEFAULT_ELO = 1500


def load_data():
    results = pd.read_csv(DATA_DIR / "results.csv", parse_dates=["date"])
    goalscorers = pd.read_csv(DATA_DIR / "goalscorers.csv", parse_dates=["date"])
    former_names = pd.read_csv(DATA_DIR / "former_names.csv", parse_dates=["start_date", "end_date"])
    shootouts = pd.read_csv(DATA_DIR / "shootouts.csv", parse_dates=["date"])
    return results, goalscorers, former_names, shootouts


def normalize_team_names(df: pd.DataFrame, former_names: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    def resolve(name, date):
        mask = (
            (former_names["former"] == name)
            & (former_names["start_date"] <= date)
            & (former_names["end_date"] >= date)
        )
        m = former_names[mask]
        return m.iloc[0]["current"] if not m.empty else name

    df["home_team"] = df.apply(lambda r: resolve(r["home_team"], r["date"]), axis=1)
    df["away_team"] = df.apply(lambda r: resolve(r["away_team"], r["date"]), axis=1)
    return df


def aggregate_goals(goalscorers: pd.DataFrame) -> pd.DataFrame:
    gs = goalscorers.copy()
    gs["goal_value"] = gs["own_goal"].apply(lambda x: -1 if x else 1)
    home = (
        gs[gs["team"] == gs["home_team"]]
        .groupby(["date", "home_team", "away_team"])["goal_value"]
        .sum().reset_index().rename(columns={"goal_value": "home_score_gs"})
    )
    away = (
        gs[gs["team"] == gs["away_team"]]
        .groupby(["date", "home_team", "away_team"])["goal_value"]
        .sum().reset_index().rename(columns={"goal_value": "away_score_gs"})
    )
    scores = home.merge(away, on=["date", "home_team", "away_team"], how="outer").fillna(0)
    scores["home_score_gs"] = scores["home_score_gs"].astype(int)
    scores["away_score_gs"] = scores["away_score_gs"].astype(int)
    return scores


def add_shootout_feature(df: pd.DataFrame, shootouts: pd.DataFrame) -> pd.DataFrame:
    keys = shootouts[["date", "home_team", "away_team"]].copy()
    keys["went_to_shootout"] = True
    df = df.merge(keys, on=["date", "home_team", "away_team"], how="left")
    df["went_to_shootout"] = df["went_to_shootout"].fillna(False)
    return df


def label_matches(df: pd.DataFrame) -> pd.DataFrame:
    def label(row):
        if row["home_score"] > row["away_score"]:
            return "home_win"
        if row["home_score"] < row["away_score"]:
            return "away_win"
        return "draw"
    df = df.copy()
    df["outcome"] = df.apply(label, axis=1)
    return df


def compute_elo(df: pd.DataFrame):
    df = df.sort_values("date").copy()
    elo: dict = {}
    home_elos, away_elos = [], []

    for _, row in df.iterrows():
        h, a = row["home_team"], row["away_team"]
        h_elo = elo.get(h, DEFAULT_ELO)
        a_elo = elo.get(a, DEFAULT_ELO)
        home_elos.append(h_elo)
        away_elos.append(a_elo)

        exp_h = 1 / (1 + 10 ** ((a_elo - h_elo) / 400))
        if row["home_score"] > row["away_score"]:
            act_h = 1.0
        elif row["home_score"] < row["away_score"]:
            act_h = 0.0
        else:
            act_h = 0.5

        elo[h] = h_elo + ELO_K * (act_h - exp_h)
        elo[a] = a_elo + ELO_K * ((1 - act_h) - (1 - exp_h))

    df["home_elo"] = home_elos
    df["away_elo"] = away_elos
    df["elo_diff"] = df["home_elo"] - df["away_elo"]
    return df, elo


def compute_recent_form(df: pd.DataFrame, n: int = 5):
    df = df.sort_values("date").copy()
    hist: dict = {}
    h_wr, a_wr, h_gd, a_gd = [], [], [], []

    for _, row in df.iterrows():
        home, away = row["home_team"], row["away_team"]

        def form(team):
            past = hist.get(team, [])[-n:]
            if not past:
                return 0.33, 0.0
            wins = sum(1 for gf, ga in past if gf > ga)
            return wins / len(past), sum(gf - ga for gf, ga in past) / len(past)

        hwf, hgd = form(home)
        awf, agd = form(away)
        h_wr.append(hwf); a_wr.append(awf)
        h_gd.append(hgd); a_gd.append(agd)

        hist.setdefault(home, []).append((row["home_score"], row["away_score"]))
        hist.setdefault(away, []).append((row["away_score"], row["home_score"]))

    df["home_recent_winrate"] = h_wr
    df["away_recent_winrate"] = a_wr
    df["home_recent_gd"] = h_gd
    df["away_recent_gd"] = a_gd
    df["form_diff"] = df["home_recent_winrate"] - df["away_recent_winrate"]
    return df, hist


def compute_h2h(df: pd.DataFrame):
    df = df.sort_values("date").copy()
    h2h: dict = {}
    rates = []

    for _, row in df.iterrows():
        home, away = row["home_team"], row["away_team"]
        key = tuple(sorted([home, away]))
        past = h2h.get(key, [])

        if past:
            home_wins = sum(
                1 for h, a, hs, as_ in past
                if (h == home and hs > as_) or (a == home and as_ > hs)
            )
            rates.append(home_wins / len(past))
        else:
            rates.append(0.5)

        h2h.setdefault(key, []).append((home, away, row["home_score"], row["away_score"]))

    df["h2h_winrate"] = rates
    return df, h2h


def add_home_advantage(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["home_advantage"] = (~df["neutral"].astype(bool)).astype(int)
    return df


def build_dataset() -> pd.DataFrame:
    results, goalscorers, former_names, shootouts = load_data()

    results = normalize_team_names(results, former_names)
    goalscorers = normalize_team_names(goalscorers, former_names)
    shootouts = normalize_team_names(shootouts, former_names)

    scores = aggregate_goals(goalscorers)
    df = results.merge(scores, on=["date", "home_team", "away_team"], how="left")

    df["home_score"] = df["home_score_gs"].combine_first(df["home_score"]).fillna(0).astype(int)
    df["away_score"] = df["away_score_gs"].combine_first(df["away_score"]).fillna(0).astype(int)
    df = df.drop(columns=["home_score_gs", "away_score_gs"], errors="ignore")

    df = add_shootout_feature(df, shootouts)
    df = label_matches(df)
    df, _ = compute_elo(df)
    df, _ = compute_recent_form(df)
    df, _ = compute_h2h(df)
    df = add_home_advantage(df)

    return df.dropna(subset=["outcome"]).reset_index(drop=True)


def save_dataset(df: pd.DataFrame, path: Path = DATA_DIR / "processed_matches.csv") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


if __name__ == "__main__":
    df = build_dataset()
    print(df.shape)
    print(df["outcome"].value_counts())
    save_dataset(df)
