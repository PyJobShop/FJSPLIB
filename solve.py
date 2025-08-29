# /// script
# dependencies = [
#   "ortools",
#   "fjsplib",
# ]
# ///

import argparse
from dataclasses import dataclass
from pathlib import Path

from ortools.sat.python.cp_model import (
    BoolVarT,
    CpModel,
    CpSolver,
    IntervalVar,
    IntVar,
)

from fjsplib import Instance, read

horizon = 2**32


@dataclass
class ModeVar:
    start: IntVar
    duration: IntVar
    end: IntVar
    present: BoolVarT
    interval: IntervalVar


def build(instance: Instance) -> CpModel:
    """
    Builds a CP model from an FJSPLIB instance.
    """
    model = CpModel()

    # Define operation variables.
    op_vars = []
    for _ in range(instance.num_operations):
        start = model.new_int_var(0, horizon, name="")
        duration = model.new_int_var(0, horizon, name="")
        end = model.new_int_var(0, horizon, name="")
        interval = model.new_interval_var(start, duration, end, name="")
        op_vars.append(interval)

    # Define mode variables.
    mode_vars = {}
    op_idx = 0
    for job in instance.jobs:
        for operations in job:
            for machine, duration in operations:
                start = model.new_int_var(0, horizon, name="")
                duration = model.new_constant(duration)
                end = model.new_int_var(0, horizon, name="")
                present = model.new_bool_var(name="")
                interval = model.new_optional_interval_var(
                    start, duration, end, present, name=""
                )
                var = ModeVar(start, duration, end, present, interval)
                mode_vars[op_idx, machine + 1] = var

            op_idx += 1

    # Select one mode and synchronize
    for operation in range(instance.num_operations):
        selected = []

        for machine in range(instance.num_machines):
            if (operation, machine) in mode_vars:
                op_var = op_vars[operation]
                mode_var = mode_vars[operation, machine]
                selected.append(mode_var.present)

                expr = op_var.start_expr() == mode_var.start
                model.add(expr)

                expr = op_var.end_expr() == mode_var.end
                model.add(expr)

                expr = op_var.size_expr() == mode_var.duration
                model.add(expr).only_enforce_if(mode_var.present)

        model.add_exactly_one(selected)

    # Define no overlap.
    for machine in range(instance.num_machines):
        intervals = [
            mode_vars[operation, machine].interval
            for operation in range(instance.num_operations)
            if (operation, machine) in mode_vars
        ]
        model.add_no_overlap(intervals)

    # Define precedence constraints.
    for pred, succ in instance.precedences:
        end = op_vars[pred].end_expr()
        start = op_vars[succ].start_expr()
        model.add(end <= start)

    makespan = model.new_int_var(0, horizon, name="")
    ends = [var.end_expr() for var in op_vars]
    model.add_max_equality(makespan, ends)
    model.minimize(makespan)

    return model


def solve(model: CpModel, time_limit: int, display: bool, num_workers: int):
    """
    Solves the CP model with a time limit.
    """
    solver = CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.log_search_progress = display
    solver.parameters.num_workers = num_workers

    return solver.Solve(model)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("instance", type=Path)
    parser.add_argument("--time_limit", type=int, default=60)
    parser.add_argument("--display", action="store_true")
    parser.add_argument("--num_workers", type=int, default=0)  # all cores

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    instance = read(args.instance)
    model = build(instance)
    reuslt = solve(model, args.time_limit, args.display, args.num_workers)
