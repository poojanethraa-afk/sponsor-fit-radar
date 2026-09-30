from load import load_data

data= load_data()
dim_club= data["dim_club"]
dim_sponsor= data["dim_sponsor"]
fact_season= data["fact_season"]
fact_sponsorship= data["fact_sponsorship"]
fact_pageviews= data["fact_pageviews"]

checks= []
for name,df in data.items():
    missing= df.isna().sum().sum()
    checks.append((f"Missing values in {name}", missing ))
    
for name,df in data.items():
    duplicate= df.duplicated().sum()
    checks.append((f"Duplicate Values in {name}", duplicate))

season= fact_season.merge(dim_club, on="club_id")

over_capacity= (season["capacity"]< season["avg_attendance"]).sum()
checks.append(("Attendance above capacity", over_capacity))

invalid_points= (~season["points"].between(0,102)).sum()
checks.append(("Points outside 0-102", invalid_points))

invalid_europe = (~season["europe"].isin(["CL", "EL", "ECL", "none"])).sum()
checks.append(("Invalid europe values", invalid_europe))   

unknown_sponsors = (~fact_sponsorship["sponsor_id"].isin(dim_sponsor["sponsor_id"])).sum()
checks.append(("Unknown sponsor_id in fact_sponsorship", unknown_sponsors))

for name in ["fact_season", "fact_sponsorship", "fact_pageviews"]:
    unknown_clubs = (~data[name]["club_id"].isin(dim_club["club_id"])).sum()
    checks.append((f"Unknown club_id in {name}", unknown_clubs))

for check_name, problems in checks:
    status = "PASS" if problems == 0 else "FAIL"
    print(f"{status} - {check_name}: {problems}")