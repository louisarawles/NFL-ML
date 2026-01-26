from NFLScrapers.GameCenter import game_finder as gf

from NFLScrapers.GameCenter.game_center_scraper import get_url_games, get_data, get_games, get_url_gameStats, get_gameStats
from NFLDataVis.zone_plots import show_zone_performance
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

    # im just using this specific game for testing purposes
    # and because go Bears and go comeback season baby

    bears_packers = gf.findGames(games, 'CHI', 'GB')

    for game in bears_packers:
        print(game)
        g_id = game.gameId
        gs_url = get_url_gameStats(g_id)
        gs_data = get_data(gs_url, headers)

        print(gs_data)

        print("Home Team: ", game.homeTeamAbbr)
        print("Visitor Team: ", game.visitorTeamAbbr)
        print(f"Score: {game.homeTeamAbbr}: {game.homeScore} - {game.visitorTeamAbbr}: {game.visitorScore}")

        gameStats = get_gameStats(gs_data, game)

        passers = gs_data.get('passers')
        h_passer = passers.get('home')
        v_passer = passers.get('visitor')
        show_zone_performance(game,h_passer)
        show_zone_performance(game,v_passer)