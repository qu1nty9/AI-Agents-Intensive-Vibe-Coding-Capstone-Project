PYTHON ?= python3
PYTHONPATH := src

.PHONY: help info cases validate-cases audit-cases benchmark-report sample-report dashboard mcp-tools mcp-demo plan demo test compile

help:
	@echo "ReproBench Agent commands"
	@echo "  make info     Show project info"
	@echo "  make cases    List benchmark cases"
	@echo "  make validate-cases"
	@echo "  make audit-cases"
	@echo "  make benchmark-report"
	@echo "  make sample-report"
	@echo "  make dashboard"
	@echo "  make mcp-tools"
	@echo "  make mcp-demo"
	@echo "  make plan     Show the foundation reproduction plan"
	@echo "  make demo     Run the milestone-0 demo flow"
	@echo "  make test     Run unit and integration tests"
	@echo "  make compile  Compile Python sources"

info:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench info

cases:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases list

validate-cases:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases validate

audit-cases:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases audit

benchmark-report:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases audit --output-dir reports/sample/benchmark

sample-report:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench run examples/cases/data_leakage --output-dir reports/sample/data_leakage

dashboard:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench dashboard

mcp-tools:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench mcp list-tools

mcp-demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench mcp call audit_case --args-json '{"case_path":"examples/cases/data_leakage"}'

plan:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench plan examples/cases/clean_baseline

demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench info
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases list
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases validate
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases audit
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases audit --output-dir reports/sample/benchmark
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench dashboard
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench mcp call audit_case --args-json '{"case_path":"examples/cases/data_leakage"}'
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench plan examples/cases/clean_baseline
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench run examples/cases/clean_baseline

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests

compile:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m compileall -q src tests
