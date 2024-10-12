import requests
import json
import re
from bs4 import BeautifulSoup
def clean(str):
    return str.replace('\n', '').replace('\t', '').strip()


def scrape_all_tourneys(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to retrieve data for URL {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    cols = soup.find_all('div', class_ = 'events-container-col')
    rows = cols[1].find_all('a', class_='wf-card mod-flex event-item')
    arr = []
    tourney = {}
    for row in rows:
        tourney = {}
        scrape_tourney_results("https://www.vlr.gg" + row['href'], tourney)
        arr.append(tourney)
    with open(r'backend/scripts/tournamentscraper/output.json', 'w') as file:
        json.dump(arr, file, indent=4)
    
def scrape_tourney_results(url, tourney_data):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to retrieve data for URL {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tournament = clean(soup.find('h1', class_='wf-title').get_text())
    print(tournament + " processsed")
    tourney_data[tournament] = {
        "teams":{},
        }
    tablecheck = soup.find('table', class_ = 'wf-table mod-simple')
    if tablecheck is None:
        return
    teamtable = tablecheck.find('tbody')
    rows = teamtable.find_all('tr')
    filtered_rows = [row for row in rows if 'standing-toggle' not in row.get('class', [])]
    for row in filtered_rows:
        cells = row.find_all('td')
        team = clean(cells[2].find('div', class_ = 'text-of standing-item-team-name').find_all(string=True, recursive=False)[0])
        place = clean(cells[0].find('div').find('div').get_text())
        tourney_data[tournament]["teams"][team] = {"place": place}
    matches_href = soup.find('div',class_ = 'wf-nav').find_all('a')[1]['href']
    allurl = re.sub(r'(?<=series_id=)\d+', 'all', matches_href)

    scrape_tourney_matches("https://www.vlr.gg" + allurl, tourney_data[tournament]["teams"])
    
    

    


def scrape_tourney_matches(url, teams_data):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to retrieve data for URL {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find('div', class_ = 'col mod-1').find_all('div', class_ = 'wf-card')
    filtered_cards = [card for card in cards if card.get('class') == ['wf-card']]

    for card in filtered_cards:
        links = card.find_all('a')
        for link in links:
            href = link['href']
            scrape_player_tourney_stats("https://www.vlr.gg" + href, teams_data)

def scrape_player_tourney_stats(url, teams_data):
    print(url)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to retrieve data for URL {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    teams = soup.find_all('div', class_ = "wf-title-med")
    team_names = [clean(teams[0].get_text()), clean(teams[1].get_text())]
    unfiltered_matches = soup.find_all('div', {'class': 'vm-stats-game'}, 
                      lambda tag: tag.get('data-game-id') != 'all')
    matches = [game for game in unfiltered_matches if game.get('data-game-id') != 'all']
    if matches is None:
        matches =  soup.find('div',{'class':'vm-stats-game'})
    if matches is None:
        return
    for match in matches:
        player_tables = match.find_all('table', class_='wf-table-inset mod-overview')
        for x in range(2):
            table = player_tables[x]
            scores = match.find_all('div', class_ = 'score')
            rounds = int(scores[0].get_text()) + int(scores[1].get_text())
            body = table.find('tbody')
            rows = body.find_all('tr')
            team = team_names[x]
            for row in rows:
                cells = row.find_all('td')
                player_name = clean(cells[0].find('div', class_='text-of').get_text())
                agent_name = cells[1].find('img')
                if agent_name is None:
                    return
                agent = clean(agent_name["alt"])
                rating = 0
                if clean(cells[2].find('span', class_='side mod-side mod-both').get_text())== '':
                    rating = 0
                else:
                    rating = float(clean(cells[2].find('span', class_='side mod-side mod-both').get_text()))
                cumrating = rating * rounds
                
                # acs = float(clean(cells[3].find('span', class_='side mod-side mod-both').get_text()))
                # kills = float(clean(cells[4].find('span', class_='side mod-side mod-both').get_text()))
                # deaths = float(clean(cells[5].find('span', class_='side mod-both').get_text()))
                # assists = float(clean(cells[6].find('span', class_='side mod-both').get_text()))
                # adr = float(clean(cells[9].find('span', class_='side mod-both').get_text()))
                fk = clean(cells[11].find('span', class_='side mod-both').get_text())
                fd = clean(cells[12].find('span', class_='side mod-both').get_text())
                if fk == '' or fd == '':
                    return
                first_contact = int(fk) + int(fd)
                if team not in teams_data:
                    teams_data[team] = {}
                if player_name not in teams_data[team]:
                    teams_data[team][player_name] = {}
                if agent not in teams_data[team][player_name]:
                    teams_data[team][player_name][agent] = {
                        "rating": cumrating,
                        "rounds": rounds,
                        "first_contact": first_contact
                    }
                else:
                    teams_data[team][player_name][agent]["rating"] += cumrating
                    teams_data[team][player_name][agent]["rounds"] += rounds
                    teams_data[team][player_name][agent]["first_contact"] += first_contact
                    # player_data[player_name]["deaths"] +=deaths
                    # player_data[player_name]["assists"] +=assists
                    # player_data[player_name]["adr"] +=adr
tiktok = {}
scrape_all_tourneys("https://www.vlr.gg/events")
