from pathlib import Path
from zipfile import ZipFile

from core.models import VehicleVersion


IMAGE_EXTENSIONS = {".jpg", ".jpeg"}


class ModScanner:

    def scan(self, path: str):

        path = Path(path)

        if path.is_dir():
            return self._scan_folder(path)

        return self._scan_zip(path)

    # --------------------------------------------------

    def _scan_folder(self, folder: Path):

        vehicles = folder / "vehicles"

        if not vehicles.exists():
            return []

        vehicle_folder = None

        for item in vehicles.iterdir():

            if item.is_dir():
                vehicle_folder = item
                break

        if vehicle_folder is None:
            return []

        return self._scan_directory(vehicle_folder)

    # --------------------------------------------------

    def _scan_zip(self, zip_path: Path):

        versions = {}

        with ZipFile(zip_path) as z:

            files = z.namelist()

            vehicle_root = None

            for file in files:

                parts = Path(file).parts

                if len(parts) >= 2 and parts[0] == "vehicles":

                    vehicle_root = Path(parts[0]) / parts[1]
                    break

            if vehicle_root is None:
                return []

            prefix = vehicle_root.as_posix() + "/"

            for file in files:

                if not file.startswith(prefix):
                    continue

                relative = Path(file).relative_to(vehicle_root)

                if len(relative.parts) != 1:
                    continue

                suffix = relative.suffix.lower()

                stem = relative.stem

                filename = relative.name

                # ---------------- JPG ----------------

                if suffix in IMAGE_EXTENSIONS:

                    version = versions.setdefault(
                        stem,
                        VehicleVersion(stem)
                    )

                    version.jpg_exists = True
                    version.jpg_path = relative

                # ---------------- PC ----------------

                elif suffix == ".pc":

                    version = versions.setdefault(
                        stem,
                        VehicleVersion(stem)
                    )

                    version.pc_exists = True
                    version.pc_path = relative

                # -------------- INFO ----------------

                elif filename.startswith("info_") and suffix == ".json":

                    name = filename[5:-5]

                    version = versions.setdefault(
                        name,
                        VehicleVersion(name)
                    )

                    version.info_exists = True
                    version.info_path = relative

        return sorted(
            versions.values(),
            key=lambda x: x.name.lower()
        )

    # --------------------------------------------------

    def _scan_directory(self, folder: Path):

        versions = {}

        for file in folder.iterdir():

            if not file.is_file():
                continue

            suffix = file.suffix.lower()

            stem = file.stem

            if suffix in IMAGE_EXTENSIONS:

                version = versions.setdefault(
                    stem,
                    VehicleVersion(stem)
                )

                version.jpg_exists = True
                version.jpg_path = file

            elif suffix == ".pc":

                version = versions.setdefault(
                    stem,
                    VehicleVersion(stem)
                )

                version.pc_exists = True
                version.pc_path = file

            elif file.name.startswith("info_") and suffix == ".json":

                name = file.name[5:-5]

                version = versions.setdefault(
                    name,
                    VehicleVersion(name)
                )

                version.info_exists = True
                version.info_path = file

        return sorted(
            versions.values(),
            key=lambda x: x.name.lower()
        )