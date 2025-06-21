#!/bin/bash
# Script to run the Google Calendar MCP server

# Change to the project root directory
cd "$(dirname "$(dirname "$(dirname "$0")")")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Default port
PORT=3001

# Parse command line arguments
TEST_MODE=false
TEST_CANCEL=false
TEST_BASIC=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --test)
      TEST_MODE=true
      shift
      ;;
    --test-cancel)
      TEST_CANCEL=true
      shift
      ;;
    --test-basic)
      TEST_BASIC=true
      shift
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Function to check if server is already running on port
check_server() {
  nc -z localhost $PORT >/dev/null 2>&1
  return $?
}

# Set any environment variables if needed

# Determine Python executable (prefer venv if available)
PYTHON_CMD=".venv/bin/python3"
echo "Using virtual environment Python: $PYTHON_CMD"

if [ "$TEST_BASIC" = true ]; then
  echo "Running basic server connectivity test"
  PYTHONPATH=. $PYTHON_CMD -m src.test_server
elif [ "$TEST_CANCEL" = true ]; then
  echo "Running cancel test - testing cancellation functionality"
  PYTHONPATH=. $PYTHON_CMD -m src.test_cancel
elif [ "$TEST_MODE" = true ]; then
  echo "Running in test mode - testing SSE connection"
  PYTHONPATH=. $PYTHON_CMD -m src.test_sse_client
else
  # Check if server is already running
  if check_server; then
    echo "A server is already running on port $PORT"
    echo "You can run the tests with:"
    echo "  ./run_mcp.sh --test-basic   # Test basic HTTP connectivity"
    echo "  ./run_mcp.sh --test         # Test SSE connection"
    echo "  ./run_mcp.sh --test-cancel  # Test cancellation"
  else
    # Run the MCP server
    echo "Starting Google Calendar MCP server at http://localhost:$PORT/"
    PYTHONPATH=. $PYTHON_CMD -m src.commands.mcp_cli --port $PORT
  fi
fi 