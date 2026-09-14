PYTHON ?= python3

.PHONY: help setup verify audit reproduce figures report clean-generated

help:
	@echo "setup      Create .venv and install the pinned environment"
	@echo "verify     Verify packaged files and recorded result counts"
	@echo "audit      Compile source and run repository verification"
	@echo "reproduce  Run the complete signal-level analysis (requires all inputs)"
	@echo "figures    Regenerate figures from versioned result tables"
	@echo "report     Regenerate the HTML report"

setup:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements-lock.txt

verify:
	$(PYTHON) verify_repository.py
	$(PYTHON) verify_run.py

audit:
	$(PYTHON) -m compileall -q -x '(^|/)(\.venv|venv)/' .
	$(MAKE) verify PYTHON=$(PYTHON)

reproduce:
	$(PYTHON) validate_spectral_fit.py
	$(PYTHON) spectral_controls.py
	$(PYTHON) individual_peak_controls.py
	$(PYTHON) state_controls.py
	$(PYTHON) make_figures.py
	$(PYTHON) build_report.py
	$(PYTHON) verify_run.py

figures:
	$(PYTHON) make_figures.py

report:
	$(PYTHON) build_report.py

clean-generated:
	@echo "Generated results are part of the audit record and are not deleted automatically."

