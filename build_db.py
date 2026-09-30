import sqlite3
from load import load_data

data= load_data()
connection= sqlite3.connect("sponsor.db")

for name,df in data.items():
    df.to_sql(name, connection, if_exists="replace", index=False)
    print(f"Loaded {name}: {len(df)} rows")

connection.close()
print("Database sponsor.db created.")