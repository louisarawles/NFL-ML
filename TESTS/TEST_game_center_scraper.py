import unittest
from NFLScrapers.GameCenter import game_center_scraper as gcs
# fake data
# **the data AFTER get_data(gs_url, headers) has been called**
game_data = [{
    'schedule': {
        'gameKey': 60165,
        'gameDate': '01/10/2026',
        'gameId': 2026011001,
        'gameTimeEastern': '20:00:00',
        'homeTeamAbbr': 'CHI',
        'homeTeamId': '0810',
        'season': 2025,
        'seasonType': 'POST',
        'visitorTeamAbbr': 'GB',
        'visitorTeamId': '1800',
        'week': 19
    },
    'passers': {
        'home': {
            'gameId': 2026011001,
            'esbId': 'WIL176897',
            'teamId': '0810',
            'teamAbbr': 'CHI',
            'shortName': 'C.Williams',
            'position': 'QB',
            'jerseyNumber': 18,
            'playerName': 'Caleb Williams',
            'zones': [
                {
                    'type': 'threeColumns',
                    'lineOfScrimmageDistance': '10To19',
                    'section': 'middleThird',
                    'attempts': 4,
                    'completionPct': 0.75,
                    'completions': 3,
                    'interceptions': 0,
                    'qbRating': 116.66666666666667,
                    'touchdowns': 0,
                    'yards': 65,
                    'qbRatingSuccessLevel': 'ABOVE'
                },
                {
                    'type': 'threeColumns',
                    'lineOfScrimmageDistance': 'losTo9',
                    'section': 'rightThird',
                    'attempts': 7,
                    'completionPct': 0.8571428571428571,
                    'completions': 6,
                    'interceptions': 0,
                    'qbRating': 104.76190476190477,
                    'touchdowns': 0,
                    'yards': 64,
                    'qbRatingSuccessLevel': 'ABOVE'
                }],
        'visitor': {
            'gameId': 2026011001,
            'esbId': 'LOV130776',
            'teamId': '1800',
            'teamAbbr': 'GB',
            'shortName': 'J.Love',
            'position': 'QB',
            'jerseyNumber': 10,
            'playerName': 'Jordan Love',
            'zones': [
                {
                    'type': 'threeColumns',
                    'lineOfScrimmageDistance': 'behindLOS',
                    'section': 'rightThird',
                    'attempts': 3,
                    'completionPct': 1,
                    'completions': 3,
                    'interceptions': 0,
                    'qbRating': 145.1388888888889,
                    'touchdowns': 1,
                    'yards': 28,
                    'qbRatingSuccessLevel': 'ABOVE'
                },
                {
                    'type': 'threeColumns',
                    'lineOfScrimmageDistance': '20Plus',
                    'section': 'leftThird',
                    'attempts': 2,
                    'completionPct': 0,
                    'completions': 0,
                    'interceptions': 0,
                    'qbRating': 39.58333333333333,
                    'touchdowns': 0,
                    'yards': 0,
                    'qbRatingSuccessLevel': 'BELOW'
                }],
                },
            'leaders': {
                'speedLeaders': {
                    'home': {
                        'gsisPlayId': 3328,
                        'esbId': 'WIL176897',
                        'jerseyNumber': 18,
                        'playerName': 'Caleb Williams',
                        'position': 'QB',
                        'shortName': 'C.Williams',
                        'teamId': '0810',
                        'maxSpeed': 19.4522727705,
                        'headshot': 'https://static.www.nfl.com/image/upload/{formatInstructions}/league/h4qs11kutwiw7whekmyt'
                    },
                    'visitor': {
                        'gsisPlayId': 474,
                        'esbId': 'REE263142',
                        'jerseyNumber': 11,
                        'playerName': 'Jayden Reed',
                        'position': 'WR',
                        'shortName': 'J.Reed',
                        'teamId': '1800',
                        'maxSpeed': 19.513636407,
                        'headshot': 'https://static.www.nfl.com/image/upload/{formatInstructions}/league/blh2tfg9qjthqo2g6ot4'}
                },
                'timeToSackLeaders': {
                    'home': {
                        'gsisPlayId': 1136,
                        'esbId': 'BOO005373',
                        'jerseyNumber': 94,
                        'playerName': 'Austin Booker',
                        'position': 'DE',
                        'shortName': 'A.Booker',
                        'teamId': '0810',
                        'tackleInfo': {
                            'timeToTackle': 3.854
                        },
                        'headshot': 'https://static.www.nfl.com/image/upload/{formatInstructions}/league/gxs1vf40thpixmxwdvmc'
                    },
                    'visitor': {
                        'gsisPlayId': 3115,
                        'esbId': 'VAN639767',
                        'jerseyNumber': 90,
                        'playerName': 'Lukas Van Ness',
                        'position': 'DE',
                        'shortName': 'L.Van Ness',
                        'teamId': '1800',
                        'tackleInfo': {
                            'timeToTackle': 3.088
                        },
                        'headshot': 'https://static.www.nfl.com/image/upload/{formatInstructions}/league/qxrs2r7nvy9k6hlkqvyb'
                    }
                },
                'passDistanceLeaders': {
                    'home': {
                        'gsisPlayId': 2255,
                        'esbId': 'WIL176897',
                        'jerseyNumber': 18,
                        'playerName': 'Caleb Williams',
                        'position': 'QB',
                        'shortName': 'C.Williams',
                        'teamId': '0810',
                        'passInfo': {
                            'airDistance': 38.6932099986548
                        },
                        'headshot': 'https://static.www.nfl.com/image/upload/{formatInstructions}/league/h4qs11kutwiw7whekmyt'
                    },
                    'visitor': {
                        'gsisPlayId': 4628,
                        'esbId': 'LOV130776',
                        'jerseyNumber': 10,
                        'playerName': 'Jordan Love',
                        'position': 'QB',
                        'shortName': 'J.Love',
                        'teamId': '1800',
                        'passInfo': {
                            'airDistance': 35.5321291228094
                        },
                        'headshot': 'https://static.www.nfl.com/image/upload/{formatInstructions}/league/uneiwen9drvci9ahuebp'
                    }
                }
            }
        }
    }
}
]

class MyTestCase(unittest.TestCase):
    def test_get_games(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
