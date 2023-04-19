import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import clean
list_of_league_urls = [
    'https://www.transfermarkt.pl/serie-a/startseite/wettbewerb/IT1',
    'https://www.transfermarkt.pl/ligue-1/startseite/wettbewerb/FR1',
    'https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1',
    'https://www.transfermarkt.pl/bundesliga/startseite/wettbewerb/L1',
    'https://www.transfermarkt.pl/laliga/startseite/wettbewerb/ES1']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}


players = []

def parse_leauge():
    for league_url in list_of_league_urls:
        league_page = requests.get(league_url, headers=headers)
        leauge_soup = BeautifulSoup(league_page.content, 'html.parser')
        parse_club(leauge_soup)
    return (players)

def parse_club(league):
    for link in league.find_all('td', class_="hauptlink no-border-links"):
        club_url = "https://www.transfermarkt.com" + (link.a.get("href"))
        club_page = requests.get(club_url, headers=headers)
        club_soup = BeautifulSoup(club_page.content, 'html.parser')
        parse_player(club_soup)
        break

def parse_player(club):
        for player in (club.find_all('td', class_="hauptlink")):
            try:
                if "profil" in player.a.get("href"):
                    player_url = player.a.get("href")
                    player_url = "https://www.transfermarkt.com" + player_url 
                    player_page = requests.get(player_url, headers=headers)
                    player_soup = BeautifulSoup(player_page.content, 'html.parser')
                  
                    league_name = player_soup.find('a', class_="data-header__league-link").text
                    league_name = clean.clearance(league_name)
                  
                    club_name = player_soup.find('span', class_="data-header__club").text
                    club_name = clean.clearance(club_name)
                  
                    player_name = player_soup.find('h1', class_="data-header__headline-wrapper").text
                    player_name = re.sub(r'[^a-zA-Z ]+', '',player_name)
                    player_name = clean.clearance(player_name)
                  
                    player_value = player_soup.find('div', class_="tm-player-market-value-development__current-value").text
                    player_value = clean.value_count(player_value)
                  
                    player_details = [data.text for data in player_soup.find_all('li', class_="data-header__label")]
                    player_info_dict = clean.list_clearance(player_details)
                    
                    player_info_dict["Name"] = player_name
                    player_info_dict["Value in millions"] = player_value
                    player_info_dict["Club"] = club_name
                    player_info_dict["League"] = league_name
                    players.append(player_info_dict)
            except:
                pass
            break

def create_df_and_save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("Players.csv", index=False)


create_df_and_save_to_csv(parse_leauge())