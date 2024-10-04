import json

with open('vlr90.json', 'r') as f:
    total_players = json.load(f)


def average_properties(objects):
    # Initialize an empty dictionary to store the sum of each property
    property_sums = {}
    
    # Iterate through each object in the dataset
    for obj in objects:
        for key, value in obj.items():
            # Check if the property is a number (float or int)
            if isinstance(value, (int, float)):
                # If the key doesn't exist in the property_sums dict, initialize it with 0
                if key not in property_sums:
                    property_sums[key] = 0
                # Add the current value to the sum for this property
                property_sums[key] += value
    
    # Calculate the averages for each property
    num_objects = len(objects)
    average_object = {key: value / num_objects for key, value in property_sums.items()}
    
    return average_object


average_obj = average_properties(total_players)
print(average_obj)

