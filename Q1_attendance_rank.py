#Wie groß ist der Abstand zum nächsten Verein?  

import sqlite3
import pandas as pd

connect= sqlite3.connect("sponsor.db")

query="""
SELECT club_name, avg_attendance, RANK()OVER(ORDER BY avg_attendance DESC)AS attendance_rank, avg_attendance- LEAD(avg_attendance,1)OVER(ORDER BY avg_attendance DESC)  AS gap_to_club_below 
FROM dim_club AS dim
LEFT JOIN fact_season AS fac
ON dim.club_id= fac.club_id
ORDER BY avg_attendance DESC
"""
print(pd.read_sql(query, connect))