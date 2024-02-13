# csv_creator.py
import os
import pandas as pd
from config import CSV_DIR

class CSVLoader:
    def __init__(self):
        self.df = pd.DataFrame()

    def load_csv_to_df(self, filename):
        csv_path = os.path.join(CSV_DIR, filename)
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path, low_memory=False)
        else:
            print(f"{filename} not found.")
        return self.df

    def load_csv_files(self):
        """Returns a list of CSV filenames found in the specified directory."""
        return [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]
