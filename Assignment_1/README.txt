# Assignment 1 (Single client and server)

1. Start the server => "python3 server.py"
2. Start the client => "python3 client.py"
3. Connection should be established and ready for file operations

	- Client reads from and stores files in the "/client_files" folder
	- Server reads from and stores files in  the "/server_files" folder

OPERATIONS:
1. Rename a file => "rename file_name.txt new_file_name.txt"
	// Checks "/server_files" folder for the file
2. Delete a file => "delete file_name.txt"
	// Checks "/server_files" folder for the file
3. Upload a file => "upload file_name.txt"
	// Checks "/server_files" folder for the file
4. Download a file => "download file_name.txt"
	// Check "/client_files" folder for the file
