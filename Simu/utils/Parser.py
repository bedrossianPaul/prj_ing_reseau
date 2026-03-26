import pandas as pd

class Parser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except Exception as e:
            print(f"Error parsing file: {e}")
            return None