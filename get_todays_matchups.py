from nba_api.stats.endpoints import ScheduleLeagueV2
from nba_api.stats.static import teams
from datetime import date
import pandas as pd


def main():
    today = date.today().strftime('%m/%d/%Y %H:%M:%S')
    schedule = ScheduleLeagueV2(season='2025-26').get_data_frames()[0]
    schedule = schedule[schedule['gameDate'] == today]
    matchups = [(i[-6:-3], i[-3:]) for i in schedule['gameCode'].tolist()]
    return matchups

if __name__ == '__main__':
    matchups = main()





