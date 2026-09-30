#Rank all clubs by average attendance. Show club_name, avg_attendance, attendance_rank
import sqlite3
import pandas as pd

connection= sqlite3.connect("sponsor.db")
query= """
SELECT club_name, avg_attendance, RANK() OVER(ORDER BY avg_attendance DESC) AS attendance_rank
FROM dim_club AS dim
LEFT JOIN fact_season AS fac
ON dim.club_id= fac.club_id
ORDER BY attendance_rank
"""
print(pd.read_sql(query, connection))