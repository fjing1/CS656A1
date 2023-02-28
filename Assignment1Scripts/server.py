import sys
import socket
import os
import errno


# -*- coding: utf-8 -*-

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # tcp connection
        s.bind(('', 0))
        ip_addr, free_port = s.getsockname()  # return (ip address, port)
        # print(free_port)
        return free_port


# get_free_port()
def main():
    # Check command line arguments
    global req_code
    if len(sys.argv) != 3:
        print("check number of argument failed, req_code followed by file_to_send")
        exit(-1)
    # check req_code be int
    try:
        req_code = int(sys.argv[1])
        file_to_send = str(sys.argv[2])
        # print("Error: req_code should be an integer.")
    except ValueError:
        print("Error:<req_code>:int, file_to_send:string")

    file_to_send = sys.argv[2]
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to a specific port
    server_address = ('', 0)
    udp_sock.bind(server_address)

    # Print the port number the server is listening on
    print("stage1 Negotiation using udp, <n_port>:", udp_sock.getsockname()[1])
    # prepare for stage 2
    # Create a TCP/IP socket for A and P
    s_tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        # Wait for a connection
        data, client_address = udp_sock.recvfrom(1024)  # max 1024 bytes
        print("Received data:", data, " from client_address", client_address)
        data = data.decode()
        data = data.split(" ")
        if data[0] == "PORT":
            client_req_code = int(data[2])
            if client_req_code == req_code:
                # register r_port and send 1
                ack = 1
                r_port = int(data[1])
                # print(r_port)
                udp_sock.sendto(str(ack).encode(), client_address)
                # transition stage to r_port of client
                print(client_address[0], r_port)
                s_tcp_sock.connect((client_address[0], r_port))
                # load the file to be sent
                with open(file_to_send, 'rb') as f:
                    file_data = f.read()
                try:
                    # send the file data
                    s_tcp_sock.sendall(file_data)
                finally:
                    # close the connection
                    s_tcp_sock.close()
            else:
                # send 0
                ack = 0
                udp_sock.sendto(str(ack).encode(), client_address)

        elif data[0] == "PASV":
            client_req_code = int(data[1])
            if client_req_code == req_code:
                r_port_server = get_free_port()
                success_message = str(1)+" "+str(r_port_server)
                print("r_port_server", r_port_server)
                s_tcp_sock.bind(('', r_port_server))
                udp_sock.sendto(success_message.encode(), client_address)
                s_tcp_sock.listen(1)
                connectionSocket, addr = s_tcp_sock.accept()
                with open(file_to_send, 'rb') as f:
                    file_data = f.read()
                try:
                    connectionSocket.send(file_data)
                except socket.error as e:
                    if e.errno == errno.EPIPE:  # client has closed the connection
                        print("Client has closed the connection")
                        # handle the error appropriately (e.g., break out of the loop)
                        break
                    elif e.errno == errno.EAGAIN:  # socket buffer is full, retry later
                        print("Socket buffer is full")
                        break
                    else:  # other errors, handle them appropriately
                        print("Error occurred while sending data:", e)
                        # handle the error appropriately (e.g., break out of the loop)
                        break

                finally:
                    s_tcp_sock.close()

            else:
                udp_sock.sendto(str(0).encode(), client_address)

        """
         try:
            if not data:
                print("No data received")
                break
        """
        # client_req_code = int.from_bytes(data, byteorder='big')
        # print("Received request code: client_req_code:", client_req_code)


if __name__ == '__main__':
    main()
