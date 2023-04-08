import requests
from bs4 import BeautifulSoup

list_of_league_urls = [
    'https://www.transfermarkt.pl/serie-a/startseite/wettbewerb/IT1',
    'https://www.transfermarkt.pl/ligue-1/startseite/wettbewerb/FR1',
    'https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1',
    'https://www.transfermarkt.pl/bundesliga/startseite/wettbewerb/L1',
    'https://www.transfermarkt.pl/laliga/startseite/wettbewerb/ES1']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

league_url = "https://www.transfermarkt.pl/premier-league/startseite/wettbewerb/GB1"

league_page = requests.get(league_url, headers=headers)

leauge_soup = BeautifulSoup(league_page.content, 'html.parser')
league_name = (leauge_soup.title.string)
league_name = league_name[:-22]  # delete 'yy/yy TransferMarkt'

for link in leauge_soup.find_all('td', class_="hauptlink no-border-links"):
    club_url = "https://www.transfermarkt.com" + (link.a.get("href"))
    club_page = requests.get(club_url, headers=headers)
    club_soup = BeautifulSoup(club_page.content, 'html.parser')
    club_name = (club_soup.title.string)
    club_name = club_name.replace(' - Club profile  | Transfermarkt', '')
    for footballer in (club_soup.find_all('span', class_="hide-for-small")):
        footballer_name = footballer.a.get("title")
        footballer_url = "https://www.transfermarkt.com" + \
            footballer.a.get("href")
        footballer_page = requests.get(footballer_url, headers=headers)
        footballer_soup = BeautifulSoup(footballer_page.content, 'html.parser')
        #print (footballer_name, club_name, league_name)
        #print (footballer_url)
        # for data in footballer_soup.find_all('dd', class_="detail-position__position"):
        #print (data, footballer_name)
        # for data in footballer_soup.find_all('div', class_="tm-player-market-value-development__current-value"):
        #print (data, footballer_name)

        # for data in footballer_soup.find_all('span', class_="info-table__content info-table__content--bold"):
        #print (data, footballer_name)
