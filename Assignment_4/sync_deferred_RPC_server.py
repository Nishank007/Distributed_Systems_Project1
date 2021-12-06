#!/usr/bin/env python3


import socket
import json
import time

HOST = '127.0.0.1'          # Use localhost
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

results = {'result': 'invalid'}  # A dictionary to store the result after it's computed


def matrix_multiply(args, conn):
    if args:
        args_array_str = '[' + args + ']'  # Add extra brackets to make args an array (string) of matrices
        args_array = json.loads(args_array_str)
        if len(args_array) == 3:
            send_ack_to_client(conn)
            do_stuff()  # Keep busy before computing the final result

            matrix_a = args_array[0]
            matrix_b = args_array[1]
            matrix_c = args_array[2]
            _result = _matrix_multiply(matrix_a, matrix_b)
            result = _matrix_multiply(_result, matrix_c)

            result_str = json.dumps(result)

            # Interrupt/send result to client
            conn.send(convert_to_bytes(result_str))
        else:
            err_str = "Expects 3 matrices you provided " + str(len(args_array))
            conn.send(convert_to_bytes(err_str))
    else:
        conn.send(b"Error! Must provide arguments for matrix_multiply")


def sort(args, conn):
    """ Validate upload request from client """
    # Deserialize array
    print('Received a sort request from a client')
    if args:
        array = json.loads(args)
        send_ack_to_client(conn)
        do_stuff()  # keep doing other stuff

        array.sort()

        # Serialize sorted array
        _array = json.dumps(array)

        # Interrupt/send result to client
        conn.send(convert_to_bytes(_array))
    else:
        conn.send(b'Error! Must provide an array to be sorted.')


def add(args, conn):       # Responds to the client's request to rename a file
    print('Received an add request from a client')
    error = 'Error! Must provide two arguments for the add function'  # Default to error message
    if args:
        args_array = args.split(',')
        if len(args_array) == 2:
            send_ack_to_client(conn)
            do_stuff()

            value1 = int(args_array[0].strip())
            value2 = int(args_array[1].strip())
            _result = value1 + value2
            result = str(_result)
            # Interrupt/send result to client
            conn.send(convert_to_bytes(result))
        else:
            conn.send(convert_to_bytes(error))  # Send error message to the client


def calculate_pi(conn):
    """ Process request from client to delete file_name """
    print('Received a calculate_pi() request from a client')
    send_ack_to_client(conn)
    do_stuff()

    print('Now computting the result')
    result = str(_calculate_pi())

    # Interrupt/send result to client
    conn.send(convert_to_bytes(result))
    do_other_stuff()


def query_result(conn):
    print('Received a request to query the previous result')
    result = results['result']
    print('Result', result)

    # Reset the result for the next call and send result
    conn.sendall(convert_to_bytes(result))

    results['result'] = 'invalid'


# Helper methods

# Sends acknowledgement to client, Proceeds to do other stuff before computing the result
def send_ack_to_client(conn):
    print('Sending acknowledgement to the client!')
    conn.send(b'ok')

# Stub for the server doing a bunch of other stuff
def do_stuff():
    sleep_time = 5  # sleep for five seconds
    print('The server is busy doing other stuff')
    for i in range(sleep_time):
        time.sleep(1)  # sleep for five seconds.
        print('The server is busy doing other stuff')

    print('Done doing other stuff, now going back to compute result')


def do_other_stuff():
    print('Doing other stuff after')
    sleep_time = 3
    for i in range(sleep_time):
        time.sleep(1)  # Sleep for a second
        print('Doing other stuff')

# function for calculating value of pi
def _calculate_pi():
    return 3.14159265359

# Creates an num_rows by num_cols matrix initialized with zeros
def create_matrix(num_rows, num_cols):
    result = [ [ 0 for i in range(num_cols) ] for j in range(num_rows) ]
    return result

# Multiplies matrix a and b, returns the resulting matrix
def _matrix_multiply(X, Y):
    result = create_matrix(len(X), len(Y[0]))
    for i in range(len(X)):  # Iterate through each row in a
        for j in range(len(Y[0])):  # Iterate through each column in b
            for k in range(len(Y)):  # Iterate through each row in column b
                result[i][j] += X[i][k] * Y[k][j]
    return result

# Takes request string, returns a tuple of the function and an array of the arguments

def parse_request(request):
    values = request.split('(')  # Split after the opening parenthesis
    if len(values) == 2:
        command = values[0]
        arguments = values[1].split(')')[0]
        return (command, arguments)
    else:
        return ('Invalid', '')  # invalid request

# helper function for converting a string into bytes
def convert_to_bytes(string):
    return bytes(string, encoding="ascii")


# Main section for the server


def main():     # The entry point for the server
    conn, addr = server.accept()
    print("Just accepted a connected from ", addr)
    while True:
        request = conn.recv(1024).decode()
        if request:
            print('Got a request: ', request)

            (command, arguments) = parse_request(request)

            if command == 'add':
                add(arguments, conn)
            elif command == 'sort':
                sort(arguments, conn)
            elif command == 'calculate_pi':
                calculate_pi(conn)
            elif command == 'matrix_multiply':
                matrix_multiply(arguments, conn)
            elif command == 'query_result':
                query_result(conn)
            else:
                conn.send(b'Unsupported operation. Make sure in include opening and closing parens')
                print('Unsupported operation. ')

        print()
        print()
    server.close()


if __name__ == '__main__':
    """ Entry point for the server"""
    main()
