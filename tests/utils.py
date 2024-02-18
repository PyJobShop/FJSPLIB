from functools import lru_cache
from pathlib import Path

from fjsplib.read import read as _read


@lru_cache
def read(where: str, *args, **kwargs):
    """
    Lightweight wrapper around ``fjsplib.read.read()``, reading problem files
    relative to the current directory.
    """
    this_dir = Path(__file__).parent
    return _read(this_dir / where, *args, **kwargs)
