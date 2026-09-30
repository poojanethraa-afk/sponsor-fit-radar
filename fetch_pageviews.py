import csv
from urllib.parse import quote

import requests

# German Wikipedia article title per club
TITLES = {
    "BVB": "Borussia_Dortmund",
    "FCB": "FC_Bayern_München",
    "VFB": "VfB_Stuttgart",
    "SGE": "Eintracht_Frankfurt",
    "HSV": "Hamburger_SV",
    "BMG": "Borussia_Mönchengladbach",
    "KOE": "1._FC_Köln",
    "RBL": "RB_Leipzig",
    "SVW": "Werder_Bremen",
    "SCF": "SC_Freiburg",
    "M05": "1._FSV_Mainz_05",
    "B04": "Bayer_04_Leverkusen",
    "FCA": "FC_Augsburg",
    "STP": "FC_St._Pauli",
    "TSG": "TSG_1899_Hoffenheim",
    "WOB": "VfL_Wolfsburg",
    "FCU": "1._FC_Union_Berlin",
    "FCH": "1._FC_Heidenheim",
}
URL = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
       "de.wikipedia/all-access/user/{}/monthly/20250801/20260531")
HEADERS = {"User-Agent": "sponsor-fit-radar/0.1 (portfolio project)"}


def fetch_pageviews():
    rows = []
    for club_id, title in TITLES.items():
        response = requests.get(URL.format(quote(title, safe="")), headers=HEADERS, timeout=30)
        response.raise_for_status()
        for item in response.json()["items"]:
            ts = item["timestamp"]
            rows.append({
                "club_id": club_id,
                "season": "2025/26",
                "month": f"{ts[:4]}-{ts[4:6]}",
                "pageviews": item["views"],
            })
    return rows


if __name__ == "__main__":
    rows = fetch_pageviews()
    with open("data/fact_pageviews_monthly.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["club_id", "season", "month", "pageviews"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to data/fact_pageviews_monthly.csv")
