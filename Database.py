import os.path
from cryptography.fernet import Fernet
import json


# json database format after gaining access
# {
#     "folder1": {
#         "1": {
#             "title": string,
#             "login": string,
#             "password": string,
#             "url": string,
#         },
#         "2": {
#             "title": string,
#             "login": string,
#             "password": string,
#             "url": string,
#         }
#     },
#     "folder2": {
#         "1": {
#             "title": string,
#             "login": string,
#             "password": string,
#             "url": string,
#         },
#         "2": {
#             "title": string,
#             "login": string,
#             "password": string,
#             "url": string,
#         }
#     }
#     ...
# }


# Create a file on a pc, can be later used for create database button.
def create_file(path):
    try:
        f = open(path, "x")
    except FileExistsError:
        print("File already exists.")


class Database:
    def __init__(self, path, key):
        self.key = key
        self.file = path
        self.password_dict = {}
        self.password_dict["Other"] = ""
        # When creating a new database object, passwords are initially loaded into password_dict,
        # so that they will be used later in DatabaseContent screen.
        self.load_file()

    def add_password(self, folder, title, login, password, url):
        entries = {"title": title, "login": login, "password": password, "url": url}
        if folder == "":
            folder = "Other"
        if title == "" and login == "" and password == "" and url == "":
            return
        # Add another record to the folder with higher ID.
        try:
            ids = list(self.password_dict[folder].keys())
            ids.sort(key=lambda Id: int(Id))
            if ids.__len__() == 0:
                ID = "1"
            else:
                ID = str(int(ids[-1]) + 1)
            self.password_dict[folder][ID] = entries
        except (KeyError, AttributeError):
            entry = {"1": entries}
            self.password_dict[folder] = entry
        self.save_file()

    def delete_record(self, folder, id_):
        if id_ not in self.password_dict[folder]:
            return

        self.password_dict[folder].pop(id_)
        if folder == "Other" and self.password_dict[folder] == {}:
            self.password_dict["Other"] = ""
            self.save_file()
            return
        if self.password_dict[folder] == {}:
            self.password_dict.pop(folder)

        # print(self.password_dict)
        self.save_file()

    def load_file(self):
        if not os.path.exists(self.file):
            create_file(self.file)
            return

        if os.stat(self.file).st_size == 0:
            return

        with open(self.file, 'r') as f:
            if not os.path.getsize(self.file) > 0:
                return

            encrypted_json_dict = f.read()
            json_dict = Fernet(self.key).decrypt(encrypted_json_dict.encode()).decode()

            # From JSON back to Python dictionary
            self.password_dict = json.loads(json_dict)

    def save_file(self):
        if self.file is None:
            return
        # Python's dictionary can't be encrypted, but JSON can be, so we encrypt it in JSON format instead.
        json_dict = json.dumps(self.password_dict)
        encrypted_json_dict = Fernet(self.key).encrypt(json_dict.encode())

        with open(self.file, 'wb') as f:
            f.write(encrypted_json_dict)

    def get_password(self, site):
        if site not in self.password_dict:
            return

        return self.password_dict[site]
