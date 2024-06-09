import numpy as np
import pandas as pd

# Defining the locations and their multipliers
locations = ['Campus', 'Ayeduase', 'Kotei', 'Boadi', 'Atonsu', 'Tech junction', 'Newsite', 'Bomsu']
location_multipliers = {
    'Campus': 1.6,
    'Ayeduase': 1.5,
    'Kotei': 1.4,
    'Boadi': 1.3,
    'Atonsu': 1.3,
    'Tech junction': 1.3,
    'Newsite': 1.1,
    'Bomsu': 1.1
}

#Defining boolean response
response = ["Yes","No"] 

infra_app_cost = {
    'Tv': 100,
    'Air_conditioner': 100,
    'Refrigerator': 100,    
    'Water_heater': 60,
    'Modern_Wardrobe': 40,
    'Back_up_power_supply': 150,
    'Gym': 100,
    'Elevator': 200,
    'Modernized_bathrooms': 120
}

# Number of people in a room and their base price
room_sizes = [1, 2, 3, 4]

# Base price per person in a room
base_price_per_person = 300  

# Define room size base prices
room_base_prices = {
    1: 6000,
    2: 4000,
    3: 3500,
    4: 2500,
    5: 1500,
    6: 1000
}


def generate_data(num_samples):
    """
    Generate a synthetic dataset for hostel pricing based on location, appliances, infrastructure, and room size.
    
    This function produces a specified number of samples, each representing a hostel room with various attributes.
    It calculates historical prices and current prices based on predefined multipliers for different locations.

    Parameters:
    num_samples (int): The number of samples to generate.

    Returns:
    pd.DataFrame: A DataFrame containing the generated dataset with the following columns:
        - 'Location': The location of the hostel (string).
        - 'Appliances': A list of appliances present in the room (list of strings).
        - 'Infrastructure': A list of infrastructure features available in the hostel (list of strings).
        - 'Room size': The size of the room (int, number of people it can accommodate).
        - 'Number of people in a room': The number of people in the room (int).
        - 'Historical pricing data': The historical price of the room based on base prices and additional features (float).
        - 'Current Price': The current price of the room, adjusted by the location multiplier (float).
    """
    data = []

    for _ in range(num_samples):
        location = np.random.choice(locations)
        choices =  {
            'Tv' : np.random.choice(response) ,
            'Air_conditioner' : np.random.choice(response),
            'Refrigerator' : np.random.choice(response) , 
            'Water_heater' : np.random.choice(response),
            'Modern_Wardrobe' : np.random.choice(response),
            'Back_up_power_supply' : np.random.choice(response),
            'Gym' : np.random.choice(response),
            'Elevator' : np.random.choice(response),
            'Modernized_bathrooms' : np.random.choice(response)
        }
        infra_app = 0
        for choice in choices:
            if choices[choice] == "Yes":
                infra_app += infra_app_cost[choice]

        room_size = np.random.choice(room_sizes)
        num_people = room_size  # Assuming the number of people is equal to room size
        
        historical_price = (room_base_prices[room_size] +
                            infra_app
                            )
        
        current_price = historical_price * location_multipliers[location]
        
        data.append([
            location, 
            *[choice for choice in choices.values()], 
            room_size, 
            num_people, 
            historical_price, 
            current_price
        ])
    
    columns = ['Location', *[key for key in choices.keys()] ,'Room size', 'Number of people in a room', 'Historical pricing data', 'Current Price']
    return pd.DataFrame(data, columns=columns)

synthetic_data = generate_data(40000)

print(synthetic_data.head())

#Saving the generated dataset to a CSV file
synthetic_data.to_csv('synthetic_hostel_data.csv', index=False)