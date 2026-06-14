import pandas as pd
def load_data(file_path):
    try:
        data = pd.read_csv(file_path, encoding="cp1252")
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None