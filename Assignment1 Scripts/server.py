import socket


HOST = 'localhost'
PORT = 12000  #port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    print(s)
    s.listen()

    print(f'Server listening on{HOST}:{PORT}')
    while True:
        #accept a new client connection
        conn, addr = s.accept()

        with conn:
            print(f'Connected by {addr}')

            while True:
                #received Data
                data = conn.recv(1024)

                if not data:
                    break

                result = data.decode().upper()

                conn.sendall(result.encode())
            print(f'Connection with {addr} closed')