CS656A1 README
Introduction
This project is a client-server application developed using Python 3. It includes modified server and client shell scripts, as well as the source code for the server and client applications.

Requirements
In order to run this program, you must first connect to the student server via SSH using the following command in the terminal:

ssh  <student id>@ubuntu2004-002.student.cs.uwaterloo.ca 
You will also need to have Python 3 installed on the Linux server, currently it is 3.8.10
Usage

Running the Server

To start the server, navigate to the directory where the server files are located and run the following commands in the terminal:
chmod +x server.sh
./server.sh <REQ_CODE> "file_to_sent.txt"

Server should be up and running now and printing:
stage1 Negotiation using udp, <n_port>: 

Running the Client
To start the client, navigate to the directory where the client files are located and run the following commands in the terminal:

ssh  <student id>@ubuntu2004-004.student.cs.uwaterloo.ca (or any other student server)
chmod +x client.sh

./client.sh <server address> <n_port> <mode> <req_code>'received.txt'

This will set up the client and save the received content into 'received.txt' locally.

Contact
Any questions or feedback, please feel free to contact me at f2jing@uwaterloo.ca
