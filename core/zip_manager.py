import shutil
import tempfile

from pathlib import Path
from zipfile import ZipFile


class ZipManager:

    def __init__(self):

        self.temp_dir = None
        self.original_zip = None
        self.extract_path = None

    # ----------------------------------------------------------

    def open(self, zip_path: str):

        self.original_zip = Path(zip_path)

        self.temp_dir = tempfile.TemporaryDirectory()

        self.extract_path = Path(self.temp_dir.name)

        with ZipFile(self.original_zip, "r") as zip_file:

            zip_file.extractall(self.extract_path)

        return self.extract_path

    # ----------------------------------------------------------

    def save(self):

        backup = self.original_zip.with_suffix(".backup.zip")

        if not backup.exists():

            shutil.copy2(self.original_zip, backup)

        temp_zip = self.original_zip.with_suffix(".new.zip")

        with ZipFile(temp_zip, "w") as zip_file:

            for file in self.extract_path.rglob("*"):

                if file.is_dir():
                    continue

                archive_name = file.relative_to(self.extract_path)

                zip_file.write(
                    file,
                    archive_name.as_posix()
                )

        self.original_zip.unlink()

        temp_zip.rename(self.original_zip)

    # ----------------------------------------------------------

    def close(self):

        if self.temp_dir:

            self.temp_dir.cleanup()