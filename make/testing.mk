.PHONY: test test-fast clean

test:
	@echo "Running tests with coverage via uvx..."
	@uvx --with pytest --with coverage --with-editable . coverage run --parallel-mode --source=src -m pytest
	@uvx --with pytest --with coverage --with-editable . coverage combine
	@uvx --with pytest --with coverage --with-editable . coverage report

test-fast:
	@echo "Running tests (no coverage) via uvx..."
	@uvx --with pytest --with-editable . pytest

clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -f .coverage*
	@rm -rf htmlcov/ 