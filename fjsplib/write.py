from pathlib import Path
from typing import Union

from .Instance import Instance


def write(where: Union[Path, str], instance: Instance):
    """
    Writes a problem instance to file in FJSPLIB format.

    Parameters
    ----------
    where
        Location to write the instance to.
    instance
        The problem instance.
    """
    lines = []

    flexibility = round(instance.num_operations / instance.num_machines, 1)
    lines.append(f"{instance.num_jobs} {instance.num_machines} {flexibility}")

    for operations in instance.jobs:
        line = [len(operations)]

        for processing_data in operations:
            num_eligible = len(processing_data)
            line.append(num_eligible)

            for machine, duration in processing_data:
                # Machine indices are 1-indexed in FJSPLIB.
                line.extend([machine + 1, duration])

        job_data = " ".join(str(num) for num in line)
        lines.append(job_data)

    formatted = "\n".join(lines)

    with open(where, "w") as fh:
        fh.write(formatted)
