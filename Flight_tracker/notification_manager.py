from discord_messenger import DiscordMessenger

class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""
    
    def __init__(self, webhook_url=None):
        """Initialize the notification manager with a Discord webhook"""
        self.discord_messenger = DiscordMessenger(webhook_url)
    
    def send_flight_deal_notification(self, flight_data, city, user="User"):
        """Send a notification about a flight deal
        
        Args:
            flight_data: Flight data object
            city: Destination city
            user: User name for the notification (defaults to "User")
        """
        return self.discord_messenger.send_flight_deal(
            city=city,
            price=flight_data.price,
            carrier=flight_data.carrier,
            origin_airport=flight_data.origin_airport,
            destination_airport=flight_data.destination_airport,
            out_date=flight_data.out_date,
            return_date=flight_data.return_date,
            user=user
        )
    
    def send_custom_message(self, message):
        """Send the message via Discord"""
        return self.discord_messenger.send_message(message)