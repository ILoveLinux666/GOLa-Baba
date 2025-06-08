import json
import os


class Options:
    config = {}

    @staticmethod
    def default_config():
        return {
            "size": [300, 300],
            "cell_size": 10
        }

    @staticmethod
    def load():
        if not os.path.exists("config.json"):
            Options.config = Options.default_config()
            Options.save()
        else:
            with open("config.json", "r", encoding="utf-8") as f:
                Options.config = json.load(f)

    @staticmethod
    def save():
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(Options.config, f, indent=4)

    @staticmethod
    def get_options():
        return Options.config

    @staticmethod
    def set_option(key, value):
        Options.config[key] = value
        Options.save()
