from dataclasses import dataclass
from typing import List

from core_get.options.options import Options


@dataclass
class TestOptions(Options):
    vunit_arguments: List[str]
