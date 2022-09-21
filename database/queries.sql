/* cat filename.sql | sqlite3 movies.db */


/* Find week that team 1 and 16 play */
SELECT schedules.week_number FROM schedules
JOIN teams AS t1 ON t1.id = schedules.source_team_id
JOIN teams AS t2 ON t2.id = schedules.opponent_id
WHERE schedules.source_team_id = 1 AND schedules.opponent_id = 16;


/* Get names of opponent team and source team */
SELECT DISTINCT t1.name, t2.name 
FROM schedules s
LEFT JOIN teams t1 ON t1.id = s.source_team_id
LEFT JOIN teams t2 ON t2.id = s.opponent_id
WHERE s.week_number = 2 AND s.event_number = 1;
