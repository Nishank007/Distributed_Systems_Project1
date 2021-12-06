import socket
import json

HOST = '127.0.0.1'          # Use localhost
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def matrix_multiply(args, conn):
    result_str = ''
    if args:
        args_array_str = '[' + args + ']'  # Add extra brackets to make args an array (string) of matrices
        args_array = json.loads(args_array_str)
        if len(args_array) == 3:
            matrix_a = args_array[0]
            matrix_b = args_array[1]
            matrix_c = args_array[2]
            _result = _matrix_multiply(matrix_a, matrix_b)
            result = _matrix_multiply(_result, matrix_c)
            result_str = json.dumps(result)
        else:
            result_str = '3 matrices to be provided ' + str(len(args_array))
    else:
        result_str = "Error! Must provide arguments for matrix_multiply"
    # Send result to the server
    conn.send(convert_to_bytes(result_str))

def sort(args, conn):
    # Validate upload request from client
    # Deserialize array
    print('Received Sort request!')
    if args:
        array = json.loads(args)
        print('array before sort: ', array)
        array.sort()
        print('array after sort:', array)
        # Serialize sorted array
        _array = json.dumps(array)
        conn.send(convert_to_bytes(_array))
    else:
        conn.send(b'Error! Must provide an array to be sorted.')

def add(args, conn):       # Responds to the client's request to rename a file
    print('Received Add request!')
    result = 'Error! Must provide two arguments for the add function'  # Default to error message
    if args:
        args_array = args.split(',')
        if len(args_array) == 2:
            value1 = int(args_array[0].strip())
            value2 = int(args_array[1].strip())
            _result = value1 + value2
            result = str(_result)
    conn.send(convert_to_bytes(result))

# Function that actually calculates pi
def calculate_pi(conn):
    print('Calculating pi!')
    pi = 3.14159265359
    conn.send(convert_to_bytes(str(pi)))

# Helper methods
def create_matrix(num_rows, num_cols):
    # Creates an num_rows by num_cols matrix initialized with zeros
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

def parse_request(request):
    # Takes request string
    # Returns a tuple of the function and an array of the arguments
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
    print("Connected ", addr)
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
            else:
                conn.send(b'Unsupported Operation. Make sure it includes opening and closing parenthesis')
                print('Unsupported operation!')

        print()
        print()
    server.close()

if __name__ == '__main__':
    # Entry point for the server
    main()
