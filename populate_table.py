from espn_api import Games, populate_schedule
import sqlite3

conn = sqlite3.connect("test.db")
schedule = populate_schedule()

conn.execute("""CREATE TABLE IF NOT EXISTS schedule (id INTEGER PRIMARY KEY, week INTEGER NOT NULL, teams STRING NOT NULL, date STRING NOT NULL, time STRING NOT NULL, info STRING NOT NULL);""")

for i in range(len(schedule)):
    for j in range(len(schedule[i])):
        s = schedule[i][j]
        conn.execute("""INSERT INTO schedule (week, teams, date, time, info) VALUES (?, ?, ?, ?, ?);""", (s.eventNum, s.teamNames, s.date, s.time, s.scores))




