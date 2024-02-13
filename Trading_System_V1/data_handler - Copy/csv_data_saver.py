import csv
import os
import threading
import logging
import time  # Added to implement a loop

class CSVDataSaver:
    def __init__(self, directory='saved_csv_files', flush_interval=5, fieldnames=None):
        self.directory = directory
        self.flush_interval = flush_interval
        self.fieldnames = fieldnames if fieldnames else ['scrip_id', 'data']
        self.file_handles = {}
        self.writers = {}
        self.buffers = {}
        self.lock = threading.Lock()

        # Set up logging
        self.logger = logging.getLogger('CSVDataSaver')
        logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more detailed logs

        # Create the directory if it does not exist
        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory, exist_ok=True)
            except Exception as e:
                self.logger.exception(f"Error creating directory {self.directory}: {e}")

        self.logger.info(f"CSVDataSaver initialized. Saving files to {self.directory}")

    def buffer_data(self, scrip_id, data):
        with self.lock:
            try:
                if scrip_id not in self.buffers:
                    self.buffers[scrip_id] = []
                    self._create_file(scrip_id)
                    self.logger.info(f"Buffer and file created for scrip_id: {scrip_id}")

                # Debug: Check if data is being added
                self.logger.debug(f"Received data for scrip_id {scrip_id}: {data}")

                self.buffers[scrip_id].append(data)
                self.logger.debug(f"Data buffered for scrip_id {scrip_id}: {data}")

                if len(self.buffers[scrip_id]) >= self.flush_interval:
                    self.logger.info(f"Flushing buffer for scrip_id {scrip_id}")
                    self.flush_buffer(scrip_id)
            except Exception as e:
                self.logger.exception(f"Error buffering data for scrip_id {scrip_id}: {e}")

    def _create_file(self, scrip_id):
        file_name = os.path.join(self.directory, f'scrip_{scrip_id}.csv')
        self.file_handles[scrip_id] = open(file_name, 'a', newline='')
        self.writers[scrip_id] = csv.DictWriter(self.file_handles[scrip_id], fieldnames=self.fieldnames)

        if os.path.getsize(file_name) == 0:
            self.writers[scrip_id].writeheader()
            self.logger.info(f"CSV header written for {file_name}")

    def flush_buffer(self, scrip_id):
        with self.lock:
            try:
                if scrip_id not in self.buffers or not self.buffers[scrip_id]:
                    self.logger.info(f"No data to flush for scrip_id {scrip_id}")
                    return

                # Debug: Check buffer content before flushing
                self.logger.debug(f"Flushing buffer for scrip_id {scrip_id}, buffer content: {self.buffers[scrip_id]}")

                for data in self.buffers[scrip_id]:
                    self.writers[scrip_id].writerow(data)

                # Ensure data is written to the file
                self.file_handles[scrip_id].flush()
                self.buffers[scrip_id] = []
                self.logger.info(f"Buffer flushed and cleared for scrip_id {scrip_id}")
            except Exception as e:
                self.logger.exception(f"Error flushing buffer for scrip_id {scrip_id}: {e}")

    def close_files(self):
        with self.lock:
            for scrip_id, file_handle in self.file_handles.items():
                file_handle.close()
                self.logger.info(f"File closed for scrip_id {scrip_id}")

    def ensure_flush_and_close(self):
        with self.lock:
            try:
                for scrip_id in list(self.buffers.keys()):
                    self.flush_buffer(scrip_id)
                self.close_files()
                self.logger.info("All buffers flushed and files closed")
            except Exception as e:
                self.logger.exception("Error in ensure_flush_and_close: {e}")

def run_data_processing():
    # Create an instance of CSVDataSaver
    csv_saver = CSVDataSaver(flush_interval=10, fieldnames=['scrip_id', 'price', 'volume'])

    while True:
        # Simulate receiving data (replace this with your actual data source)
        data = {
            'scrip_id': 'scrip1',
            'price': 100,
            'volume': 150
        }

        # Process and buffer the received data
        scrip_id = data['scrip_id']
        csv_saver.buffer_data(scrip_id, data)

        # Sleep for a while before checking for new data
        time.sleep(1)  # Adjust the sleep duration as needed

if __name__ == "__main__":
    run_data_processing()
