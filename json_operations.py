import json
import os

def load_data(filepath):
    data = {}
    if os.path.exists(filepath):
        try:
            f = open(filepath, 'r')
            data = json.load(f)
            f.close()
            return data
        except ValueError:
            print("Decode error")
            return data
    else:
        return data
    

def save_json_data(filepath, data):
    stringified_json_data = json.dumps(data, indent=4)
    with open(filepath, 'w') as f:
        f.write(stringified_json_data)
        
    return True