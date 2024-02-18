from dataclasses import dataclass
from pathlib import Path

ProcessingData = list[tuple[int, int]]
Arc = tuple[int, int]


@dataclass
class Instance:
    """
    The parsed data from the FJSPLIB instance.

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
    jobs: list[list[ProcessingData]]
    precedences: list[tuple[int, int]]


def parse_job_line(line: list[int]) -> list[ProcessingData]:
    """
    Parses a standard formatted FJSP job data line:
    - The first number is the number of operations (n >= 1) of that job.
    - Repeat for n times:
        - First a number k >= 1 that represents the number of machines that can
          process the operation.
        - Then there are k pairs of numbers (machine, processing time) that
          specify which are the machines and the processing times.

    Note that the machine indices start from 1, so we subtract 1 to make them
    zero-based.
    """
    num_operations = line[0]
    operations = []
    idx = 1

    while idx < len(line):
        num_eligible_machines = int(line[idx])
        idx += 1
        operation = []

        for _ in range(num_eligible_machines):
            machine = int(line[idx]) - 1  # make zero-based
            duration = int(line[idx + 1])
            operation.append((machine, duration))
            idx += 2

        operations.append(operation)

    assert len(operations) == num_operations

    return operations


def read(loc: Path) -> Instance:
    """
    Parses an FJSPLIB formatted instance.

    Parameters
    ----------
    loc
        Location of the instance file.

    Returns
    -------
    Instance
        The parsed instance.
    """
    lines = file2lines(loc)

    # First line contains metadata.
    num_jobs, num_machines, _ = lines[0]

    # The remaining lines contain the job-operation data, where each line
    # represents a job and its operations.
    jobs = [parse_job_line(line) for line in lines[1:]]

    # Precedence relationships between operations can be assumed from the FJSP
    # problem definition, where operations are processed in sequence of their
    # appearance in the job operation data.
    precedences: list[Arc] = []
    idx = 0

    for operations in jobs:
        job_indices = range(idx, idx + len(operations) - 1)
        precedences.extend((i, i + 1) for i in job_indices)
        idx += len(operations)

    return Instance(
        num_jobs,
        num_machines,
        num_operations=idx,
        jobs=jobs,
        precedences=precedences,
    )


def file2lines(loc: Path | str) -> list[list[int]]:
    with open(loc, "r") as fh:
        lines = [line for line in fh.readlines() if line.strip()]

    def is_int(x):  # only relevant for avg. operations data
        return "." not in x

    return [
        [int(x) if is_int(x) else int(float(x)) for x in line.split()]
        for line in lines
    ]
