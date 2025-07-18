import json
import threading
from unittest.mock import patch


class MockStdin:
    def __init__(self, input_data):
        self.input_data = input_data
        self.position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.position < len(self.input_data):
            line = self.input_data[self.position]
            self.position += 1
            return line
        raise StopIteration


def run_server_with_timeout(server, timeout=0.2):
    def run_server():
        try:
            server.start()
        except Exception:
            pass
    
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    thread.join(timeout=timeout)


def create_initialize_request(request_id=1):
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "initialize",
        "params": {}
    }


def find_response_by_id(responses, response_id):
    for response_str in responses:
        try:
            response = json.loads(response_str)
            if response.get("id") == response_id and "result" in response:
                return response
        except json.JSONDecodeError:
            continue
    return None 