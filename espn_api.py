import requests, json
from datetime import datetime

WEEKS = 17

class Games:    #scores
    def __init__(self, eventNum, teamNames, date, homeTeam):
        self.eventNum = eventNum
        self.teamNames = teamNames 
        self.date = date
        self.homeTeam = homeTeam
        '''this is a massive object that cant possibly fit in a db column'''
        #self.scores = scores

        self._format_date()

    ''' default date is dateTtime it just splits them both into instance variables at object initialization '''
    def _format_date(self):
        split = self.date.split("T")
        self.date = split[0]
        self.time = split[1][:-1]

    def get_time(self):
        return self.time
    
    def __repr__(self):
        return "{} \t Date: {}".format(self.teamNames, self.date)


def populate_schedule():
    schedule = [[] for i in range(WEEKS)]
    week_num = 1

    ''' loops through all weeks of NFL schedule and turns them into objects 
        and then appends them to a list to be returned by function'''

    while week_num <= WEEKS:
        r = requests.get('http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week=' + str(week_num))
        response = r.json()

        ''' not sure what I am doing with these yet but thought I might need them'''
        season = response['season']['year']
        week = response['week']['number']

        events = response["events"]

        for eventNum in range(len(events)):
            teamNames = events[eventNum]['name']
            date = events[eventNum]['date']
            #scores = events[eventNum]['competitions'][0]['competitors']
            homeTeam = events[eventNum]['competitions'][0]['competitors'][0]["homeAway"]
            schedule[week_num-1].append(Games(eventNum, teamNames, date, homeTeam)) #scores

        week_num += 1
    
    return schedule


if __name__ == "__main__":
    schedule = populate_schedule()








'''
import requests, json
from datetime import datetime

WEEKS = 17

class Games:
    def __init__(self, eventNum, teamNames, date, scores):
        self.eventNum = eventNum
        self.teamNames = teamNames 
        self.date = date
        self.scores = scores

        self._format_date()

    def _format_date(self):
        split = self.date.split("T")
        self.date = split[0]
        self.time = split[1][:-1]

    def get_time(self):
        return self.time
    
    def __repr__(self):
        return "{} \t Date: {}".format(self.teamNames, self.date)


def populate_schedule():
    schedule = [[] for i in range(WEEKS)]
    week_num = 1

    while week_num <= WEEKS:
        r = requests.get('http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?week=' + str(week_num))
        response = r.json()

        season = response['season']['year']
        week = response['week']['number']
        events = response["events"]

        for eventNum in range(len(events)):
            teamNames = events[eventNum]['name']
            date = events[eventNum]['date']
            scores = events[eventNum]['competitions'][0]['competitors']
            schedule[week_num-1].append(Games(eventNum, teamNames, date, scores))

        week_num += 1
    
    return schedule

schedule = populate_schedule()

'''