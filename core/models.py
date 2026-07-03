from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class VehicleVersion:

    name: str

    jpg_path: Optional[Path] = None
    pc_path: Optional[Path] = None
    info_path: Optional[Path] = None

    jpg_exists: bool = False
    pc_exists: bool = False
    info_exists: bool = False

    def get_status(self):

        if self.info_exists:
            return "Complete"

        if self.jpg_exists:
            return "Missing Info"

        return "Unknown"

    def can_create_info(self):

        return self.jpg_exists and not self.info_exists