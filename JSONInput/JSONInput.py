import json
import os


class JSONInput:
    file_path: str = None
    parameters: dict = None

    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            with open(file_path, "r") as file:
                self.parameters = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {file_path}")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {e}")

    def __getitem__(self, key: str):
        return self.parameters.get(key)
