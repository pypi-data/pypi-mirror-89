from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core_get.options.options import Options


@dataclass
class CommonOptions(Options):
    dry_run: bool = False
    offline: bool = False
    project_dir: Optional[Path] = None
    working_dir: Optional[Path] = None
    network_timeout: float = 10.0
