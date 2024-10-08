import random
import math
import json


# Function to filter players based on the sums of minimums
def filter_dataset(player_data,constraints):
    filters = {}

    def sum_minimums(category):
        return sum(min_value for min_value, _ in category.values())
    # Calculate the sum of minimums for each category
    region_sum = sum_minimums(constraints['region'])
    league_sum = sum_minimums(constraints['league'])
    org_sum = sum_minimums(constraints['org'])

    # Determine which categories will be used for filtering based on the sum of minimums
    if region_sum == 5:
        filters['region'] = [region for region, (min_val, _) in constraints['region'].items() if min_val > 0]
    if league_sum == 5:
        filters['league'] = [league for league, (min_val, _) in constraints['league'].items() if min_val > 0]
    if org_sum == 5:
        filters['org'] = [org for org, (min_val, _) in constraints['org'].items() if min_val > 0]

    # Filter players based on the selected filters
    def meets_criteria(player,stats):
        region_check = 'region' not in filters or player['region'] in filters['region']
        league_check = 'league' not in filters or player['league'] in filters['league']
        org_check = 'org' not in filters or player['org'] in filters['org']
        for k,v in stats.items():
            if player[k] <= v:
                return False
        
        return region_check and league_check and org_check



    return [player for player in player_data if meets_criteria(player, constraints["stats"])]


# Scoring function based on individual player stats
def calculate_team_score(team):
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

def satisfies_constraints(team, constraints):
    for region in constraints["region"]:
        count = 0
        for player in team:
            if player["region"] == region:
                count+=1
        if count < constraints["region"][region][0] or count > constraints["region"][region][1]:
            return False
    for league in constraints["league"]:
        count = 0
        for player in team:
            if player["league"] == league:
                count+=1
        if count < constraints["league"][league][0] or count > constraints["league"][league][1]:
            return False
    for org in constraints["org"]:
        count = 0
        for player in team:
            if player["org"] == org:
                count+=1
        if count < constraints["org"][org][0] or count > constraints["org"][org][1]:
            return False
    for playerName in constraints["player"]:
        playerFound = False
        for player in team:
            if player["player"] == playerName:
                playerFound = True
        if not playerFound:
            return False
    
    unique_agents = set()

    for player in team:
        unique_agents.update(player["agents"])

    valorant_roles = {
        "smokes": ["omen", "brimstone", "viper", "astra", "harbor", "clove"],
        "entry": ["reyna", "phoenix", "yoru", "iso"],
        "intel_gatherer": ["sova", "fade", "cypher", "gekko", "skye"],
        "lurker": ["cypher", "omen", "chamber", "yoru", "viper", "killjoy"],
        "flank_watch": ["killjoy", "cypher", "chamber", "vyse"],
        "flash_initiator": ["skye", "kayo", "breach", "phoenix", "reyna", "gekko"],
        "movement_duelist": ["reyna", "raze", "neon", "jett", "yoru"],
        "controller": ["astra", "brimstone", "harbor", "omen", "viper", "clove"],
        "sentinel": ["chamber", "cypher", "killjoy", "sage", "vyse"],
        "duelist": ["jett", "neon", "phoenix", "raze", "reyna", "yoru", "iso"],
        "initiator": ["breach", "fade", "gekko", "kayo", "skye", "sova"]
    }

    all_agents = [
        "astra", "breach", "brimstone", "chamber", "clove", "cypher", "fade",
        "gekko", "harbor", "iso", "jett", "kayo", "killjoy", "neon", "omen",
        "phoenix", "raze", "reyna", "sage", "skye", "sova", "viper", "vyse", "yoru"
    ]
    for agenttype in constraints["agents"]:
        if agenttype in valorant_roles:
            count = 0
            for player in team:
                for agent in player["agents"]:
                    if agent in valorant_roles[agenttype]:
                        count+=1
                        break
            if count < constraints["agents"][agenttype][0] or count > constraints["agents"][agenttype][1]:
                return False
        elif agenttype in all_agents:
            if agenttype in all_agents:
                count = 0
                for player in team:
                    if agenttype in player["agents"]:
                        count+=1
                if count < constraints["agents"][agenttype][0] or count > constraints["agents"][agenttype][1]:
                    return False
        elif agenttype == "agentCount":
            if constraints["agents"][agenttype] > len(unique_agents):
                return False
            
    return True


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
def genetic_algorithm(constraints, generations=100, population_size=50):
    # Initial population of random teams   
    total_players = []
    with open(r"..\..\backend\API\vlr90.json", 'r') as f:
        total_players = json.load(f)
    constraintjson = json.loads(constraints)
    if "region" not in constraintjson:
        constraintjson["region"] = {}
    if "league" not in constraintjson:
        constraintjson["league"] = {}
    if "org" not in constraintjson:
        constraintjson["org"] = {}
    if "player" not in constraintjson:
        constraintjson["player"] = {}
    if "stats" not in constraintjson:
        constraintjson["stats"] = {}
    if "agents" not in constraintjson:
        constraintjson["agents"] = {}
    player_pool = filter_dataset(total_players,constraintjson)
    population = [generate_random_team(player_pool) for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate fitness (team score) for each team
        population = [team for team in population if satisfies_constraints(team,constraintjson)]
        while len(population) < 50:
            for x in range(population_size):
                team = generate_random_team(player_pool)
                if(satisfies_constraints(team,constraintjson)):
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
        "description": "Runs a genetic algorithm to generate a good team of 5 Valorant players, based on a constraint json that ensures that the team fits the constraints required.",
        "input_schema": {
            "type": "object",
            "properties": {
                "constraint_data": {
                    "type": "string",
                    "description": """A string which contains a json object which contains data to represent the different requests and restraints of the team.""",
                        },
            },
            "required": [
                "constraint_data"
            ]
        }
    }
