import socket
import sys

def main():
    # Check if all required command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python3 server.py <req_code> <file_to_send>")
        return

    # Parse command-line arguments
    req_code = int(sys.argv[1])
    file_path = sys.argv[2]

    # Load file contents
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific port on localhost
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    print("Server is listening on port", port)

    # Start listening for incoming connections
    s.listen(1)

    # Wait for a client to connect
    conn, addr = s.accept()
    print('Connection from', addr)

    try:
        # Receive the request code from the client
        req_code_recv = conn.recv(1024)
        if not req_code_recv:
            print("Error: empty request code received")
            return

        req_code_recv = int(req_code_recv.decode())
        if req_code_recv != req_code:
            print("Error: invalid request code received")
            return

        # Send the file contents to the client
        conn.sendall(file_data)
        print("File sent successfully")

    finally:
        # Clean up the connection
        conn.close()

if __name__ == '__main__':
    main()
