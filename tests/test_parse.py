from numpy.testing import assert_equal
from pyjobshop.parse import parse


def test_parse_fjsp():
    """
    Tests that ``parse`` correctly parses a simple a FJSP instance.
    """
    url = "data/fjsp/instance.json"
    instance = parse(url)

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

    pass
