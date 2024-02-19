from pathlib import Path

from numpy.testing import assert_equal

from fjsplib.write import write
from tests.utils import read


def test_write(tmp_path: Path):
    instance = read("data/classic.fjs")
    write(tmp_path / "classic.fjs", instance)

    expected = [
        "2 3 1.0",
        "1 2 1 1 2 2",
        "2 1 1 1 2 3 1 2 1",
    ]
    with open(tmp_path / "classic.fjs", "r") as fh:
        assert_equal(fh.read().splitlines(), expected)
