import json
import os


class Options:
    config = {}

    @staticmethod
    def load():

        if not os.path.exists("config.json"):
            with open("config.json", "w") as f:
                # TODO napisać metodę statyczną do wytworzenia wszystkich dostępnych pól w opcjach i ustawienie domyślnych wartości
                pass
        with open("config.json", "r") as f:
            Options.config = json.load(f)

    @staticmethod
    def get_options():
        return Options.config
