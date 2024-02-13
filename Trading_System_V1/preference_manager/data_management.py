import pandas as pd
import requests
import os
from config.settings import CSV_FILES, CSV_DIR

class CSVFileManager:
    @staticmethod
    def download_csv_files():
        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)
        for filename, url in CSV_FILES.items():
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(CSV_DIR, filename), 'wb') as file:
                    file.write(response.content)

    @staticmethod
    def load_csv(filename):
        path = os.path.join(CSV_DIR, filename)
        if os.path.exists(path):
            return pd.read_csv(path)
        else:
            print(f"File {filename} not found in {CSV_DIR}.")
            return pd.DataFrame()
