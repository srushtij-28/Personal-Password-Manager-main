import json
import os


def load_data(filename, default=None):
    if default is None:
        default = []

    if not os.path.exists(filename):
        return default

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return default


def save_data(filename, data):
    directory = os.path.dirname(filename)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
