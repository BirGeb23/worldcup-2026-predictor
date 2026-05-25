# 2026 FIFA World Cup Match Predictor

> A machine-learning-powered match outcome predictor for the 2026 FIFA World Cup — built with Python, scikit-learn, and Streamlit.

---

## Features

- **ML Match Prediction** — predicts Win / Draw / Loss using Logistic Regression and Random Forest trained on historical FIFA match data
- **Live Countdown Timer** — real-time ticker counting down to the June 11 2026 opening match, updating every second via `st.fragment`
- **Browse Nations Modal** — searchable flag grid covering all 48 qualified nations; click any flag card to instantly swap the selected team
- **Animated Reveal** — results appear in a staggered sequence: team flags → predicted winner → probability bars → insights panel
- **Win Probability Bars** — animated bars showing the likelihood of each outcome (Home / Draw / Away)
- **Match Insights Panel** — Elo edge, form differential, H2H win rate, and home advantage in a single grid
- **Head-to-Head History** — full W/D/L record and last 5 meetings pulled from historical data
- **Team Form Tracker** — last 5 results per team displayed as coloured W/D/L dots
- **Key Players** — curated squad highlights for all 48 qualified nations
- **Auto-Generated Match Preview** — narrative text built from Elo, form, and H2H stats
- **2026 Group Draw** — collapsible panel showing all 12 official groups with flags
- **48 Qualified Nations** — full CONCACAF, UEFA, AFC, CAF, CONMEBOL, and OFC rosters

---

## Live Demo

> **Streamlit Cloud:** `<!-- https://your-app-url.streamlit.app -->`
> _(Link will be added after deployment)_

---

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| ML | scikit-learn (LogisticRegression, RandomForest, Pipeline, ColumnTransformer) |
| Data | pandas |
| Frontend | Streamlit + custom CSS |
| Flags | [flagcdn.com](https://flagcdn.com) |
| Version Control | Git / GitHub |

---

## Installation

**1. Clone the repository**

```bash
git clone git@github.com:BirGeb23/worldcup-2026-predictor.git
cd worldcup-2026-predictor
```

**2. Install dependencies**

```bash
pip install streamlit scikit-learn pandas
```

**3. Run the preprocessing pipeline**

```bash
python src/preprocess.py
```

**4. Train the model**

```bash
python src/train_model.py
```

**5. Launch the app**

```bash
streamlit run src/streamlit_app.py
```

---

## How to Use

1. Open the app in your browser (defaults to `http://localhost:8501`)
2. Click **Browse all nations** under HOME or AWAY to open the flag grid
3. Search or scroll to find a nation — click its card to select it
4. Toggle **Neutral Venue** if the match is played on neutral ground
5. Click **Predict Match Outcome**
6. Watch the animated reveal — team flags slide in, the predicted winner fades up, then probability bars expand and the full insights panel appears

---

## Project Structure

```
worldcup-2026-predictor/
│
├── src/
│   ├── streamlit_app.py          # Entry point — page config, layout orchestration
│   ├── styles.py                 # Global CSS injected at startup
│   │
│   ├── components/
│   │   ├── countdown.py          # Live countdown fragment (st.fragment, run_every=1)
│   │   ├── team_selector.py      # HOME/AWAY cards + Browse Nations modal
│   │   ├── strength_meter.py     # Animated prediction reveal sequence
│   │   └── groups.py             # 2026 group draw expander
│   │
│   ├── data/
│   │   ├── team_logos.py         # Flag URLs for all 48 nations (flagcdn.com)
│   │   ├── qualified_teams.py    # QUALIFIED_2026 list + GROUPS draw dict
│   │   └── world_rankings.py     # KEY_PLAYERS squads for all 48 nations
│   │
│   ├── logic/
│   │   └── prediction.py         # Model I/O, feature engineering, stat helpers
│   │
│   ├── preprocess.py             # Feature engineering pipeline (Elo, form, H2H)
│   └── train_model.py            # Model training and serialisation
│
├── data/
│   ├── results.csv               # Historical international match results
│   ├── goalscorers.csv           # Goal-level event data
│   ├── shootouts.csv             # Penalty shootout records
│   ├── former_names.csv          # Historical team name mappings
│   └── processed_matches.csv     # Engineered feature dataset (generated)
│
├── models/
│   └── model.pkl                 # Trained pipeline (generated)
│
├── assets/
│   └── worldcup2026.png          # Official emblem (add manually)
│
└── README.md
```

---

## Architecture

The app is split into four layers so each concern lives in one place:

| Layer | Path | Responsibility |
|---|---|---|
| **Entry point** | `src/streamlit_app.py` | Page config, layout order, prediction trigger |
| **Styles** | `src/styles.py` | All CSS — injected once at startup via `inject_css()` |
| **Components** | `src/components/` | Self-contained UI pieces; each exposes a `render_*` function |
| **Data** | `src/data/` | Pure Python dicts/lists — no logic, no imports |
| **Logic** | `src/logic/prediction.py` | Model loading, feature engineering, stat calculations |

Streamlit adds `src/` to `sys.path` at runtime, so every sub-package imports as `from data.team_logos import TEAM_LOGOS`, `from logic.prediction import build_input_row`, etc.

---

## Feature Engineering

The model uses no raw match scores as input — all features are pre-match statistics only:

| Feature | Description |
|---|---|
| `home_elo` / `away_elo` | Elo rating at time of match |
| `elo_diff` | Home Elo minus Away Elo |
| `home_recent_winrate` | Win % across last 5 matches |
| `away_recent_winrate` | Win % across last 5 matches |
| `home_recent_gd` | Average goal difference, last 5 matches |
| `away_recent_gd` | Average goal difference, last 5 matches |
| `form_diff` | Home win rate minus Away win rate |
| `h2h_winrate` | Home team's historical win rate vs this opponent |
| `home_advantage` | 1 if non-neutral venue, 0 if neutral |

---

## Future Improvements

- [ ] **Tournament Simulation** — simulate the full group stage and knockout bracket
- [ ] **Live Odds Comparison** — compare model probabilities with bookmaker lines
- [ ] **Form Trend Chart** — sparkline of Elo rating over the last 12 months
- [ ] **Team Info Drawer** — expandable panel with squad depth, coach, confederation
- [ ] **Deploy to Streamlit Cloud** — add live demo link

---

## Data Sources

Historical match data sourced from publicly available football datasets covering international fixtures from 1872 to the present.

---

## Disclaimer

This project is an **unofficial fan project** created for educational and entertainment purposes. It is **not affiliated with, endorsed by, or associated with FIFA** or any national football association. All team names, flags, and tournament references are used for non-commercial, informational purposes only.

---

## Author

**Biruk** — [GitHub](https://github.com/BirGeb23)

---

*2026 World Cup Edition · USA · Canada · Mexico*
