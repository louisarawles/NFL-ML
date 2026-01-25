from NFLScrapers.GameCenter.game_center_scraper import get_url_games, get_data, get_games, get_url_gameStats, \
    get_gameStats
from NFLLoaders import NFLLoader as nl

if __name__ == '__main__':
    games_url = get_url_games()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://nextgenstats.nfl.com/stats/game-center-index",
    }
    # params = get_params(20,2,1)
    # idk how to use params yet so this just loads er up
    # tbh would only need params if i wanted previous seasons

    data_games = get_data(games_url, headers)
    games, unfinished_games = get_games(data_games)

    for g in games:
        g_id = g.gameId
        gs_url = get_url_gameStats(g_id)
        gs_data = get_data(gs_url, headers)

        h_gameStats = get_gameStats(gs_data, g, homeVisitor='home')
        v_gameStats = get_gameStats(gs_data, g, homeVisitor='visitor')

        nl.load_gameStats(h_gameStats)
        nl.load_gameStats(v_gameStats)