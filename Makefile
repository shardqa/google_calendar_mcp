# Makefile for google_calendar_mcp

# Use .PHONY to ensure these commands run even if files with the same name exist
.PHONY: test test-fast clean

# Define the default command to run when you just type 'make'
default: test

# Full test suite with coverage report
test:
	@echo "Running tests with coverage..."
	@coverage run -m pytest
	@coverage combine
	@coverage report

# A faster test run without coverage
test-fast:
	@echo "Running tests (no coverage)..."
	@pytest

# Clean up temporary Python and coverage files
clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -f .coverage*
	@rm -rf htmlcov/

help:
	@echo "Available commands:"
	@echo "  make test       - Run the full test suite with coverage report"
	@echo "  make test-fast  - Run tests quickly without coverage"
	@echo "  make clean      - Remove temporary files"
	@echo "  make help       - Show this help message" 