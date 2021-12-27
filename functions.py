import json
import csv
import datetime
CSV_ENTRIES_PATH = "sessions.csv"

def get_json_data(path) -> dict:
    data: None
    try:
        with open(path, "r") as f:
            data = json.load(f)

    except: raise Exception("Couldn't read from '%s'"%path)
    else: return data

def set_json_data(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f)

    except: raise Exception("Couldn't write to '%s'"%path)
    
def get_from_db(owner: str, date: str = None) -> list:
    '''Raises exception if no data is found for owner (user)'''
    if not owner: raise Exception("I can't get anthing from the datebase without any parameters you big, fat doof")

    data = []

    with open(CSV_ENTRIES_PATH, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["owner"] == owner and not date: 
                data.append(row)
            
            elif row["owner"] == owner and row["date"] == date:
                data.append(row)

    if len(data) == 0: raise Exception("No data found for user %s"%owner)
    else: return data

def write_to_db(type: str, owner: str, smokes: float, grams: float, filter: bool, paper: bool):
    '''writes row string argument to the end of csv file'''
    current = datetime.datetime.today()
    formatted_time = current.strftime("%b %d %Y %H:%M:%S")
    line = [str(formatted_time), str(owner), str(type), float(smokes), float(grams), bool(filter), bool(paper)]
    with open(CSV_ENTRIES_PATH, "a+") as f:
        writer = csv.writer(f)
        writer.writerow(line)
        
        f.close()