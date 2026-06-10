import pandas as pd
def load_data(file_path):
    try:
        data=pd.read_csv(file_path)
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None