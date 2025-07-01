import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

data_file = 'Flight_historical.json'




# Load environment variables from .env file
load_dotenv()


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        """Get destination data from the JSON file."""
        try:
            with open(data_file, "r") as file:
                flight_data = file.read()
                self.destination_data = json.loads(flight_data)  # Parse JSON string to dictionary
                return self.destination_data
        except FileNotFoundError:
            print(f"Path to {data_file} not found. Returning empty data.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: path to '{data_file}' contains invalid JSON.")
            return {}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}

    def update_destination_code(self):
        # Load the original JSON
        with open(data_file, 'r') as file:
            data = json.load(file)

        # Update iataCode in place for each user and their cities
        for user in self.destination_data:
            if user in data:  # Make sure the user exists in both data structures
                for updated_city in self.destination_data[user]:
                    for city in data[user]:
                        if city["id"] == updated_city["id"]:
                            city["iataCode"] = updated_city["iataCode"]

        # Write the modified JSON back to the file
        with open(data_file, 'w') as file:
            json.dump(data, file, indent=2)
    

    def add_flight_data(flight_data):
        """Add flight data to the JSON file."""
        with open(data_file, 'a') as file:
            file.write(flight_data + '\n')

    def delete_flight_data(flight_id):
        """Delete flight data by ID."""
        pass