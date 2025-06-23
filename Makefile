# Makefile for google_calendar_mcp

# Use .PHONY to ensure these commands run even if files with the same name exist
.PHONY: test test-fast clean mcp-start mcp-stop mcp-restart mcp-restart-local mcp-local

# Define the default command to run when you just type 'make'
default: test

# Full test suite with coverage report
test:
	@echo "Running tests with coverage..."
	@.venv/bin/python -m coverage run -m pytest
	@.venv/bin/python -m coverage combine
	@.venv/bin/python -m coverage report

# A faster test run without coverage
test-fast:
	@echo "Running tests (no coverage)..."
	@.venv/bin/pytest

# Clean up temporary Python and coverage files
clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -f .coverage*
	@rm -rf htmlcov/

# MCP Server Management
mcp-start:
	@echo "Starting Google Calendar MCP server..."
	@src/scripts/run_mcp.sh

mcp-stop:
	@echo "Stopping MCP server..."
	@pkill -f "mcp_cli" || echo "No MCP server running"
	@pkill -f "mcp_server.py" || echo "No local MCP server running"

mcp-restart: mcp-stop
	@sleep 2
	@echo "Restarting MCP server..."
	@src/scripts/run_mcp.sh

mcp-restart-local: mcp-stop
	@sleep 2
	@echo "Restarting local MCP server on port 3001..."
	@src/scripts/run_mcp.sh --port 3001

mcp-local:
	@echo "Starting Google Calendar MCP server locally on port 3001..."
	@chmod +x src/scripts/run_mcp.sh
	@src/scripts/run_mcp.sh --port 3001

help:
	@echo "Available commands:"
	@echo "  make test       - Run the full test suite with coverage report"
	@echo "  make test-fast  - Run tests quickly without coverage"
	@echo "  make clean      - Remove temporary files"
	@echo "  make mcp-start  - Start the Google Calendar MCP server"
	@echo "  make mcp-local  - Start the MCP server locally on port 3001"
	@echo "  make mcp-stop   - Stop the MCP server"
	@echo "  make mcp-restart - Restart the MCP server"
	@echo "  make mcp-restart-local - Restart the local MCP server on port 3001"
	@echo "  make help       - Show this help message" 