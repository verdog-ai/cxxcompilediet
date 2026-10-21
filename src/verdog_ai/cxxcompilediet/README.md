# verdog_ai.cxxcompilediet

## Description

An agent loop that lowers the compile cost of C++ libraries: one change per
round, linted, rebuilt from scratch, tested and kept only if the measured
metric drops by the configured threshold.

## Authors

drexlerd

## Inputs

`Options`: `config`, the path of a `cxxcompilediet.toml`, and `runs`, the
directory of the runs (relative to the configuration file).

## Outputs

`Outcome`: the run directory, its branch, the numbers of kept changes and
attempts, and the path of the patched rules file.
