from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import OutputType
from datetime import date
import json

class BasketballStats:
    def __init__(self, client, output_format, current_date):
        self.client = client
        self.output_format = output_format
        self.current_date = current_date

    def daily_player_stats(self):
        daily_stats_raw = self.client.player_box_scores(
            day=self.current_date.day, 
            month=self.current_date.month, 
            year=self.current_date.year, 
            output_type=self.output_format
        )

        return json.loads(daily_stats_raw)

    def daily_team_stats(self):
        team_stats_raw = self.client.team_box_scores(
            day=self.current_date.day,
            month=self.current_date.month,
            year=self.current_date.year,
            output_type=self.output_format
        )
        return json.loads(team_stats_raw)

    def specific_player_stats(self, player_name):

        all_players_stats = self.daily_player_stats()
        return [stat for stat in all_players_stats if player_name in stat['name']]

    def specific_team_stats(self, team_name):
        all_teams_stats = self.daily_team_stats()
        return [stat for stat in all_teams_stats if team_name in stat['team']]
    
    def season_standings(self):
        standings_raw = self.client.standings(
            season_end_year=self.current_date.year, 
            output_type=self.output_format
            )
        return json.loads(standings_raw)

    def team_season_record(self, team_name):
        standings = self.season_standings()
        print(team_name)
        for record in standings:
            if team_name.lower() in record['team'].lower():
                return record
        return {}

if __name__ == "__main__":
    stats_scraper = BasketballStats(client, OutputType.JSON, date.today())
    
    # 일일 선수 통계
    player_daily_stats = stats_scraper.daily_player_stats()
    print("오늘의 선수 통계:", player_daily_stats)
    
    # 일일 팀 통계
    team_daily_stats = stats_scraper.daily_team_stats()
    print("오늘의 팀 통계:", team_daily_stats)
    
    # 특정 선수 통계
    # 예시로 "LeBron James" 사용 (실제 이름은 데이터에 따라 다를 수 있음)
    specific_player_stats = stats_scraper.specific_player_stats("LeBron James")
    print("LeBron James의 통계:", specific_player_stats)
    
    # 특정 팀 통계
    # 예시로 "ATLANTA HAWKS" 사용 (실제 이름은 데이터에 따라 다를 수 있음)
    specific_team_stats = stats_scraper.specific_team_stats("ATLANTA HAWKS")
    print("ATLANTA HAWKS의 통계:", specific_team_stats)
    
    # 시즌 순위
    season_standings = stats_scraper.season_standings(2019)
    print("2019 시즌 순위:", season_standings)
    
    # 특정 팀의 시즌 기록
    lakers_record = stats_scraper.team_season_record("ATLANTA HAWKS", 2019)
    print("ATLANTA HAWKS 2019 기록:", lakers_record)
