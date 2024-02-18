from pathlib import Path

from numpy.testing import assert_equal

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
