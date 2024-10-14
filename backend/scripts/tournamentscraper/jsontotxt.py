import json

# with open(r'backend/scripts/tournamentscraper/output_file.json', 'rb') as file:
#     # Move the file pointer to the specific position
#     file.seek(40403)
    
#     # Read the byte at the position
#     byte_value = file.read(1)
    
#     # Print the byte in hexadecimal format
#     print(f'Byte at position 40403: {byte_value.hex()}')
# with open(r'backend\scripts\playernames.json', 'r') as file:
#     playernames = json.load(file)
# print(len(playernames))
# with open(r'backend/scripts/tournamentscraper/output.json', 'r', encoding='utf-8', errors='replace') as file:
#     data = json.load(file)
# with open(r'backend\API\vlr90.json', 'r') as file:
#     regionleague = json.load(file)
def calculate_placement(placement_str):
    try:
        if "–" in placement_str:
            parts = placement_str.split("–")
            return (int(parts[0][:-2]) + int(parts[1][:-2])) / 2  # Removing "st", "nd", etc.
        else:
            return int(placement_str[:-2])  # Removing suffix like 'st', 'nd', etc.
    except (ValueError, IndexError):
        return None

def classify_team(placement, total_teams):
    if placement is None:
        return "unknown"
    elif placement <= total_teams * 0.25:
        return "in the top 25%"
    elif placement <= total_teams * 0.75:
        return "in the middle 50%"
    else:
        return "in the bottom 25%"

def classify_player_performance(rating_per_round):
    if rating_per_round > 1.2:
        return "performing well"
    elif rating_per_round < 0.9:
        return "playing poorly"
    else:
        return "playing decently"

def describe_play_style(first_contact_per_round):
    if first_contact_per_round > 0.3:
        return "and aggressively"
    elif first_contact_per_round < 0.1:
        return "and defensively"
    else:
        return None

def summarize_agents_in_tournament(agent_dict):
    summary = []
    total_rating = 0
    total_first_contact = 0
    total_rounds = 0

    for agent_name, stats in agent_dict.items():
        rounds = stats.get('rounds', 1)  # Avoid division by zero
        rating_per_round = stats.get('rating', 0) / rounds
        first_contact_per_round = stats.get('first_contact', 0) / rounds

        total_rating += stats.get('rating', 0)
        total_first_contact += stats.get('first_contact', 0)
        total_rounds += rounds

        performance_desc = classify_player_performance(rating_per_round)
        play_style = describe_play_style(first_contact_per_round)

        description = f"played {rounds} rounds on {agent_name}, {performance_desc}"
        if play_style:
            description += f", {play_style}"

        description += f" with a rating of {round(rating_per_round, 2)} and first contact per round of {round(first_contact_per_round, 2)}"

        summary.append(description)

    # Calculate overall stats
    overall_rating = total_rating / total_rounds if total_rounds > 0 else 0
    overall_first_contact = total_first_contact / total_rounds if total_rounds > 0 else 0
    overall_performance_desc = classify_player_performance(overall_rating)
    overall_play_style = describe_play_style(overall_first_contact)

    overall_summary = f"{overall_performance_desc} with a rating of {round(overall_rating, 2)}"
    if overall_play_style:
        overall_summary += f" and {overall_play_style}"
    overall_summary += f", with a first contact per round of {round(overall_first_contact, 2)}"

    return summary, overall_summary
regionleaguekeys = {
    "ap": "Asia-Pacific",
    "amer": "Americas",
    "emea": "Europe, Middle East and Africa",
    "cn": "China",
    "gc": "Game Changers",
    "international": "VCT International",
    "challengers": "VCT Challengers",

}
def generate_player_based_narrative(data):
    player_dict = {}

    for tournament in data:
        for tournament_name, tournament_data in tournament.items():
            teams = tournament_data["teams"]
            total_teams = len(teams)

            for team_name, team_data in teams.items():
                place = team_data.get("place", "Unknown placement")
                placement_avg = calculate_placement(place)
                team_classification = classify_team(placement_avg, total_teams)

                team_performance = f"They played on team {team_name}, finished {place} and placing them {team_classification}."

                for player_name, agent_data in team_data.items():
                    if player_name != "place":
                        agent_summary, overall_summary = summarize_agents_in_tournament(agent_data)

                        if player_name not in player_dict:
                            player_dict[player_name] = {}

                        if tournament_name not in player_dict[player_name]:
                            player_dict[player_name][tournament_name] = {
                                "team_performance": team_performance,
                                "overall_summary": overall_summary,
                                "agents": agent_summary
                            }
    count = 0
    playercount = []
    for player_name, tournaments in list(player_dict.items()):
        
        if player_name not in playernames:
            continue
        playercount.append(player_name)
        player_obj = next((obj for obj in regionleague if obj["player"] == player_name), None)
        region = regionleaguekeys[player_obj["region"]]
        league = regionleaguekeys[player_obj["league"]]
        narrative = f"{player_name} plays in the {region} region and {league} league. {player_name} from participated in the following tournaments:\n"
        for tournament_name, details in tournaments.items():
            narrative += (f"- In {tournament_name}, {details['team_performance']} "
                          f"{player_name} was {details['overall_summary']}.\n"
                          f"{player_name} played the following agents in {tournament_name}:\n")

            agents_played = ". ".join(details['agents'])
            narrative += f"  - {agents_played}.\n"

        # Write narrative to a file named after the player
        filename = 'backend/scripts/tournamentscraper/playerdata/' + f"{player_name}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(narrative)
            count+=1
    difference = list(set(playercount) - set(playernames))
    print(difference)
    print(count)
    return "Player narratives have been written to separate files."




def convert_json_to_text(tournaments):
    result = ""

    for tournament in tournaments:
        for tournament_name, tournament_data in tournament.items():
            result += f"Tournament: {tournament_name}\n\n"

            result += "Teams:\n"
            for team_name, team_data in tournament_data['teams'].items():
                result += f"  - Team: {team_name}\n"

                # Only add the placement if 'place' exists in the team data
                if 'place' in team_data:
                    result += f"    Placement: {team_data['place']}\n"

                result += "    Players:\n"
                for player_name, player_data in team_data.items():
                    if player_name != 'place':  # Ignore the 'place' key
                        result += f"      * {player_name}: Rating: {round(player_data['rating'], 2)}\n"
                result += "\n"

    return result

def unicode_convert():
    with open(r'backend/scripts/tournamentscraper/output_file.json', 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()

# Write the decoded content back to a new file
    with open('backend/scripts/tournamentscraper/output_file.json', 'w', encoding='utf-8') as output_file:
        output_file.write(content)

# Convert JSON to text

import os

def remove_last_two_lines(file_path):
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Write back all but the last two lines
    with open(file_path, 'w') as file:
        file.writelines(lines[:-1])

def process_folder(folder_path):
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the current item is a file
        if os.path.isfile(file_path):
            remove_last_two_lines(file_path)
            print(f"Processed file: {filename}")

# Example usage
folder_path = r'C:\Users\alex2\OneDrive\Desktop\valorant\VCTHack\backend\scripts\tournamentscraper\playerdata'
process_folder(folder_path)


# generate_player_based_narrative(data)


# # Write to a text file
# with open(r'backend/scripts/tournamentscraper/knowledge_base.txt', 'w', encoding='utf-8') as file:
#     file.write(generate_player_based_narrative(data))

print("Knowledge base has been written to 'knowledge_base.txt'")        