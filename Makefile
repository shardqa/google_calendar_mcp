default: test

include make/testing.mk
include make/analysis-files.mk
include make/analysis-dirs.mk
include make/mcp.mk

help:
	@echo "Available commands:"
	@echo "  make test       - Run the full test suite with coverage report"
	@echo "  make test-fast  - Run tests quickly without coverage"
	@echo "  make clean      - Remove temporary files"
	@echo "  make check-file-sizes - Analyze files with more than 100 lines"
	@echo "  make check-file-sizes-summary - Quick summary of large files"
	@echo "  make check-directory-sizes - Analyze directories with more than 10 items"
	@echo "  make check-directory-sizes-clean - Analyze directories (exclude __pycache__)"
	@echo "  make check-directory-sizes-summary - Quick summary of large directories"
	@echo "  make count-items - Complete item count for all directories"
	@echo "  make count-items-quick - Quick overview with emojis"
	@echo "  make mcp-start  - Start the Google Calendar MCP server"
	@echo "  make mcp-local  - Start the MCP server locally on port 3001"
	@echo "  make mcp-stop   - Stop the MCP server"
	@echo "  make mcp-restart - Restart the MCP server"
	@echo "  make mcp-restart-local - Restart the local MCP server on port 3001"
	@echo "  make help       - Show this help message" 

.PHONY: help 

auth:
	@echo "Starting Google OAuth flow to refresh credentials..."
	python3 -c 'from src.core.auth import get_credentials; get_credentials()'
	@echo "If successful, your credentials have been refreshed." 