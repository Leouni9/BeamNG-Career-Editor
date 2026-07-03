from pathlib import Path


class JsonEditor:

    def __init__(self, file_path: Path):

        self.file_path = file_path

        self.lines = []

        self.load()

    # ------------------------------------------

    def load(self):

        with open(
            self.file_path,
            "r",
            encoding="utf8"
        ) as file:

            self.lines = file.readlines()

    # ------------------------------------------

    def save(self):

        with open(
            self.file_path,
            "w",
            encoding="utf8",
            newline=""
        ) as file:

            file.writelines(self.lines)