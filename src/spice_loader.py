import os
from pathlib import Path

import spiceypy as spice

from src.config import PROJECT_ROOT


def load_kernels(meta_kernel_path: Path) -> None:
    current_dir = Path.cwd()
    try:
        os.chdir(PROJECT_ROOT)
        spice.furnsh(str(meta_kernel_path.resolve()))
    finally:
        os.chdir(current_dir)


def clear_kernels() -> None:
    spice.kclear()
