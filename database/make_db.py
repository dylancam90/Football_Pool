import csv, sqlite3

TOTAL_WEEKS = 18

conn = sqlite3.connect("test.db")
cur = conn.cursor()

conn.execute("""CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY NOT NULL, \
                                    name TEXT NOT NULL, \
                                    abbreviation TEXT NOT NULL, \
                                    conference TEXT NOT NULL, \
                                    division TEXT NOT NULL)""")

conn.execute("""CREATE TABLE IF NOT EXISTS schedules (event_number INTEGER NOT NULL, \
                                    week_number INTEGER NOT NULL, \
                                    source_team_id INTEGER NOT NULL, \
                                    opponent_id INTEGER, \
                                    location TEXT NOT NULL, \
                                    FOREIGN KEY(source_team_id) REFERENCES teams(id), \
                                    FOREIGN KEY(opponent_id) REFERENCES teams(id))""")

# turn csv into list for easier access
def file_list(filename):
    with open(filename, newline="") as open_file:
        reader = csv.DictReader(open_file)
        obj_list = [i for i in reader]
        return obj_list

# insert teams list into teams DB
def insert_teams(teams_list):
    for i in teams_list:
        name = i["Name"]
        abbreviation = i["Abbreviation"]
        conference = i["Conference"]
        division = i["Division"]
        conn.execute("INSERT INTO teams (name, abbreviation, conference, division) VALUES (?, ?, ?, ?)", (name, abbreviation, conference, division))
    conn.commit()


# for team_schedule table that shows every teams schedule per weekly basis
def team_schedule_list(schedules_list, teams_list, week):
    list = []
    week_number = week[1:]

    for game_num, sch in enumerate(schedules_list):
        weeks = dict()

        source_team = sch["Team"]
        opponent_teams = sch[week]
        weeks['event_number'] = game_num + 1

        for t in teams_list:

            weeks["week_number"] = int(week_number)
            if t["Abbreviation"] in opponent_teams or opponent_teams == "BYE":
                if opponent_teams[0] == "@":
                    weeks["location"] = "Away"
                else:
                    weeks["location"] = "Home"

                # have to check for BYE seperatley
                if opponent_teams == "BYE":
                    weeks["location"] = "BYE"
                else:
                    opponent_id = t["ID"]
                    #weeks["opponent_team"] = opponent_teams
                    weeks["opponent_id"] = opponent_id  

            if t["Abbreviation"] in source_team:
                source_team_id = t["ID"]
                #weeks["source_team"] = source_team
                weeks["source_team_id"] = int(source_team_id)

        list.append(weeks)
        
    return list


# loops through team_schedule list to get list of all teams in 18 weeks of the season 
def full_schedule_list(schedules, teams, weeks):
    games = []
    for i in range(1, weeks + 1):
        s = "W"
        week = s + str(i)
        games.append(team_schedule_list(schedules, teams, week))
    return games


# prints all weeks returned from all_temas_schedule
def print_all_teams_schedule(teams_schedule):
    for i in range(len(teams_schedule)):
        for j in teams_schedule[i]:
            print(j)


# insert teams_schedule into schedules DB
def insert_schedules(schedules):
    for i in range(len(schedules)):
        for j in schedules[i]:
            # event_number, week_number, source_team_id, location, opponent_id
            try: 
                conn.execute("""INSERT INTO schedules (event_number, week_number, source_team_id, location, opponent_id) VALUES (?, ?, ?, ?, ?)""", (j["event_number"], j["week_number"], j["source_team_id"], j["location"], j["opponent_id"]))
            except KeyError:
                conn.execute("""INSERT INTO schedules (event_number, week_number, source_team_id, location) VALUES (?, ?, ?, ?)""", (j["event_number"], j["week_number"], j["source_team_id"], "BYE"))
    conn.commit()

def main():
    schedules = file_list("nfl_2022_schedule.csv")
    teams = file_list("nfl_teams.csv")
    teams_schedule = full_schedule_list(schedules, teams, TOTAL_WEEKS)
    


if __name__ == "__main__":
    main()

    '''FIGURE OUT HOW TO QUERY TABLE'''

    '''
                            COMMMENTS
        # IF DB NEEDS TO BE MADE AGAIN RE-RUN THESE LINES
            #insert_schedules(teams_schedule)
            #insert_teams(teams)

        # use this to print 1 week
            #print(team_schedule_list(schedules, teams, "W13"))
            #l = team_schedule_list(schedules, teams, "W13")[0]["week_number"]

        # use this to print all
            #print_all_teams_schedule(teams_schedule)

        #THIS IS WHAT A QUERY TO THE DATABASE LOOKS LIKE

            #cur.execute("SELECT * FROM schedules where week_number = ?", (13, ))
            
            for i in cur:
                print(i)

    '''









