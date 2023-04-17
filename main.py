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


all_footballers = []


def parse_leauge():
    for league_url in list_of_league_urls:
        league_page = requests.get(league_url, headers=headers)
        leauge_soup = BeautifulSoup(league_page.content, 'html.parser')
        league_name = (leauge_soup.title.string)
        league_name = league_name[:-22]  # delete 'yy/yy TransferMarkt'
        parse_club(leauge_soup)
        
    return (all_footballers)



def parse_club(league):
    for link in league.find_all('td', class_="hauptlink no-border-links"):
        club_url = "https://www.transfermarkt.com" + (link.a.get("href"))
        club_page = requests.get(club_url, headers=headers)
        club_soup = BeautifulSoup(club_page.content, 'html.parser')
        club_name = (club_soup.title.string)
        club_name = club_name.replace(' - Club profile  | Transfermarkt', '')
        parse_footballer(club_soup)
        break

def parse_footballer(club):
        for footballer in (club.find_all('td', class_="hauptlink")):
            try:
                if "profil" in footballer.a.get("href"):
                    footballer_url = footballer.a.get("href")
                    footballer_url = "https://www.transfermarkt.com" + footballer_url
                    footballer_page = requests.get(footballer_url, headers=headers)
                    footballer_soup = BeautifulSoup(footballer_page.content, 'html.parser')
                    club_name = footballer_soup.find('span', class_="data-header__club").text
                    league_name = footballer_soup.find('a', class_="data-header__league-link").text
                    footballer_name = footballer_soup.find('h1', class_="data-header__headline-wrapper").text
                    footballer_name = re.sub(r'[^a-zA-Z ]+', '',footballer_name)
                    value = footballer_soup.find('div', class_="tm-player-market-value-development__current-value").text
                    footballer_details = [data.text for data in footballer_soup.find_all('li', class_="data-header__label")]
                    footballer_info_pack = clean.list_clearance(footballer_details)
                    
                    footballer_name = clean.clearance(footballer_name)
                    footballer_info_pack["Name"] = footballer_name

                    value = clean.value_count(value)
                    footballer_info_pack["Value in million"] = value

                    club_name = clean.clearance(club_name)
                    footballer_info_pack["Club"] = club_name

                    league_name = clean.clearance(league_name)
                    footballer_info_pack["Leauge"] = league_name

                    all_footballers.append(footballer_info_pack)
            except:
                pass
            break

def create_df_and_save_to_csv(data):
    df = pd.DataFrame(data)
    df.to_csv("Players.csv", index=False)


create_df_and_save_to_csv(parse_leauge())
