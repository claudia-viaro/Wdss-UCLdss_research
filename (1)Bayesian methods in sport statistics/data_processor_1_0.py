from data_tools import load_games

## ---------------------------- Info about load_games ----------------------------
##
## The function outputs a list of "game_match" objects, which represents
## a single match. It has the following attributes:
##  league    -> just a remainder that its the correct league
##
##  season    -> the starting year for that season (2012-2013 would be 2012)
##
##  date      -> the date when that match took place (DD/MM/YY)
##
##  home_team -> name of the home team (!! Important to note that most names
##  away_team -> name of the away team     are slightly changed, because the 
##                                         author of those csv files decided
##                                         to do that. For example, 
##                                         Manchester United is Man United
##                                         Tottenham Hotspur F.C. is Tottenham !!)
##
##  features  -> A dictioary with data from the csv files, where each key is
##               an entry from the ENTRIES list (except Date, HomeTeam, AwayTeam)
##               (!! it doesnt happen often but there might be about 10-20 games
##                   out of 26k that dont have some of those entries, meaning 
##                   HTAG might have a value of ""                             !!)
##
## ------------ misc stuff ------------
##
## It also stores the games the home team had played against the away team and any
## team this season, the previous season and the season before that. Note that
## a lot of teams might have been demoted from the top leagues so its probable that
## they dont have past info.
## In addition, it also stores the previous season standings


## Defines the data entires that will loaded from the csv files
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

## Properly functioning csv files given these entries
## England --> 2000-2021
## Germany --> 2006-2021
## Italy   --> 2005-2021
## Spain   --> 2005-2021
LOWER_BOUND = {'England': 2000,
               'Germany': 2006,
               'Italy'  : 2005,
               'Spain'  : 2005}



def main():
    ## Sample usage
    # loads all available premier league games
    GAMES = load_games("England", (2000, 2021))
    
    game = GAMES[123]
    # match identifiers
    print(f"\nSeason {game.season}/{int(game.season) + 1} | {game.date}")
    print(f"{game.home_team} vs {game.away_team}\n")
    
    # one match features
    print("### Features ###")
    features = game.features
    for feat in features:
        print(f"{feat} -> {features[feat]}")

    ## If you want to load only one season then
    # 1. if only features are needed
    GAMES = load_games("England", (2012, 2012))
    
    # 2. if also the past games are needed then load two year before that
    # and ignore the first two seasons from the output list.
    # for germany [306*2:] since they have 306 games instead of 380 in one season
    GAMES = load_games("England", (2012 - 2, 2012))[380*2:]
    print(len(GAMES))
                       
if __name__ == "__main__":
    main()