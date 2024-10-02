import json
import os


class Helper:
    def __init__(self):
        self.file_path = "data.json"

    def init_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file)

    @staticmethod
    def dump_to_file(f, data):
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

    def get_key_and_delete(self, key):
        with open(self.file_path, "r+") as f:
            data = json.load(f)
            if key in data:
                value = data[key]
                del data[key]
                self.dump_to_file(f, data)
                return value
            else:
                print("Key doesn't exist")
                return None

    def get_key(self, key):
        with open(self.file_path, "r") as f:
            data = json.load(f)
            return data.get(key)

    def write_raffle_member(self, member_id):
        with open(self.file_path, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            data["raffle_member"] = member_id
            self.dump_to_file(f, data)
