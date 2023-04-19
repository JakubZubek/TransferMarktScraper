import pandas as pd

df = pd.read_csv('Players.csv')
country_league_dict = {"Serie A": "Italy",
                       "Ligue 1": "France",
                       "Bundesliga": "Germany",
                       "LaLiga": "Spain",
                       "Premier League": "England"
                       }


for league, country in country_league_dict.items():
    all_players = (df.loc[df["League"] == league]).shape[0]
    homegrown_players = (df[(df["League"] == league) & (
        df["Citizenship"] == country)]).shape[0]
    percentage = str(round(homegrown_players / all_players*100, 4))
    print (league + " has " + percentage + "% homegrown players")
