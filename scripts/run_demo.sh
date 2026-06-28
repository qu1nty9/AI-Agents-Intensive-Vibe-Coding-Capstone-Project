#!/usr/bin/env sh
set -eu

PYTHONPATH=src python3 -m reprobench info
PYTHONPATH=src python3 -m reprobench plan examples/cases/clean_baseline
PYTHONPATH=src python3 -m reprobench run examples/cases/clean_baseline

