import time
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

data_manager = DataManager()
json_data = data_manager.get_destination_data()
print("Data loaded successfully.\n")

flight_search = FlightSearch()

# Initialize notification manager for sending alerts
notification_manager = NotificationManager()
print("Notification manager initialized.\n")

# Setting City of Origin (IATA CODE)

ORIGIN_CITY_IATA = "SFO"

# ==================== Update the Airport Codes Json ====================
# Check if any city needs an IATA code for all users
empty_codes_exist = False

# Loop through all users in the JSON data
for user in json_data:
    for place in json_data[user]:
        if place["iataCode"] == "":
            empty_codes_exist = True
            break
    if empty_codes_exist:
        break

# If empty codes exist, create flight search and update all cities
if empty_codes_exist:
    flight_search = FlightSearch()
    # Update IATA codes for all users
    for user in json_data:
        for place in json_data[user]:
            if place["iataCode"] == "":
                place["iataCode"] = flight_search.get_destination_code(place["city"])
    print("IATA code updated\n")
    
    # Update the data manager and save changes
    data_manager.destination_data = json_data
    data_manager.update_destination_code()
else:
    print("Every city has an IATA code.\n")

# ==================== Search for Flights ====================

# Loop through each user in the JSON data
for user, destinations in json_data.items():
    print(f"\nSearching flights for user: {user}")
    
    for destination in destinations:
        # Get origin city from the destination data
        origin_city = destination.get("og city", ORIGIN_CITY_IATA)
        
        # Parse departure and return dates from the JSON
        try:
            # Try to parse dates from JSON, fallback to default if not valid
            dep_date_str = destination.get("dep_date")
            ret_date_str = destination.get("ret_date")
            
            # Parse dates if they exist and are valid
            if dep_date_str and ret_date_str:
                try:
                    departure_date = datetime.strptime(dep_date_str, "%Y-%m-%d")
                    return_date = datetime.strptime(ret_date_str, "%Y-%m-%d")
                except ValueError:
                    # Fallback to default dates if parsing fails
                    departure_date = datetime.now() + timedelta(days=1)
                    return_date = datetime.now() + timedelta(days=(7*3))
            else:
                # Use default dates if not specified
                departure_date = datetime.now() + timedelta(days=1)
                return_date = datetime.now() + timedelta(days=(7*3))
                
        except Exception as e:
            print(f"Error parsing dates for {destination['city']}: {e}")
            # Fallback to default dates
            departure_date = datetime.now() + timedelta(days=1)
            return_date = datetime.now() + timedelta(days=(7*3))
        
        print(f"Getting rates for {origin_city} to {destination['city']}...")
        print(f"Dates: {departure_date.strftime('%Y-%m-%d')} to {return_date.strftime('%Y-%m-%d')}")
        
        flights = flight_search.check_flights(
            origin_city,
            destination["iataCode"],
            from_time=departure_date,
            to_time=return_date
        )
        cheapest_flight = find_cheapest_flight(flights)
        print(f"{destination['city']}: ${cheapest_flight.price} from {cheapest_flight.carrier}\n")
        
        # Send notification to Discord if a valid flight was found
        if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["LowestPrice"]:
            notification_manager.send_flight_deal_notification(
                flight_data=cheapest_flight,
                city=destination['city'],
                user=user
            )
            print(f"Discord notification sent for {user}'s {destination['city']} deal")
        
        # Slowing down requests to avoid rate limit
        time.sleep(2)
