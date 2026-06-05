"""
2026 FIFA World Cup — Official Group Stage Fixtures
72 matches, 11 June – 27 June 2026 (group stage only).

Source: official FIFA schedule.
Team names are normalised to match TEAM_LOGOS keys.
Matchday is auto-assigned (first 2 group appearances = MD1, next 2 = MD2, last 2 = MD3).
"""

from collections import defaultdict

# ── Name normalisation: JSON name → TEAM_LOGOS key ────────────────────────────
_TEAM = {
    "Korea Republic": "South Korea",
    "USA":            "United States",
    "IR Iran":        "Iran",
    "Congo DR":       "DR Congo",
}

# ── Month abbreviation → zero-padded number ───────────────────────────────────
_MONTH = {
    "January": "01", "February": "02", "March": "03",   "April":    "04",
    "May":     "05", "June":     "06", "July":   "07",   "August":   "08",
    "September":"09","October": "10", "November":"11",   "December": "12",
}

# ── City → local timezone abbreviation ───────────────────────────────────────
_TZ = {
    "Mexico City": "CT",  "Guadalajara": "CT",  "Monterrey": "CT",
    "Toronto":     "ET",  "Vancouver":   "PT",
    "Seattle":     "PT",  "Los Angeles": "PT",  "San Francisco Bay Area": "PT",
    "Houston":     "CT",  "Dallas":      "CT",  "Kansas City": "CT",
    "New Jersey":  "ET",  "Philadelphia":"ET",  "Boston": "ET",
    "Miami":       "ET",  "Atlanta":     "ET",
}

# ── City → host country ───────────────────────────────────────────────────────
_COUNTRY = {
    "Mexico City": "Mexico",  "Guadalajara": "Mexico",  "Monterrey": "Mexico",
    "Toronto":     "Canada",  "Vancouver":   "Canada",
}


def _iso(date_str: str) -> str:
    """'Thursday 11 June 2026' → '2026-06-11'"""
    _, day, month, year = date_str.split()
    return f"{year}-{_MONTH[month]}-{day.zfill(2)}"


# ── Raw data (official FIFA schedule, field names preserved) ──────────────────
_RAW: list[dict] = [
    {"Date": "Thursday 11 June 2026",   "Time": "15:00", "Team 1": "Mexico",       "Team 2": "South Africa",           "Group": "Group A", "Stadium": "Mexico City Stadium",          "City": "Mexico City"},
    {"Date": "Thursday 11 June 2026",   "Time": "22:00", "Team 1": "Korea Republic","Team 2": "Czechia",                "Group": "Group A", "Stadium": "Guadalajara Stadium",           "City": "Guadalajara"},
    {"Date": "Friday 12 June 2026",     "Time": "15:00", "Team 1": "Canada",        "Team 2": "Bosnia and Herzegovina", "Group": "Group B", "Stadium": "Toronto Stadium",               "City": "Toronto"},
    {"Date": "Friday 12 June 2026",     "Time": "21:00", "Team 1": "USA",           "Team 2": "Paraguay",               "Group": "Group D", "Stadium": "Los Angeles Stadium",           "City": "Los Angeles"},
    {"Date": "Saturday 13 June 2026",   "Time": "15:00", "Team 1": "Qatar",         "Team 2": "Switzerland",            "Group": "Group B", "Stadium": "San Francisco Bay Area Stadium","City": "San Francisco Bay Area"},
    {"Date": "Saturday 13 June 2026",   "Time": "18:00", "Team 1": "Brazil",        "Team 2": "Morocco",                "Group": "Group C", "Stadium": "New York/New Jersey Stadium",   "City": "New Jersey"},
    {"Date": "Saturday 13 June 2026",   "Time": "21:00", "Team 1": "Haiti",         "Team 2": "Scotland",               "Group": "Group C", "Stadium": "Boston Stadium",                "City": "Boston"},
    {"Date": "Sunday 14 June 2026",     "Time": "00:00", "Team 1": "Australia",     "Team 2": "Türkiye",                "Group": "Group D", "Stadium": "BC Place Vancouver",            "City": "Vancouver"},
    {"Date": "Sunday 14 June 2026",     "Time": "13:00", "Team 1": "Germany",       "Team 2": "Curaçao",                "Group": "Group E", "Stadium": "Houston Stadium",               "City": "Houston"},
    {"Date": "Sunday 14 June 2026",     "Time": "16:00", "Team 1": "Netherlands",   "Team 2": "Japan",                  "Group": "Group F", "Stadium": "Dallas Stadium",                "City": "Dallas"},
    {"Date": "Sunday 14 June 2026",     "Time": "19:00", "Team 1": "Côte d'Ivoire", "Team 2": "Ecuador",                "Group": "Group E", "Stadium": "Philadelphia Stadium",          "City": "Philadelphia"},
    {"Date": "Sunday 14 June 2026",     "Time": "22:00", "Team 1": "Sweden",        "Team 2": "Tunisia",                "Group": "Group F", "Stadium": "Monterrey Stadium",             "City": "Monterrey"},
    {"Date": "Monday 15 June 2026",     "Time": "12:00", "Team 1": "Spain",         "Team 2": "Cabo Verde",             "Group": "Group H", "Stadium": "Atlanta Stadium",               "City": "Atlanta"},
    {"Date": "Monday 15 June 2026",     "Time": "15:00", "Team 1": "Belgium",       "Team 2": "Egypt",                  "Group": "Group G", "Stadium": "Seattle Stadium",               "City": "Seattle"},
    {"Date": "Monday 15 June 2026",     "Time": "18:00", "Team 1": "Saudi Arabia",  "Team 2": "Uruguay",                "Group": "Group H", "Stadium": "Miami Stadium",                 "City": "Miami"},
    {"Date": "Monday 15 June 2026",     "Time": "21:00", "Team 1": "IR Iran",       "Team 2": "New Zealand",            "Group": "Group G", "Stadium": "Los Angeles Stadium",           "City": "Los Angeles"},
    {"Date": "Tuesday 16 June 2026",    "Time": "15:00", "Team 1": "France",        "Team 2": "Senegal",                "Group": "Group I", "Stadium": "New York/New Jersey Stadium",   "City": "New Jersey"},
    {"Date": "Tuesday 16 June 2026",    "Time": "18:00", "Team 1": "Iraq",          "Team 2": "Norway",                 "Group": "Group I", "Stadium": "Boston Stadium",                "City": "Boston"},
    {"Date": "Tuesday 16 June 2026",    "Time": "21:00", "Team 1": "Argentina",     "Team 2": "Algeria",                "Group": "Group J", "Stadium": "Kansas City Stadium",           "City": "Kansas City"},
    {"Date": "Wednesday 17 June 2026",  "Time": "00:00", "Team 1": "Austria",       "Team 2": "Jordan",                 "Group": "Group J", "Stadium": "San Francisco Bay Area Stadium","City": "San Francisco Bay Area"},
    {"Date": "Wednesday 17 June 2026",  "Time": "13:00", "Team 1": "Portugal",      "Team 2": "Congo DR",               "Group": "Group K", "Stadium": "Houston Stadium",               "City": "Houston"},
    {"Date": "Wednesday 17 June 2026",  "Time": "16:00", "Team 1": "England",       "Team 2": "Croatia",                "Group": "Group L", "Stadium": "Dallas Stadium",                "City": "Dallas"},
    {"Date": "Wednesday 17 June 2026",  "Time": "19:00", "Team 1": "Ghana",         "Team 2": "Panama",                 "Group": "Group L", "Stadium": "Toronto Stadium",               "City": "Toronto"},
    {"Date": "Wednesday 17 June 2026",  "Time": "22:00", "Team 1": "Uzbekistan",    "Team 2": "Colombia",               "Group": "Group K", "Stadium": "Mexico City Stadium",           "City": "Mexico City"},
    {"Date": "Thursday 18 June 2026",   "Time": "12:00", "Team 1": "Czechia",       "Team 2": "South Africa",           "Group": "Group A", "Stadium": "Atlanta Stadium",               "City": "Atlanta"},
    {"Date": "Thursday 18 June 2026",   "Time": "15:00", "Team 1": "Switzerland",   "Team 2": "Bosnia and Herzegovina", "Group": "Group B", "Stadium": "Los Angeles Stadium",           "City": "Los Angeles"},
    {"Date": "Thursday 18 June 2026",   "Time": "18:00", "Team 1": "Canada",        "Team 2": "Qatar",                  "Group": "Group B", "Stadium": "BC Place Vancouver",            "City": "Vancouver"},
    {"Date": "Thursday 18 June 2026",   "Time": "21:00", "Team 1": "Mexico",        "Team 2": "Korea Republic",         "Group": "Group A", "Stadium": "Guadalajara Stadium",           "City": "Guadalajara"},
    {"Date": "Friday 19 June 2026",     "Time": "15:00", "Team 1": "USA",           "Team 2": "Australia",              "Group": "Group D", "Stadium": "Seattle Stadium",               "City": "Seattle"},
    {"Date": "Friday 19 June 2026",     "Time": "18:00", "Team 1": "Scotland",      "Team 2": "Morocco",                "Group": "Group C", "Stadium": "Boston Stadium",                "City": "Boston"},
    {"Date": "Friday 19 June 2026",     "Time": "20:30", "Team 1": "Brazil",        "Team 2": "Haiti",                  "Group": "Group C", "Stadium": "Philadelphia Stadium",          "City": "Philadelphia"},
    {"Date": "Friday 19 June 2026",     "Time": "23:00", "Team 1": "Türkiye",       "Team 2": "Paraguay",               "Group": "Group D", "Stadium": "San Francisco Bay Area Stadium","City": "San Francisco Bay Area"},
    {"Date": "Saturday 20 June 2026",   "Time": "13:00", "Team 1": "Netherlands",   "Team 2": "Sweden",                 "Group": "Group F", "Stadium": "Houston Stadium",               "City": "Houston"},
    {"Date": "Saturday 20 June 2026",   "Time": "16:00", "Team 1": "Germany",       "Team 2": "Côte d'Ivoire",          "Group": "Group E", "Stadium": "Toronto Stadium",               "City": "Toronto"},
    {"Date": "Saturday 20 June 2026",   "Time": "20:00", "Team 1": "Ecuador",       "Team 2": "Curaçao",                "Group": "Group E", "Stadium": "Kansas City Stadium",           "City": "Kansas City"},
    {"Date": "Sunday 21 June 2026",     "Time": "00:00", "Team 1": "Tunisia",       "Team 2": "Japan",                  "Group": "Group F", "Stadium": "Monterrey Stadium",             "City": "Monterrey"},
    {"Date": "Sunday 21 June 2026",     "Time": "12:00", "Team 1": "Spain",         "Team 2": "Saudi Arabia",           "Group": "Group H", "Stadium": "Atlanta Stadium",               "City": "Atlanta"},
    {"Date": "Sunday 21 June 2026",     "Time": "15:00", "Team 1": "Belgium",       "Team 2": "IR Iran",                "Group": "Group G", "Stadium": "Los Angeles Stadium",           "City": "Los Angeles"},
    {"Date": "Sunday 21 June 2026",     "Time": "18:00", "Team 1": "Uruguay",       "Team 2": "Cabo Verde",             "Group": "Group H", "Stadium": "Miami Stadium",                 "City": "Miami"},
    {"Date": "Sunday 21 June 2026",     "Time": "21:00", "Team 1": "New Zealand",   "Team 2": "Egypt",                  "Group": "Group G", "Stadium": "BC Place Vancouver",            "City": "Vancouver"},
    {"Date": "Monday 22 June 2026",     "Time": "13:00", "Team 1": "Argentina",     "Team 2": "Austria",                "Group": "Group J", "Stadium": "Dallas Stadium",                "City": "Dallas"},
    {"Date": "Monday 22 June 2026",     "Time": "17:00", "Team 1": "France",        "Team 2": "Iraq",                   "Group": "Group I", "Stadium": "Philadelphia Stadium",          "City": "Philadelphia"},
    {"Date": "Monday 22 June 2026",     "Time": "20:00", "Team 1": "Norway",        "Team 2": "Senegal",                "Group": "Group I", "Stadium": "New York/New Jersey Stadium",   "City": "New Jersey"},
    {"Date": "Monday 22 June 2026",     "Time": "23:00", "Team 1": "Jordan",        "Team 2": "Algeria",                "Group": "Group J", "Stadium": "San Francisco Bay Area Stadium","City": "San Francisco Bay Area"},
    {"Date": "Tuesday 23 June 2026",    "Time": "13:00", "Team 1": "Portugal",      "Team 2": "Uzbekistan",             "Group": "Group K", "Stadium": "Houston Stadium",               "City": "Houston"},
    {"Date": "Tuesday 23 June 2026",    "Time": "16:00", "Team 1": "England",       "Team 2": "Ghana",                  "Group": "Group L", "Stadium": "Boston Stadium",                "City": "Boston"},
    {"Date": "Tuesday 23 June 2026",    "Time": "19:00", "Team 1": "Panama",        "Team 2": "Croatia",                "Group": "Group L", "Stadium": "Toronto Stadium",               "City": "Toronto"},
    {"Date": "Tuesday 23 June 2026",    "Time": "22:00", "Team 1": "Colombia",      "Team 2": "Congo DR",               "Group": "Group K", "Stadium": "Guadalajara Stadium",           "City": "Guadalajara"},
    {"Date": "Wednesday 24 June 2026",  "Time": "15:00", "Team 1": "Switzerland",   "Team 2": "Canada",                 "Group": "Group B", "Stadium": "BC Place Vancouver",            "City": "Vancouver"},
    {"Date": "Wednesday 24 June 2026",  "Time": "15:00", "Team 1": "Bosnia and Herzegovina","Team 2": "Qatar",          "Group": "Group B", "Stadium": "Seattle Stadium",               "City": "Seattle"},
    {"Date": "Wednesday 24 June 2026",  "Time": "18:00", "Team 1": "Scotland",      "Team 2": "Brazil",                 "Group": "Group C", "Stadium": "Miami Stadium",                 "City": "Miami"},
    {"Date": "Wednesday 24 June 2026",  "Time": "18:00", "Team 1": "Morocco",       "Team 2": "Haiti",                  "Group": "Group C", "Stadium": "Atlanta Stadium",               "City": "Atlanta"},
    {"Date": "Wednesday 24 June 2026",  "Time": "21:00", "Team 1": "Czechia",       "Team 2": "Mexico",                 "Group": "Group A", "Stadium": "Mexico City Stadium",           "City": "Mexico City"},
    {"Date": "Wednesday 24 June 2026",  "Time": "21:00", "Team 1": "South Africa",  "Team 2": "Korea Republic",         "Group": "Group A", "Stadium": "Monterrey Stadium",             "City": "Monterrey"},
    {"Date": "Thursday 25 June 2026",   "Time": "16:00", "Team 1": "Curaçao",       "Team 2": "Côte d'Ivoire",          "Group": "Group E", "Stadium": "Philadelphia Stadium",          "City": "Philadelphia"},
    {"Date": "Thursday 25 June 2026",   "Time": "16:00", "Team 1": "Ecuador",       "Team 2": "Germany",                "Group": "Group E", "Stadium": "New York/New Jersey Stadium",   "City": "New Jersey"},
    {"Date": "Thursday 25 June 2026",   "Time": "19:00", "Team 1": "Japan",         "Team 2": "Sweden",                 "Group": "Group F", "Stadium": "Dallas Stadium",                "City": "Dallas"},
    {"Date": "Thursday 25 June 2026",   "Time": "19:00", "Team 1": "Tunisia",       "Team 2": "Netherlands",            "Group": "Group F", "Stadium": "Kansas City Stadium",           "City": "Kansas City"},
    {"Date": "Thursday 25 June 2026",   "Time": "22:00", "Team 1": "Türkiye",       "Team 2": "USA",                    "Group": "Group D", "Stadium": "Los Angeles Stadium",           "City": "Los Angeles"},
    {"Date": "Thursday 25 June 2026",   "Time": "22:00", "Team 1": "Paraguay",      "Team 2": "Australia",              "Group": "Group D", "Stadium": "San Francisco Bay Area Stadium","City": "San Francisco Bay Area"},
    {"Date": "Friday 26 June 2026",     "Time": "15:00", "Team 1": "Norway",        "Team 2": "France",                 "Group": "Group I", "Stadium": "Boston Stadium",                "City": "Boston"},
    {"Date": "Friday 26 June 2026",     "Time": "15:00", "Team 1": "Senegal",       "Team 2": "Iraq",                   "Group": "Group I", "Stadium": "Toronto Stadium",               "City": "Toronto"},
    {"Date": "Friday 26 June 2026",     "Time": "20:00", "Team 1": "Cabo Verde",    "Team 2": "Saudi Arabia",           "Group": "Group H", "Stadium": "Houston Stadium",               "City": "Houston"},
    {"Date": "Friday 26 June 2026",     "Time": "20:00", "Team 1": "Uruguay",       "Team 2": "Spain",                  "Group": "Group H", "Stadium": "Guadalajara Stadium",           "City": "Guadalajara"},
    {"Date": "Friday 26 June 2026",     "Time": "23:00", "Team 1": "Egypt",         "Team 2": "IR Iran",                "Group": "Group G", "Stadium": "Seattle Stadium",               "City": "Seattle"},
    {"Date": "Friday 26 June 2026",     "Time": "23:00", "Team 1": "New Zealand",   "Team 2": "Belgium",                "Group": "Group G", "Stadium": "BC Place Vancouver",            "City": "Vancouver"},
    {"Date": "Saturday 27 June 2026",   "Time": "17:00", "Team 1": "Panama",        "Team 2": "England",                "Group": "Group L", "Stadium": "New York/New Jersey Stadium",   "City": "New Jersey"},
    {"Date": "Saturday 27 June 2026",   "Time": "17:00", "Team 1": "Croatia",       "Team 2": "Ghana",                  "Group": "Group L", "Stadium": "Philadelphia Stadium",          "City": "Philadelphia"},
    {"Date": "Saturday 27 June 2026",   "Time": "19:30", "Team 1": "Colombia",      "Team 2": "Portugal",               "Group": "Group K", "Stadium": "Miami Stadium",                 "City": "Miami"},
    {"Date": "Saturday 27 June 2026",   "Time": "19:30", "Team 1": "Congo DR",      "Team 2": "Uzbekistan",             "Group": "Group K", "Stadium": "Atlanta Stadium",               "City": "Atlanta"},
    {"Date": "Saturday 27 June 2026",   "Time": "22:00", "Team 1": "Algeria",       "Team 2": "Austria",                "Group": "Group J", "Stadium": "Kansas City Stadium",           "City": "Kansas City"},
    {"Date": "Saturday 27 June 2026",   "Time": "22:00", "Team 1": "Jordan",        "Team 2": "Argentina",              "Group": "Group J", "Stadium": "Dallas Stadium",                "City": "Dallas"},
]


def _build() -> list[dict]:
    group_counts: dict[str, int] = defaultdict(int)
    fixtures = []
    for i, r in enumerate(_RAW, 1):
        grp   = r["Group"]
        count = group_counts[grp]
        md    = 1 if count < 2 else (2 if count < 4 else 3)
        group_counts[grp] += 1

        city = r["City"]
        fixtures.append({
            "id":         f"M{i:03d}",
            "matchday":   md,
            "group":      grp,
            "stage":      f"First Stage, {grp}",
            "date":       _iso(r["Date"]),
            "kickoff":    r["Time"],
            "kickoff_tz": _TZ.get(city, ""),
            "home":       _TEAM.get(r["Team 1"], r["Team 1"]),
            "away":       _TEAM.get(r["Team 2"], r["Team 2"]),
            "stadium":    r["Stadium"],
            "city":       city,
            "country":    _COUNTRY.get(city, "United States"),
        })
    return fixtures


FIXTURES: list[dict] = _build()
