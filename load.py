import pandas as pd


def load_data():
    dim_club = pd.read_csv("data/dim_club.csv")
    dim_sponsor = pd.read_csv("data/dim_sponsor.csv")
    fact_season = pd.read_csv("data/fact_club_season.csv")
    fact_sponsorship = pd.read_csv("data/fact_club_sponsorship.csv")
    fact_pageviews = pd.read_csv("data/fact_pageviews_monthly.csv")

    return {
        "dim_club": dim_club,
        "dim_sponsor": dim_sponsor,
        "fact_season": fact_season,
        "fact_sponsorship": fact_sponsorship,
        "fact_pageviews": fact_pageviews,
    }


if __name__ == "__main__":
    data = load_data()
    for name, df in data.items():
        print(name, len(df))