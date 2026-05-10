# 2026 FIFA World Cup Match Predictor

> A machine-learning-powered match outcome predictor for the 2026 FIFA World Cup — built with Python, scikit-learn, and Streamlit.

---

## Features

- **ML Match Prediction** — predicts Win / Draw / Loss using Logistic Regression and Random Forest trained on historical FIFA match data
- **Elo-Based Rankings** — each team's strength is derived from a chronological Elo rating system (K=32)
- **Animated Reveal** — results appear in a staggered sequence: team flags → predicted winner → probability bars → insights panel
- **Win Probability Bars** — animated bars showing the likelihood of each outcome
- **Match Insights Panel** — Elo edge, recent form differential, H2H win rate, and home advantage at a glance
- **Head-to-Head History** — full W/D/L record and last 5 meetings pulled from historical data
- **Team Form Tracker** — last 5 match results per team displayed as coloured W/D/L dots
- **Key Players** — curated starting lineup highlights for all 48 qualified nations
- **Match Preview** — auto-generated match narrative based on the computed stats
- **2026 World Cup UI** — official colour palette (red `#E8112D`, black, silver), team flags via flagcdn, animated card layout
- **48 Qualified Nations** — full CONCACAF, UEFA, AFC, CAF, CONMEBOL, and OFC squads
- _(Placeholder) World Rankings integration_
- _(Placeholder) Team Info Drawer_

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
pip install -r requirements.txt
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
2. Select a **Home Team** and an **Away Team** from the dropdowns
3. Toggle **Neutral Venue** if the match is played on neutral ground
4. Click **Predict Match Outcome**
5. Watch the animated reveal — team flags slide in, the predicted winner fades in, then probability bars expand and the full insights panel appears below

---

## Project Structure

```
worldcup-2026-predictor/
│
├── src/
│   ├── streamlit_app.py      # Main Streamlit UI and animation logic
│   ├── preprocess.py         # Feature engineering pipeline (Elo, form, H2H)
│   └── train_model.py        # Model training and serialisation
│
├── data/
│   ├── results.csv           # Historical match results
│   ├── goalscorers.csv       # Goal-level data
│   ├── shootouts.csv         # Penalty shootout records
│   ├── former_names.csv      # Historical team name mappings
│   └── processed_matches.csv # Engineered feature dataset (generated)
│
├── models/
│   └── model.pkl             # Trained pipeline (generated)
│
├── assets/
│   └── worldcup2026.png      # Official emblem (add manually)
│
├── requirements.txt
└── README.md
```

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

- [ ] **World Rankings** — overlay FIFA/Elo world ranking badges on team cards
- [ ] **Team Info Drawer** — expandable panel with squad depth, coach, confederation
- [ ] **Tournament Simulation** — simulate the full group stage and knockout bracket
- [ ] **Live Odds Comparison** — compare model probabilities with bookmaker lines
- [ ] **Form Trend Chart** — sparkline graph of Elo rating over the last 12 months

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
