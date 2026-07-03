from pathlib import Path


def find_vehicle_folder(root: Path):

    vehicles = root / "vehicles"

    if not vehicles.exists():
        return None

    for folder in vehicles.iterdir():

        if folder.is_dir():
            return folder

    return None