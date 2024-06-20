> [!NOTE]
> This package is under development. Expect things to break significantly during the v0.0.x phase.


# FJSPLIB
[![PyPI](https://img.shields.io/pypi/v/FJSPLIB?style=flat-square)](https://pypi.org/project/fjsplib/)
[![License](https://img.shields.io/github/license/leonlan/FJSPLIB?style=flat-square&color=blue)](https://github.com/leonlan/FJSPLIB/)
[![CI](https://img.shields.io/github/actions/workflow/status/leonlan/FJSPLIB/.github%2Fworkflows%2FCI.yml?style=flat-square)](https://github.com/leonlan/FJSPLIB/)
[![Codecov](https://img.shields.io/codecov/c/github/leonlan/FJSPLIB?style=flat-square)](https://app.codecov.io/gh/leonlan/FJSPLIB/)

FJSPLIB is a Python package for reading and writing flexible job shop problem (FJSP) instances.

The FJSPLIB format is as follows:

``` sh
<num jobs> <num machines> <average operations per job>
<num operations> * (<num machines> * (<machine idx> <duration>))
...

<OPERATION_PRECEDENCE_SECTION>
<node 1> <node 2>
<node 3> <node 4>
...
```

The first line contains data about the number of jobs, number machines and average number of operations per job.
The following lines each represent the job data, one line for each job.
These lines are each parsed as follows:
- The first number denotes the number of operations for this job.
- Then, for each operation, the first number represents the number of machines that can process this operation, followed by the machine index and processing time for each eligible machine.

The FJSPLIB format is not well-defined for extensions of the FJSP, such as sequence-dependent setup times and arbitrary precedence graphs. One goal of this project is to extend FJSPLIB format to include these and other variants.
