import json
import math

def calculate_mean(json_array):
    # Create a dictionary to store the sum of each property
    sums = {}
    count = len(json_array)
    
    # Iterate over each object in the JSON array
    for obj in json_array:
        for key, value in obj.items():
            if isinstance(value, (int, float)):  # Check if the property is numeric
                if key not in sums:
                    sums[key] = 0
                sums[key] += value
    
    # Calculate the mean for each numeric property
    means = {key: sums[key] / count for key in sums}
    return means

def calculate_std_dev(json_array, means):
    # Create a dictionary to store the squared differences from the mean
    squared_diffs = {}
    count = len(json_array)
    
    # Iterate over each object in the JSON array
    for obj in json_array:
        for key, value in obj.items():
            if isinstance(value, (int, float)):  # Check if the property is numeric
                if key not in squared_diffs:
                    squared_diffs[key] = 0
                squared_diffs[key] += (value - means[key]) ** 2
    
    # Calculate the standard deviation for each numeric property
    std_devs = {key: math.sqrt(squared_diffs[key] / (count - 1)) for key in squared_diffs}
    return std_devs
def implement_zscores(data):
    means = calculate_mean(data)
    std_devs = calculate_std_dev(data, means)
    for player in range(len(data)):
        z_score_sum = 0
        for stat, value in data[player].items():
            if isinstance(value, (int, float)):
                mean = means[stat]
                std_dev = std_devs[stat]
                # Calculate z-score
                if stat == "first_deaths_per_round":
                    z_score_sum -= (value - mean) / std_dev if std_dev != 0 else 0
                elif stat == "rounds_played" or stat == "rating":
                    continue
                else:
                    z_score_sum += (value - mean) / std_dev if std_dev != 0 else 0

        data[player]["zscore"] = z_score_sum

def process_agents(data):
    for x in data:
        array = x["agents"].strip("[]").split(",")
        array = [item.strip() for item in array]
        x["agents"] = array
    
def combine_regions(data):
    for x in data:
        if x["region"] in ["ap","jp","oce"]:
            x["region"] = "ap"
        if x["region"] in ["na","sa"]:
            x["region"] = "amer"
        if x["region"] in ["eu","mn"]:
            x["region"] = "emea"
with open('vlr90.json', 'r') as f:
    megadata = json.load(f)
implement_zscores(megadata)
combine_regions(megadata)
with open('vlr90.json', 'w') as f:
    json.dump(megadata, f, separators=None)




