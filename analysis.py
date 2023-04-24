import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tick


def calulate_percentage(a, b):
    percentage = round(a / b*100, 2)
    return percentage


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i]//2, y[i], ha='center')


def bar(dict, league_name, league_average, scale):
    x = dict.keys()
    y = list(dict.values())
    x = [name.replace(" ", "\n") for name in x]
    fig = plt.figure(figsize=(15, 10))

    plt.bar(x, y, label="Team average")

    plt.axhline(y=league_average, color='r',
                linestyle='-', label="League average")

    if scale == "a":
        addlabels(x, y)
        plt.text(-1.2, league_average+0.4, league_average)
        plt.gca().yaxis.set_major_formatter(tick.PercentFormatter())
        plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        plt.title(league_name + " percentage of domestic players")
    elif scale == "b":
        plt.text(0, league_average, league_average)
        plt.yticks([1.76, 1.78, 1.8, 1.82, 1.84, 1.86, 1.88, 1.9])
        plt.ylim([1.76, 1.9])
        plt.title(league_name + " average height")
    elif scale == "c":
        plt.text(-1.2, league_average+0.4, league_average)
    plt.xticks(rotation=75)
    plt.legend(loc='best')
    plt.show()
    #plt.savefig(league_name + ".png", dpi=fig.dpi)


country_league_dict = {"Serie A": "Italy",
                       "Ligue 1": "France",
                       "Bundesliga": "Germany",
                       "LaLiga": "Spain",
                       "Premier League": "England",
                       }

df = pd.read_csv('Players.csv')
for league, country in country_league_dict.items():
    domestic_percent = {}
    height = {}
    value = {}
    one_league_df = (df[df["League"] == league])
    all_players = one_league_df.shape[0]
    domesitc_players = (df[(df["League"] == league) & (
        df["Citizenship"] == country)]).shape[0]
    league_domestic_procent = calulate_percentage(
        domesitc_players, all_players)
    clubs_in_league = one_league_df["Club"].unique()
    league_height = one_league_df["Height"].mean()
    league_value = one_league_df["Value in million"].mean()
    for club in clubs_in_league:
        one_club_df = one_league_df[one_league_df["Club"] == club]

        height[club] = one_club_df["Height"].mean()
        value[club] = one_club_df["Value in million"].mean()
        club_players = one_club_df.shape[0]
        club_domestic_players = (one_league_df[(one_league_df["Club"] == club) & (
            one_league_df["Citizenship"] == country)]).shape[0]
        club_percentage = calulate_percentage(
            club_domestic_players, club_players)
        domestic_percent[club] = club_percentage
    bar(domestic_percent, league, league_domestic_procent, "a")
    bar(height, league, league_height, "b")
    bar(value, league, league_value, "c")
    break
