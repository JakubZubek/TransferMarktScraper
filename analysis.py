import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tick


def calulate_percentage(a, b):
    percentage = round(a / b*100, 2)
    return percentage


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i]//2, y[i], ha='center')


def bar(dict, league_name, league_average, title):
    x = dict.keys()
    y = list(dict.values())
    x = [name.replace(" ", "\n") for name in x]
    fig = plt.figure(figsize=(15, 10))

    plt.bar(x, y, label="Team average")

    plt.axhline(y=league_average, color='r',
                linestyle='-', label="League average")
    
    if title == "domestic players":
        addlabels(x, y)
        plt.gca().yaxis.set_major_formatter(tick.PercentFormatter())
        plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    elif title == "average height (m)":
        plt.yticks([1.76, 1.78, 1.8, 1.82, 1.84, 1.86, 1.88, 1.9])
        plt.ylim([1.76, 1.9])
    elif title == "average player value (millions €)":
        addlabels(x, y)
    plt.title(league_name + " " + title)
    plt.text(-1.2, league_average, league_average)
    plt.xticks(rotation=75)
    plt.legend(loc='best')
    plt.savefig(league_name + "_" + title.replace(" ", "_") + ".png", dpi=fig.dpi)


country_league_dict = {"Serie A": "Italy",
                       "Ligue 1": "France",
                       "Bundesliga": "Germany",
                       "LaLiga": "Spain",
                       "Premier League": "England",
                       }

df = pd.read_csv('Players.csv')
for league, country in country_league_dict.items():
    domestic_percent = {}
    club_average_height = {}
    club_average_value = {}
    one_league_df = (df[df["League"] == league])
    quantity_league_players = one_league_df.shape[0]
    quantity_domesitc_players = (df[(df["League"] == league) & (
        df["Citizenship"] == country)]).shape[0]
    league_domestic_procent = calulate_percentage(
        quantity_domesitc_players, quantity_league_players)
    
    league_average_height = round(one_league_df["Height"].mean(), 4)
    league_average_value = round(one_league_df["Value in million"].mean(), 2)
    clubs_in_league = one_league_df["Club"].unique()
    for club in clubs_in_league:
        one_club_df = one_league_df[one_league_df["Club"] == club]
        club_average_height[club] = round(one_club_df["Height"].mean(), 4)
        club_average_value[club] = round(one_club_df["Value in million"].mean(), 2)
        quantity_club_players = one_club_df.shape[0]
        club_domestic_players = (one_league_df[(one_league_df["Club"] == club) & (
            one_league_df["Citizenship"] == country)]).shape[0]
        club_percentage = calulate_percentage(
            club_domestic_players, quantity_club_players)
        domestic_percent[club] = club_percentage
        
    bar(domestic_percent, league, league_domestic_procent, "domestic players")
    bar(club_average_height, league, league_average_height, "average height (m)")
    bar(club_average_value, league, league_average_value, "average player value (millions €)")