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
    stringified_json_data = json.dumps(data)
    f = open(filepath, 'w')
    f.write(stringified_json_data)
    f.close
    return True