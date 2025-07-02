.PHONY: mcp-start mcp-stop mcp-restart mcp-restart-local mcp-local

mcp-start:
	@echo "Starting Google Calendar MCP server..."
	@src/scripts/run_mcp.sh

mcp-stop:
	@echo "Stopping MCP server..."
	@pkill -f "mcp_cli" || echo "No MCP server running"

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