import csv
import datetime
import copy

## Properly functioning csv files given these entries
## England --> 2000-2021
## Germany --> 2006-2021
## Italy   --> 2005-2021
## Spain   --> 2005-2021
LOWER_BOUND = {'England': 2000,
               'Germany': 2006,
               'Italy'  : 2005,
               'Spain'  : 2005}

## Defines the data entires that will be used to train the machine
##                     # 0)  season (starting year) or div if from a csv reader
ENTRIES = ["Date",     # 1)  date at which it was played
           "HomeTeam", # 2)  home team
           "AwayTeam", # 3)  away team
           "FTHG",     # 4)  full time home goals
           "FTAG",     # 5)  full time away goals
           "FTR",      # 6)  full time result (H, D, A)
           "HTHG",     # 7)  half time home goals
           "HTAG",     # 8)  half time away goals
           "HTR",      # 9)  half time result (H, D, A)
           "HS",       # 10) home shots
           "AS",       # 11) away shots
           "HST",      # 12) home team shots on target
           "AST",      # 13) away team shots on target
           "HF",       # 14) home team fouls
           "AF",       # 15) away team fouls
           "HC",       # 16) home team corners
           "AC",       # 17) away team corners
           "HY",       # 18) home yellow cards
           "AY",       # 19) away yellow cards
           "HR",       # 20) home red cards
           "AR"        # 21) away red cards
        ]


class game_match:
    def __init__(self, league, season, date, home_team, away_team):
        # Match identifiers
        self.league    = league
        self.season    = season
        self.date      = date
        self.home_team = home_team
        self.away_team = away_team
        
        # Data from the match
        self.features      = {}
        self.gathered_feat = {"same_opponent" :{"this_season" : [],
                                                "past1_season": [],
                                                "past2_season": []},
                              
                              "any_opponent"   :{"this_season" : [],
                                                 "past1_season": [],
                                                 "past2_season": []},
                              
                              "home_standings" :{"this_season" : [],
                                                 "past1_season": [],
                                                 "past2_season": []},
                              
                              "away_standings" :{"this_season" : [],
                                                 "past1_season": [],
                                                 "past2_season": []}}




##########################################################################
##########################################################################
##########################################################################


def load_games(country, BOUNDRIES):
    """
    Loads the data from csv files into a list.\n
    Choose one of the following:\n
    England\n
    Germany\n
    Italy\n
    Spain\n...\n
    Boundry sets the first and the last season:\n
    BOUNDRIES = [_FirstYear_, _LastYear_]
    """
    csv_games     = []
    csv_standings = []
    FEATURES      = ENTRIES[3:]
    
    if country == "England":
        PATH = "soccer_stats_data/england/england-premier-league-"
        file_path_standings = "soccer_stats_data/england/EPL_Standings_2000-2022.csv"
    elif country == "Germany":
        PATH = "soccer_stats_data/germany/germany-bundesliga-1-"
        file_path_standings = "soccer_stats_data/germany/Bundesliga_Standings_2001-2021.csv"
    elif country == "Italy":
        PATH = "soccer_stats_data/italy/italy-serie-a-"
        file_path_standings = "soccer_stats_data/italy/Italy_Standings_2003-2021.csv"
    elif country == "Spain":
        PATH = "soccer_stats_data/spain/spain-la-liga-primera-division-"
        file_path_standings = "soccer_stats_data/spain/Spanish_Standings_2003-2021.csv"
        
    for year in range(BOUNDRIES[0], BOUNDRIES[1] + 1):
        file_path_games = PATH+str(year)+"-to-"+str(year+1)+".csv"
        with open(file_path_games) as f:
            dict_reader = csv.DictReader(f)
            for row in dict_reader:
                temp_match = game_match(row["Div"], year, row["Date"], row["HomeTeam"], row["AwayTeam"])
                for entry in FEATURES:
                    temp_match.features[entry] = row[entry]
                csv_games.append(temp_match)
    
    with open(file_path_standings) as f:
        dict_reader = csv.DictReader(f)
        for row in dict_reader:
            temp_rank = {"Season": row["Season"], "Team": row["Team"], "Pos": row["Pos"], "Pts": row["Pts"]}
            csv_standings.append(temp_rank)
            
    ## ------------------------------------------------------------------------------------------------------
    ## Records the season of the first game
    this_season   = BOUNDRIES[0]
    list_of_games = get_game_list(csv_games, this_season)
    list_of_past1 = []
    list_of_past2 = []
    game_index    = 0
    loading_count = 0
    
    for game in csv_games:
        if this_season != game.season:
            game_index    = 0
            this_season   = game.season
            list_of_games = get_game_list(csv_games, this_season)
            if this_season == BOUNDRIES[0] + 1:
                list_of_past1 = get_game_list(csv_games, this_season -1)
            else:
                list_of_past1 = get_game_list(csv_games, this_season -1)
                list_of_past2 = get_game_list(csv_games, this_season -2)
        
        if this_season <= BOUNDRIES[0]:
            ## There is no info about prior seasons
            gather_data(game, list_of_games, game_index, 0)
            game.gathered_feat["home_standings"]["past1_season"] = find_standings(csv_standings, game.home_team, this_season - 1)
            game.gathered_feat["home_standings"]["past2_season"] = find_standings(csv_standings, game.home_team, this_season - 2)
            game.gathered_feat["away_standings"]["past1_season"] = find_standings(csv_standings, game.away_team, this_season - 1)
            game.gathered_feat["away_standings"]["past2_season"] = find_standings(csv_standings, game.away_team, this_season - 2)
            
        elif this_season == BOUNDRIES[0] + 1:
            ## Data about the current season
            gather_data(game, list_of_games, game_index, 0)
            
            ## Data about the previous season
            gather_data(game, list_of_past1, 0, 1)
            game.gathered_feat["home_standings"]["past1_season"] = find_standings(csv_standings, game.home_team, this_season - 1)
            game.gathered_feat["home_standings"]["past2_season"] = find_standings(csv_standings, game.home_team, this_season - 2)
            game.gathered_feat["away_standings"]["past1_season"] = find_standings(csv_standings, game.away_team, this_season - 1)
            game.gathered_feat["away_standings"]["past2_season"] = find_standings(csv_standings, game.away_team, this_season - 2)
        
        else:
            ## Data about the current season
            gather_data(game, list_of_games, game_index, 0)
            
            ## Data about the previous season
            gather_data(game, list_of_past1, 0, 1)
            game.gathered_feat["home_standings"]["past1_season"] = find_standings(csv_standings, game.home_team, this_season - 1)
            game.gathered_feat["away_standings"]["past1_season"] = find_standings(csv_standings, game.away_team, this_season - 1)
            
            ## Data about the season before the previous season
            gather_data(game, list_of_past2, 0, 2)
            game.gathered_feat["home_standings"]["past2_season"] = find_standings(csv_standings, game.home_team, this_season - 2)
            game.gathered_feat["away_standings"]["past2_season"] = find_standings(csv_standings, game.away_team, this_season - 2)
        game_index += 1
    return csv_games


def gather_data(this_game, list_of_games, game_index, season):
    """
    Gathers data about each match.\n
    season must be 0, 1 or 2\n
    0 - this_season\n
    ...\n
    2 - past2_season
    """
    if season == 0:
        for i in range(game_index - 1, -1, -1):
            prev_game = list_of_games[i]
            ## The index represent which game it is counting from the current game
            if prev_game.home_team == this_game.home_team or prev_game.away_team == this_game.home_team:
                ## This game has the home team in it
                update_game(this_game, prev_game, 0)
    elif season == 1:
        for i in range(len(list_of_games) -1, -1, -1):
            prev_game = list_of_games[i]
            if prev_game.home_team == this_game.home_team or prev_game.away_team == this_game.home_team:
                update_game(this_game, prev_game, 1)
    elif season == 2:
        for i in range(len(list_of_games) -1, -1, -1):
            prev_game = list_of_games[i]
            if prev_game.home_team == this_game.home_team or prev_game.away_team == this_game.home_team:
                update_game(this_game, prev_game, 2)

    
def update_game(this_game, previous_game, season):
    """
    Updates the gathered info about this game\n
    season should be a number:\n
    0 - this_season\n
    1 - past1_season\n
    2 - past2_season
    """
    season_indicator = ["this_season",
                        "past1_season",
                        "past2_season"]
    current_season   = season_indicator[season]
    
    if previous_game.home_team == this_game.home_team:
        ## This game home was the current home
        if previous_game.away_team == this_game.away_team:
            ## This game was played against the same team
            this_game.gathered_feat["same_opponent"][current_season].append(previous_game)
            this_game.gathered_feat["any_opponent"][current_season].append(previous_game)
        else:
            this_game.gathered_feat["any_opponent"][current_season].append(previous_game)
    elif previous_game.away_team == this_game.home_team:
        ## This game home was the current away
        if previous_game.home_team == this_game.away_team:
            ## This game was played against the same team
            this_game.gathered_feat["same_opponent"][current_season].append(previous_game)
            this_game.gathered_feat["any_opponent"][current_season].append(previous_game)
        else:
            this_game.gathered_feat["any_opponent"][current_season].append(previous_game)
    
               
def get_date(date_string):
    """
    Returns the date specified in the string\n
    'dd/mm/yyyy', where year is >= 2000
    """
    date_temp = date_string.split("/")
    if len(date_temp[2]) == 4:
        date_temp[2] = date_temp[2][2:]
    this_date = datetime.date(int("20"+date_temp[2]), 
                              int(date_temp[1]), int(date_temp[0]))
    return this_date


def get_game_list(csv_games, season):
    """
    Outputs a list of games in this season
    """
    output     = []
    game_count = 0
    for game in csv_games:
        if game_count >= 380:
            break
        if game.season == season:
            output.append(copy.copy(game))
            game_count += 1
    return output


def find_standings(standings, team_name, season):
    """
    Finds and returns standings. \n
    season in this case is the staring year
    """
    for result in standings:
        if result["Season"] == str(season):
            if result["Team"] == team_name:
                return result
    return None