import random
import math
import json

# def filter_dataset(player_data, constraints):
#     # Extract region and league constraints from the JSON
#     region_constraints = {k: v for k, v in constraints.items() if k in ["amer", "emea", "cn", "ap"] and v != 0}
#     league_constraints = {k: v for k, v in constraints.items() if k in ["gc", "international", "challengers"] and v != 0}
#     filtered_data = player_data
#     # Check if either regions or leagues add up to 5
#     if sum(region_constraints.values()) == 5:
#         # Filter players based on regions and leagues
#         filtered_data = [player for player in filtered_data if player["region"] in region_constraints ]
#     if  sum(league_constraints.values()) == 5:
#         filtered_data = [player for player in filtered_data if player["league"] in league_constraints ]
#     return filtered_data


# Scoring function based on individual player stats
def calculate_team_score(team):
    # Example: sum of individual scores + bonus for synergy
    valorant_roles = {
    "smokes": ["omen", "brimstone", "viper", "astra", "harbor", "clove"],
    "entry": ["reyna", "phoenix", "yoru", "iso"],
    "intel_gatherer": ["sova", "fade", "cypher","gekko","skye"],
    "lurker": ["cypher", "omen", "chamber", "yoru", "viper", "killjoy"],
    "flank_watch": ["killjoy", "cypher", "chamber","vyse"],
    "flash_initiator": ["skye", "kayo", "breach", "phoenix","reyna","gekko"],
    "movement_duelist": ["reyna", "raze", "neon", "jett", "yoru"]
    }
    team_roles = {
        "smokes": False,
        "entry": False,
        "intel_gatherer": False,
        "lurker": False,
        "flank_watch": False,
        "flash_initiator": False,
        "movement_duelist": False
    }

    for player in team:
        for agent in player["agents"]:
            for role in valorant_roles:
                if agent in valorant_roles[role]:
                    team_roles[role] = True
    return sum(player["zscore"] for player in team) + sum(1 for value in team_roles.values() if value is True) * 5

# def satisfies_constraints(team):
#     # Count number of female players
#     gc_count = sum(1 for player in team if player["league"] == "gc")
#     amer_count = sum(1 for player in team if player["region"] == "amer")
#     cn_count = sum(1 for player in team if player["region"] == "cn")

    
#     # Check for required roles


#     return (
#         amer_count >= 1 and 
#         cn_count >= 3 and 
#         gc_count >= 5
#     )

# Generate a random team of 5 players
def generate_random_team(player_pool):
    return random.sample(player_pool, 5)

# Crossover: combine two teams
def crossover(team1, team2, total_pool):
    # Create a new team by combining parts of both teams
    new_team = team1[:3] + team2[3:]

    # Use a set to track the unique player names in the new team
    unique_players = set()
    
    # Create a list to hold the final unique team
    final_team = []

    for player in new_team:
        player_name = player["player"]  # Assuming each player is a dictionary with a "name" key
        if player_name in unique_players:
            # Find a random player from the total pool that is not already in the team
            random_player = random.choice([p for p in total_pool if p["player"] not in unique_players])
            final_team.append(random_player)
            unique_players.add(random_player["player"])
        else:
            final_team.append(player)
            unique_players.add(player_name)

    return final_team

# Mutation: randomly change one player in the team
def mutate(team, player_pool):
    # Choose a random index to mutate
    idx = random.randint(0, len(team) - 1)
    current_player = team[idx]["player"]  # Assuming each player is a dictionary with a "name" key

    # Filter the player pool to exclude the current player and any other players in the team
    available_players = [player for player in player_pool if player["player"] != current_player and player["player"] not in [p["player"] for p in team]]

    if available_players:  # Check if there are any players available for selection
        # Randomly select a new player from the available pool
        team[idx] = random.choice(available_players)

    return team
# Genetic Algorithm
def genetic_algorithm(filter_string, constraint_string, generations=100, population_size=50):
    # Initial population of random teams   
    total_players = []
    with open("vlr90.json", 'r') as f:
        total_players = json.load(f)
    exec(filter_string,globals())
    exec(constraint_string, globals())
    player_pool = filter_dataset(total_players)
    population = [generate_random_team(player_pool) for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate fitness (team score) for each team
        population = [team for team in population if satisfies_constraints(team)]
        while len(population) < 50:
            for x in range(population_size):
                team = generate_random_team(player_pool)
                if(satisfies_constraints(team)):
                    population.append(team)

        population_scores = [(team, calculate_team_score(team)) for team in population]
        population_scores.sort(key=lambda x: x[1], reverse=True)
        # Selection: keep the top half of teams
        population = [team for team, score in population_scores[:population_size // 2]]
        
        # Crossover and mutation to generate the next generation
        next_generation = []
        while len(next_generation) < population_size:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2, player_pool)
            mutate(child, player_pool)
            next_generation.append(child)
        
        population = next_generation
    
    # Return the best team
    best = max(population_scores, key=lambda x: x[1])[0]
    player_list = []
    for x in best:
        player_list.append(x["player"])
    return player_list

def get_genalg_spec():
    return {
        "name": "genetic_alg_tool",
        "description": "Runs a genetic algorithm to generate a good team of 5 Valorant players, based on a constraint function that ensures that the team fits the constraints required.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filter_data": {
                    "type": "string",
                    "description": """A string which contains the code for the function filter_data. This function takes an array of json objects, "players", and returns a filtered
                    dataset based on some constraints.""",
                        },
                "satisfies_constraints": {
                    "type": "string",
                    "description": """A string which contains the code for the function satsifies_constraints. This function takes an array of json objects, "players", which checks 
                    if the team fits a set of constraints.""",
                },
            },
            "required": [
                "filter_data",
                "satisfies_constraints"
            ]
        }
    }
