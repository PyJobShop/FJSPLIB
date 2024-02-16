from numpy.testing import assert_equal

from fjsplib import read


def test_read():
    """
    Tests that ``read`` correctly reads an FJSP instance from a file location.
    """
    instance = read("tests/data/classic.fjs")

    assert_equal(instance.num_jobs, 2)
    assert_equal(instance.num_machines, 3)
    assert_equal(instance.num_operations, 3)
    assert_equal(
        instance.operations,
        [
            {"job": 0, "processing_times": [(0, 1), (1, 2)]},
            {"job": 1, "processing_times": [(0, 1)]},
            {"job": 1, "processing_times": [(2, 1), (1, 1)]},
        ],
    )
    assert_equal(instance.precedences, [(1, 2)])
