import csv
from datetime import datetime
import json
import os


def get_timestamp(date=None):
    if date:
        # format 'November 20, 2022 8:23 PM'
        formatted_date = datetime.strptime(date, "%B %d, %Y %I:%M %p")
    else:
        formatted_date = datetime.now()

    return int(formatted_date.timestamp())


def get_input_file(input_folder):
    files = [
        os.path.join(input_folder, filename) for filename in os.listdir(input_folder)
    ]
    return max(files, key=os.path.getctime)


def read_file_json():
    file_path = get_input_file("backup_files")
    with open(file_path, "r") as f:
        data = json.load(f)

    return data


def read_file_csv():
    file_path = get_input_file("vocabulary_files")
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def save_output_file(data):
    file_timestamp = get_timestamp()
    file_name = f"output/vocabulary_{file_timestamp}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


if __name__ == "__main__":

    backup_file = read_file_json()
    words = []
    for item in read_file_csv():
        types = item.get("Type", "").split(", ")
        types = [f"{type}s" for type in types if type]
        timestamp = get_timestamp(item.get("Last edited time"))
        if item.get("Article"):
            item["Word"] = f'{item["Article"]} {item["Word"]}'
        word = {
            "a": "",
            "e": item.get("Example", ""),
            "g": types,
            "l": 0,
            "m": item["\ufeffMeaning"],
            "mn": "",
            "n": item.get("Forms", ""),
            "p": "",
            "s": "",
            "tsS": timestamp,
            "tsU": timestamp,
            "w": item["Word"],
            "i": {},
        }
        words.append(word)
    backup_file["words"].extend(words)
    save_output_file(backup_file)
