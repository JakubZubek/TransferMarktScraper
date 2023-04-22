import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from matplotlib.axis import Axis


def calulate_percentage(a, b):
    percentage = round(a / b*100, 2)
    return percentage


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i]//2, y[i], ha='center')


def bar(x, y, league_name, league_percentage):
    x = [name.replace(" ", "\n") for name in x]
    fig = plt.figure(figsize=(15, 10))
    plt.gca().yaxis.set_major_formatter(tick.PercentFormatter())
    plt.bar(x, y, label="Team average")
    addlabels(x, y)
    plt.axhline(y=league_percentage, color='r',
                linestyle='-', label="League average")
    plt.text(-1.2, league_percentage+0.4, league_percentage)
    plt.title(league_name + " percentage of domestic players")
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.xticks(rotation=75)
    plt.legend(loc='best')
    plt.savefig(league_name + ".png", dpi=fig.dpi)


country_league_dict = {"Serie A": "Italy",
                       "Ligue 1": "France",
                       "Bundesliga": "Germany",
                       "LaLiga": "Spain",
                       "Premier League": "England",
                       }

df = pd.read_csv('Players.csv')
for league, country in country_league_dict.items():
    percentages = []
    names = []
    one_league_df = (df[df["League"] == league])
    all_players = one_league_df.shape[0]
    homegrown_players = (df[(df["League"] == league) & (
        df["Citizenship"] == country)]).shape[0]
    league_percentage = calulate_percentage(homegrown_players, all_players)
    clubs_in_league = one_league_df["Club"].unique()

    for club in clubs_in_league:
        one_club_df = one_league_df[one_league_df["Club"] == club]
        club_players = one_club_df.shape[0]
        club_homegrown_players = (one_league_df[(one_league_df["Club"] == club) & (
            one_league_df["Citizenship"] == country)]).shape[0]
        club_percentage = calulate_percentage(
            club_homegrown_players, club_players)
        percentages.append(club_percentage)
        names.append(club)
    league_percentage = (league_percentage)
    bar(names, percentages, league, league_percentage)
