import requests
import json




class Top_Plays:

    def get_top_plays(self, page):
        try:
            base_url = "https://nextgenstats.nfl.com/stats/top-plays/"
            response = requests.get(base_url + page)
            response.raise_for_status()
            api_data = response.json()
        except requests.exceptions.RequestException as err:
            print(f"Error fetching api data: {err}")
        else:
            return api_data

    def get_fastest_ball_carrier(self, year=2025):
        postfix = f"/{year}/REG/all"
        page = f"fastest-ball-carriers"+postfix
        api_data = self.get_top_plays(page)


    def get_longest_plays(self, year=2025):
        postfix = f"/{year}/REG/all"
        page = f"longest-plays"+postfix
        api_data = self.get_top_plays(page)

    def get_fastest_sacks(self, year=2025):
        postfix = f"/{year}/REG/all"
        page = f"fastest-sacks"+postfix
        api_data = self.get_top_plays(page)

    def get_longest_tackles(self, year=2025):
        postfix = f"/{year}/REG/all"
        page = f"longest-tackles" + postfix
        api_data = self.get_top_plays(page)

    def get_improbably_completions(self, year=2025):
        postfix = f"/{year}/REG/all"
        page = f"improbably-completions"+postfix
        api_data = self.get_top_plays(page)

    def get_incredible_YAC(self, year=2025):
        postfix = f"/{year}/REG/all"
        page = f"incredible-YAC"+postfix
        api_data = self.get_top_plays(page)

    def get_remarkable_rushes(self, year=2025):
        postfix = f"/{year}/REG/all"
        page = f"remarkable-rushes"+postfix
        api_data = self.get_top_plays(page)
