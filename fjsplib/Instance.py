from dataclasses import dataclass


@dataclass
class Instance:
    """
    The FJSPLIB instance data.

    Parameters
    ----------
    num_jobs
        The number of jobs.
    num_machines
        The number of machines.
    num_operations
        The number of operations.
    jobs
        A list of job data, each job consisting of a list of operation indices.
    precedences
        A list of tuples consisting of two operation indices, representing the
        precedence relationship of two operations.
    """

    num_jobs: int
    num_machines: int
    num_operations: int
    jobs: list[list[list[tuple[int, int]]]]
    precedences: list[tuple[int, int]]
