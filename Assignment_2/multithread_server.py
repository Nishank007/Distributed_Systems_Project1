import socket
import os
import _thread

HOST = '127.0.0.1'          # Use localhost
PORT = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def download(args, conn):     # Responds to the download request from the client
    file_path = 'server_files/' + args[1]
    if os.path.exists(file_path):
        # client acknowlege
        conn.send(b'ok')

        # Start sending file to the client
        print('Downloading...')
        f_path = open(file_path, 'rb')
        data = f_path.read(1024)
        while (data):
            conn.send(data)
            data = f_path.read(1024)
        f_path.close()
        print('Sent!')
    else:
        conn.send(b'download')

def upload(file_path, conn):
    # Receive the uploaded file and save it to the server
    conn.settimeout(0.5)  # Timeout after waiting for a second
    f_path = open(file_path, 'wb')
    while True:
        try:
            data = conn.recv(1024)
        except socket.timeout:
            print('File transferred successfully!')
            break
        else:
            f_path.write(data)
    f_path.close()
    print('Upload successful!')
    conn.settimeout(None)  # Reset timeout

def request_upload(args, conn):
    # Validate upload request from client
    print('Upload request received!')
    file_path = 'server_files/' + args[1]
    if os.path.exists(file_path):
        print('Upload request denied, file already exists!')
        conn.send(b'File with the same name already exists!')
    else:
        conn.send(b'ok')
        # Start waiting for the upload from the client
        upload(file_path, conn)

def rename(args, conn):       # Responds to the client's request to rename a file
    print('Rename request received!')
    file_path = 'server_files/' + args[1]
    if len(args) == 3 and os.path.exists(file_path):
        src = file_path
        dest = 'server_files/' + args[2]
        # Rename the file
        os.rename(src, dest)
        print("File renamed successfully!")
        print("Sending acknowledgment to client!")
        conn.send(b'ok')
    else:
        print("Rename request denied. Error!")
        conn.send(b'File not found in the server!')

def delete(args, conn):
    # Process request from client to delete file_name
    print('Received delete request!')
    if len(args) == 2:
        file_path = 'server_files/' + args[1]
        print('file_path', file_path)
        if os.path.exists(file_path):
            print("Sending acknowledgment to client!")
            conn.send(b'ok')
            # Delete the file
            os.remove(file_path)
            print("File successfully deleted!")
        else:
            print('File not found!')
            conn.send(b'File not found!')
    else:
        print("Delete request denied. Error!")
        conn.send(b'Invalid delete request!')

def main(conn):     # The entry point for the server
    while True:
        request = conn.recv(1024).decode()
        if request:
            args = request.split()
            operation = args[0]
            print('operation', operation)
            if operation == 'delete':
                delete(args, conn)
            elif operation == 'rename':
                rename(args, conn)
            elif operation == 'download':
                download(args, conn)
            elif operation == 'upload':
                request_upload(args, conn)
            else:
                print('Server only supports upload, download, rename & delete.')

        print()
        print()

if __name__ == '__main__':
    while True:
        conn, addr = server.accept()
        print("Connected ", addr)
        server_thread = _thread.start_new_thread(main, (conn,))  # Start thread
    server.close()
