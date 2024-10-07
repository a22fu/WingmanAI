import requests
import json
from bs4 import BeautifulSoup

def scrape_player_image(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to retrieve data for URL {url}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    player_name = ""
    h1_tag = soup.find('h1', class_='wf-title')
    
    if h1_tag:
        player_name = h1_tag.get_text(strip=True)

    player_div = soup.find('div', class_='player-header')
    
    if player_div:
        # Find the image inside that div
        player_image = player_div.find('img')
        
        if player_image and player_image['src']:
            image_url = player_image['src']
            return [image_url, player_name]
        else:
            print(f"No image found for player in URL {url}")
            return None
    else:
        print(f"No player div found for URL {url}")
        return None


def scrape_players_from_table(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error: Unable to retrieve data from {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows = soup.find_all('tr')
    player_urls = []
    
    for row in table_rows:
        # Find <td> with class "mod-player mod-a"
        player_td = row.find('td', class_='mod-player mod-a')
        if player_td:
            player_link = player_td.find('a', href=True)
            if player_link:
                player_url = player_link['href']
                player_urls.append(player_url)
    
    return player_urls


def scrape_all_player_images(main_url):
    player_urls = scrape_players_from_table(main_url)
    
    all_player_images = {}
    for player_url in player_urls:
        full_url = f"https://vlr.gg{player_url}" # Construct the full URL
        player_data = scrape_player_image(full_url)
        
        if player_data:
            print(player_data[1] + " found")
            all_player_images[player_data[1]] = player_data[0]
    
    return all_player_images


# Example usage:
main_url = "https://www.vlr.gg/stats/?event_group_id=all&event_id=all&region=all&min_rounds=200&min_rating=1550&agent=all&map_id=all&timespan=90d"
player_images = scrape_all_player_images(main_url)

# This will print the list of [image_url, player_name] for all scraped players
print(player_images)
with open('player_images.json', 'w') as f:
    json.dump(player_images, f, separators=None)