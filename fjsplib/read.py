from pathlib import Path
from typing import Union

from fjsplib.Instance import Instance

ProcessingData = list[tuple[int, int]]
Arc = tuple[int, int]


def parse_job_line(line: list[int]) -> list[ProcessingData]:
    """
    Parses a FJSPLIB job data line of the following form:

        <num operations> * (<num machines> * (<machine> <processing time>))

    In words, the first value is the number of operations. Then, for each
    operation, the first number represents the number of machines that can
    process the operation, followed by, the machine index and processing time
    for each eligible machine.

    Note that the machine indices start from 1, so we subtract 1 to make them
    zero-based.
    """
    num_operations = line[0]
    operations = []
    idx = 1

    for _ in range(num_operations):
        num_pairs = int(line[idx]) * 2
        machines = line[idx + 1 : idx + 1 + num_pairs : 2]
        durations = line[idx + 2 : idx + 2 + num_pairs : 2]
        operations.append([(m - 1, d) for m, d in zip(machines, durations)])

        idx += 1 + num_pairs

    return operations


def classic_precedences(jobs: list[list[ProcessingData]]) -> list[Arc]:
    """
    Computes precedence relationships according to the classic FJSP definition,
    where operations are processed in the order they appear in the job data.
    """
    precedences: list[Arc] = []
    idx = 0

    for operations in jobs:
        arcs = range(idx, idx + len(operations) - 1)
        precedences.extend((i, i + 1) for i in arcs)
        idx += len(operations)

    return precedences


def read(loc: Path) -> Instance:
    """
    Reads an FJSPLIB instance.

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
    num_jobs, num_machines = lines[0][0], lines[0][1]

    # The remaining lines contain the job-operation data, where each line
    # represents a job and its operations.
    jobs = [parse_job_line(line) for line in lines[1:]]

    # TODO Identify "OPERATION_PRECEDENCE_DATA" and parse accordingly.

    # The remaining data can be computed from the job data.
    num_operations = len([op for operations in jobs for op in operations])
    precedences = classic_precedences(jobs)

    return Instance(
        num_jobs,
        num_machines,
        num_operations=num_operations,
        jobs=jobs,
        precedences=precedences,
    )


def file2lines(loc: Union[Path, str]) -> list[list[int]]:
    with open(loc, "r") as fh:
        lines = [line for line in fh.readlines() if line.strip()]

    def parse_num(word: str):
        return int(word) if "." not in word else int(float(word))

    return [[parse_num(x) for x in line.split()] for line in lines]
