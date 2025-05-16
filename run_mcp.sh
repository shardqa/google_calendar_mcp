#!/bin/bash
# Script to run the Google Calendar MCP server

# Change to the project directory
cd "$(dirname "$0")"

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

if [ "$TEST_BASIC" = true ]; then
  echo "Running basic server connectivity test"
  python -m src.test_server
elif [ "$TEST_CANCEL" = true ]; then
  echo "Running cancel test - testing cancellation functionality"
  python -m src.test_cancel
elif [ "$TEST_MODE" = true ]; then
  echo "Running in test mode - testing SSE connection"
  python -m src.test_sse_client
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
    python -m src.mcp_cli --port $PORT
  fi
fi 