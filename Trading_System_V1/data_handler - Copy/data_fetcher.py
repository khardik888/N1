import logging
from authentication.token_manager import TokenManager
from .data_parser import DataParser
from .preferences_manager import PreferencesManager
from .connection_manager import ConnectionManager
from .csv_data_saver import CSVDataSaver


# Configure logging at the beginning of the file
logging.basicConfig(level=logging.INFO)

class DataFetcher:
    def __init__(self, constants):
        self.logger = logging.getLogger('DataFetcher')
        self.token_manager = TokenManager()
        self.constants = constants
        self.data_parser = DataParser(self.logger)
        self.preferences_manager = PreferencesManager(self.logger)
        self.connection_manager = ConnectionManager(self.token_manager, self.constants, self.logger, self.on_message, self.on_open)
        self.csv_data_saver = CSVDataSaver()

    def on_message(self, ws, message):
        self.logger.info(f"Received message: {message}")
        parsed_data = self.data_parser.parse_binary(message)
        self.logger.info(f"Parsed data: {parsed_data}")

        # Buffer and save data using CSVDataSaver
        for data in parsed_data:
            self.csv_data_saver.buffer_data(data['security_id'], data)

    def on_open(self, ws):
        self.logger.info("WebSocket opened.")
        self.preferences_manager.send_preferences(ws)

    def start(self):
        self.connection_manager.connect()

if __name__ == "__main__":
    logger = logging.getLogger('Main')

    # Initialize constants and other required components here...
    constants = None  # Replace with actual constants

    # Create an instance of DataFetcher
    data_fetcher = DataFetcher(constants)

    # Start the data fetching process
    data_fetcher.start()
