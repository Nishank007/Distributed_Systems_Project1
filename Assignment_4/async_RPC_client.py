#!/usr/bin/env python3

import socket
import time

HOST = '127.0.0.1'          # Use localhost
PORT = 5000                 # The server port the client will connect to

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establish initial connection
server.connect((HOST, PORT))


def convert_to_bytes(string):
    """ A helper function for converting a string into bytes """
    return bytes(string, encoding="ascii")


def send_to_server(procedure):
    """ Synchronously send request to the server """
    print('Sending procedure to server')
    procedure_bytes = convert_to_bytes(procedure)
    server.send(procedure_bytes)

    print('Waiting for acknowledgement from the server...')
    ack = server.recv(1024).decode()
    if ack == 'ok':
        print('Received acknowledgement from the server')
        print('Proceeding to do other work, will query for the result later')
        do_stuff()
        query_for_result()
    else:
        print('An error occured: ', ack)


def do_stuff():
    """ A helper function to keep busy until we query for results """
    print('Doing other stuff right now :)')
    sleep_time = 10
    for i in range(sleep_time):
        print('Doing other stuff right now')
        time.sleep(1)


def query_for_result():
    print('Querying the server for the result')
    query = 'query_result()'
    server.send(convert_to_bytes(query))

    # Get response
    response = server.recv(1024).decode()
    if response and response != 'invalid':
        print('Got result from the server')
        print('Result is: ', response)
    else:
        print('Server does not have the result')
        print('Response: ', response)


def main():
    procedure = input()
    if procedure:
        send_to_server(procedure)

        print()
        print()


if __name__ == '__main__':
    while True:
        main()
    server.close()
