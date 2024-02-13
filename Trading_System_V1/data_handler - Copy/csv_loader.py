import pandas as pd
import os
import threading

class CSVLoader:
    def __init__(self, root, csv_dir='security_master'):
        self.root = root
        self.csv_dir = csv_dir
        self.df = pd.DataFrame()

    def load_csv_files(self):
        try:
            files = [f for f in os.listdir(self.csv_dir) if f.endswith('.csv')]
            return files
        except FileNotFoundError:
            return []

    def load_csv_to_df(self, selected_csv):
        if selected_csv:
            csv_path = os.path.join(self.csv_dir, selected_csv)
            self.df = pd.read_csv(csv_path, low_memory=False)
            return self.df
        return pd.DataFrame()

    def load_csv_to_df_async(self, selected_csv, callback):
        def task():
            df = self.load_csv_to_df(selected_csv)
            # Directly pass DataFrame to the callback
            self.root.after(0, lambda: callback(df))
        threading.Thread(target=task).start()
