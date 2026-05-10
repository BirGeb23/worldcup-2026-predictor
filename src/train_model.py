import pickle
import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = Path("./data/processed_matches.csv")
MODEL_DIR = Path("./models")
TARGET = "outcome"

# Leakage columns (derived from scores) and non-predictive identifiers are excluded.
# went_to_shootout is unknowable pre-match; home/away_score determine the label.
DROP_COLS = {
    "date", TARGET,
    "home_score", "away_score",
    "went_to_shootout",
    "city", "country", "neutral",
}

CAT_COLS = ["home_team", "away_team", "tournament"]

NUM_COLS = [
    "home_elo", "away_elo", "elo_diff",
    "home_recent_winrate", "away_recent_winrate",
    "home_recent_gd", "away_recent_gd",
    "form_diff", "h2h_winrate", "home_advantage",
]


def load_features(path: Path):
    df = pd.read_csv(path, parse_dates=["date"])

    y = df[TARGET]
    X = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

    cat_cols = [c for c in CAT_COLS if c in X.columns]
    num_cols = [c for c in NUM_COLS if c in X.columns]

    # Drop any remaining string columns not explicitly handled
    stray_str = [c for c in X.columns if c not in cat_cols + num_cols and X[c].dtype == object]
    X = X.drop(columns=stray_str)

    for col in cat_cols:
        X[col] = X[col].astype(str)

    return X[cat_cols + num_cols], y, num_cols, cat_cols


def build_pipeline(num_cols, cat_cols, classifier):
    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ])
    return Pipeline([("preprocessor", preprocessor), ("clf", classifier)])


def evaluate(name, pipeline, X_test, y_test):
    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"\n{'='*40}\n{name}  —  Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds, target_names=["away_win", "draw", "home_win"]))
    return acc


def train():
    X, y, num_cols, cat_cols = load_features(DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
    }

    best_acc, best_pipeline, best_name = 0.0, None, ""

    for name, clf in models.items():
        pipeline = build_pipeline(num_cols, cat_cols, clf)
        pipeline.fit(X_train, y_train)
        acc = evaluate(name, pipeline, X_test, y_test)
        if acc > best_acc:
            best_acc, best_pipeline, best_name = acc, pipeline, name

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(best_pipeline, f)

    print(f"\nBest model: {best_name} ({best_acc:.4f}) — saved to {model_path}")


if __name__ == "__main__":
    train()
