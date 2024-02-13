import json
import logging
import os  # Import os for joining paths

class PreferencesManager:
    def __init__(self, logger, preferences_file='selected_preferences.json'):
        self.logger = logger
        # Use os.path.join to ensure the correct path format is used for different operating systems
        self.preferences_file_path = os.path.join(os.path.dirname(__file__), preferences_file)
        self.preferences = self.load_preferences()

    def load_preferences(self):
        try:
            with open(self.preferences_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            self.logger.error(f"Preferences file '{self.preferences_file_path}' not found.")
            return []
        except json.JSONDecodeError:
            self.logger.error(f"Error decoding JSON from '{self.preferences_file_path}'.")
            return []

    def send_preferences(self, ws):
        ws.send(json.dumps(self.preferences))
        self.logger.info(f"Sent preferences: {self.preferences}")
