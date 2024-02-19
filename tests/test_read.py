from pathlib import Path

import pytest
from numpy.testing import assert_equal

from fjsplib.read import parse_job_line
from tests.utils import read


def test_read():
    """
    Tests that ``read`` correctly reads an FJSP instance from a file location.
    """
    loc = "data/classic.fjs"
    instance = read(Path(loc))

    assert_equal(instance.num_jobs, 2)
    assert_equal(instance.num_machines, 3)
    assert_equal(instance.num_operations, 3)
    assert_equal(
        instance.jobs,
        [
            [[(0, 1), (1, 2)]],
            [[(0, 1)], [(2, 1), (1, 1)]],
        ],
    )
    assert_equal(instance.precedences, [(1, 2)])


@pytest.mark.parametrize(
    "line, expected",
    [
        ([1, 1, 1, 1], [[(0, 1)]]),
        ([2, 1, 1, 1, 1, 1, 1], [[(0, 1)], [(0, 1)]]),
        ([1, 2, 3, 4, 5, 6], [[(2, 4), (4, 6)]]),
    ],
)
def test_parse_job_line(
    line: list[int], expected: list[list[tuple[int, int]]]
):
    """
    Tests that a FJSPLIB job data line is correctly parsed.
    """
    assert_equal(parse_job_line(line), expected)
