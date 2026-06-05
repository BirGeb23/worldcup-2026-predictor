import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st

st.set_page_config(
    page_title="2026 World Cup Predictor",
    page_icon="🏆",
    layout="centered",
)

pg = st.navigation(
    [
        st.Page("pages/1_Fixtures.py",  title="Fixtures",  url_path="fixtures"),
        st.Page("pages/2_Standings.py", title="Standings", url_path="standings"),
        st.Page("pages/predictor.py",   title="Predictor", default=True),
    ],
    position="sidebar",
)
pg.run()
