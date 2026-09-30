# Sponsor Fit Radar

**Which Bundesliga club offers a sponsor the most value?**
*Welcher Bundesliga-Verein bietet einem Sponsor den größten Mehrwert?*

A small end-to-end BI project: public data on the Bundesliga season 2025/26 is collected, quality-checked in Python, queried with SQL and turned into an interactive Power BI dashboard. Its core is the **Sponsor Fit Score**: a salesperson sets what matters to their sponsor with five sliders, and the club ranking updates live.

## The question

Every sponsor has different goals. The radar compares all 18 clubs on five criteria:

| Criterion | Measures | Sponsor question |
|---|---|---|
| Attendance | Average spectators per home game | How many people see my brand live? |
| Utilization | Attendance ÷ stadium capacity | Is the stadium full? |
| Points | Points in the season | Is the club successful? |
| Europe | Champions League = 3, Europa League = 2, Conference League = 1 | Will my brand be seen internationally? |
| Online | Monthly Wikipedia page views | How much attention does the club get online? |

## Pipeline

```
Wikipedia / Wikimedia API → CSV → Python (load + 17 quality checks) → SQLite + SQL → Power BI
```

| File | Purpose |
|---|---|
| `data/` | The five CSV tables (see data model) |
| `fetch_pageviews.py` | Downloads monthly page views from the Wikimedia API |
| `load.py` | Loads all tables with pandas (`load_data()`) |
| `quality.py` | 17 automatic data quality checks |
| `build_db.py` | Writes the tables into a SQLite database (`sponsor.db`) |
| `Q1_attendance_rank.py`, `Q_Online_Interest.py` | SQL queries with window functions (`RANK`, `LEAD`) |
| `Sponsor_dashboard.pbix` | Power BI report: Club Overview + Sponsor Fit Radar |

## Data model

A star schema (more precisely a galaxy schema: three fact tables share `dim_club`).

| Table | Content | Rows |
|---|---|---|
| `dim_club` | Club, city, stadium, capacity | 18 |
| `dim_sponsor` | Sponsor and industry | 44 |
| `fact_club_season` | Attendance, points, European competition, relegation | 18 |
| `fact_club_sponsorship` | Which sponsor at which club (shirt, sleeve, kit) | 54 |
| `fact_pageviews_monthly` | Wikipedia page views per club and month | 180 |

All relationships are one-to-many via `club_id` and `sponsor_id`.

## Data quality

`quality.py` runs 17 checks in four categories and counts the failing rows for each:

- **Completeness** – missing values in every table
- **Uniqueness** – duplicate rows in every table
- **Validity** – attendance ≤ capacity, points between 0 and 102, valid Europe values
- **Referential integrity** – every `club_id` and `sponsor_id` exists in its dimension

## Sponsor Fit Score (Power BI)

1. **Normalize** each criterion to 0–1 with min-max scaling (DAX: `MINX` / `MAXX` over `ALL(dim_club)`), so 80,000 spectators and 70 points are comparable.
2. **Weight** each criterion with a what-if parameter slider (0–10).
3. **Score** = weighted average × 100 → a ranking from 0 to 100 that changes live.

**Limitation:** min-max scaling can exaggerate small differences (utilization only ranges from 87% to 100%). Rank-based scores would be worth testing.

## Selected findings

- Dortmund (81,285) and Bayern (75,000) lead attendance by far; the gap from 2nd to 3rd is 15,559 spectators.
- Average stadium utilization is 97.5%. Hamburger SV reached 99.9% despite finishing 13th.
- VfL Wolfsburg had the 5th-highest online interest despite being relegated.
- Insurance is the most common industry among shirt and sleeve sponsors (5 of 36).

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python quality.py
python build_db.py
python Q1_attendance_rank.py
```

Open `Sponsor_dashboard.pbix` in Power BI Desktop. If the CSV paths differ on your machine, update them under *Transform data → Data source settings*.

## Data sources and license

- Wikipedia: [Fußball-Bundesliga 2025/26](https://de.wikipedia.org/wiki/Fußball-Bundesliga_2025/26) and [2025–26 Bundesliga](https://en.wikipedia.org/wiki/2025–26_Bundesliga), licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The CSV files derived from them are shared under the same license.
- [Wikimedia Pageviews API](https://wikimedia.org/api/rest_v1/) (German Wikipedia, August 2025 – May 2026).
- The industry classification of sponsors is my own.

This is a personal portfolio project and not affiliated with any club, league or agency.
