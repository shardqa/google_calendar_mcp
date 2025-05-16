import socket

def check_server_status(host, port, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_sse_url(url=None, ports_to_try=None, host="localhost"):
    if url:
        return url
    if ports_to_try is None:
        ports_to_try = [3001, 3000]
    for port in ports_to_try:
        if check_server_status(host, port):
            print(f"Server detected on port {port}")
            return f"http://{host}:{port}/sse"
    raise RuntimeError("No server detected on common ports") 