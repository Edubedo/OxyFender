import json

class Configuration:
    def __init__(self, config_file="words.json"):
        self.config_file = config_file
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"language": "english"}

    def save_settings(self):
        with open(self.config_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_language(self):
        return self.settings.get("language", "english")

    def set_language(self, language):
        self.settings["language"] = language
        self.save_settings()
