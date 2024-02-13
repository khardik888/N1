import os
import json
import pandas as pd

class SelectionManager:
    def __init__(self, filename='selected_preferences.json'):
        self.filename = filename
        self.selected_items = set()
        self.load_selections()

    def load_selections(self):
        if not os.path.isfile(self.filename):
            self.selected_items = set()
            self.save_preferences([])  # Create an empty JSON file if it doesn't exist
        else:
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.selected_items = set(map(str, data))  # Ensure all items are strings
            except json.JSONDecodeError:
                self.selected_items = set()

    def save_preferences(self, preferences):
        with open(self.filename, 'w') as f:
            json.dump(preferences, f, indent=4)

    def update_selections(self, indices):
        indices = set(map(str, indices))  # Convert indices to strings
        self.selected_items.symmetric_difference_update(indices)

    def remove_selections(self, indices):
        indices_set = set(map(str, indices))
        self.selected_items.difference_update(indices_set)

    def remove_selection(self, index):
        try:
            index_str = str(index)
            self.selected_items.remove(index_str)
        except KeyError:
            pass

    def fetch_preferences(self, df):
        preferences = []
        invalid_security_ids = set()

        df['security_id'] = df['security_id'].astype(str)

        for security_id in self.selected_items:
            security_id_str = str(security_id)

            if security_id_str not in df['security_id'].values:
                print(f"Invalid security_id: {security_id_str}. Not found in DataFrame.")
                invalid_security_ids.add(security_id_str)
                continue

            try:
                row = df[df['security_id'] == security_id_str].iloc[0]
                preference = self.create_preference(row)
                preferences.append(preference)
            except (IndexError, KeyError) as e:
                print(f"Error processing security_id: {security_id_str}: {e}")
                invalid_security_ids.add(security_id_str)

        # Update selected_items to remove invalid security_ids
        self.selected_items.difference_update(invalid_security_ids)

        return preferences

    def create_preference(self, row):
        instrument_type_mapping = {
            'OPTIDX': 'OPTION',
            'OPTSTK': 'OPTION',
            'FUTIDX': 'FUTURE',
            'FUTSTK': 'FUTURE',
            'ES': 'EQUITY',
            'I': 'INDEX',
            'ETF': 'ETF'
        }
        instrument_type = instrument_type_mapping.get(row['instrument_type'], 'UNKNOWN')

        return {
            'actionType': 'ADD',
            'modeType': 'FULL',
            'scripType': instrument_type,
            'exchangeType': row['exchange'],
            'scripId': str(row['security_id'])
        }

# Usage example:
# manager = SelectionManager()
# df = pd.read_csv('security_master.csv')  # Load your DataFrame
# manager.update_selections([1, 2, 3])  # Update selections with indices
# preferences = manager.fetch_preferences(df)
# manager.save_preferences(preferences)  # Save the fetched preferences
