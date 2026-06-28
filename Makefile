PYTHON ?= python3
PYTHONPATH := src

.PHONY: help info cases validate-cases plan demo test compile

help:
	@echo "ReproBench Agent commands"
	@echo "  make info     Show project info"
	@echo "  make cases    List benchmark cases"
	@echo "  make validate-cases"
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

plan:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench plan examples/cases/clean_baseline

demo:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench info
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases list
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench cases validate
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench plan examples/cases/clean_baseline
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m reprobench run examples/cases/clean_baseline

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover -s tests

compile:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m compileall -q src tests
