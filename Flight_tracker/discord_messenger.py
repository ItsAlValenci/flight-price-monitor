from discord import SyncWebhook
import re
import os
from dotenv import load_dotenv
WEBHOOK_URL = os.environ["DISCORD_URL"] 


# Default webhook URL - should be configured by the user
DEFAULT_WEBHOOK_URL = WEBHOOK_URL

class DiscordMessenger:
    """Class for sending messages to Discord via webhooks"""
    
    def __init__(self, webhook_url=None):
        """Initialize the Discord messenger with a webhook URL
        """
        self.webhook_url = webhook_url or DEFAULT_WEBHOOK_URL
        
        # Extract webhook ID and token from URL
        webhook_pattern = r"https://discord\.com/api/webhooks/([^/]+)/([^/]+)"
        match = re.match(webhook_pattern, self.webhook_url)
        
        if match:
            webhook_id, webhook_token = match.groups()
            self.webhook = SyncWebhook.from_url(self.webhook_url)
        else:
            raise ValueError("Invalid Discord webhook URL format")
    
    def send_message(self, message):
        """Send a simple text message to Discord
        """
        try:
            self.webhook.send(message)
            return True
        except Exception as e:
            print(f"Error sending Discord message: {e}")
            return False
    
    def send_flight_deal(self, city, price, carrier, origin_airport, destination_airport, 
                         out_date, return_date, user="User"):
        """Send a formatted flight deal message to Discord
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            message = f"\n\n✈️**FLIGHT DEAL ALERT!** ✈️\n\n"
            message += f"**{user}**\n"
            message += f"**Route:** {origin_airport} → {city} {destination_airport}\n"
            message += f"**Price:** ${price} with {carrier}\n"
            message += f"**Dates:** from {out_date} to {return_date}\n\n"
            
            self.webhook.send(message)
            return True
        except Exception as e:
            print(f"Error sending flight deal to Discord: {e}")
            return False