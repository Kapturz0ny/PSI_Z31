import socket
import struct
import io

from linked_list import Element, deserialize

# Server configuration
HOST = '127.0.0.1'  # Listen on localhost
PORT = 8000        # Port to listen on

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"Server started on {HOST}:{PORT}")
        server_socket.listen()
        print("Waiting for a connection...")


        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected by {client_address}")

            total_size = 0
            bstream = io.BytesIO()
            try:
                while True:
                    portion = client_socket.recv(1024)
                    if not portion:
                        break
                    bstream.write(portion)
                    total_size += len(portion)
            finally:
                print(f"Closing connection with {client_address}")
                client_socket.close()

            bstream.seek(0)
            print(f'Received {total_size} bytes of data')

            llist = deserialize(bstream)
            llist.print()
            print('Node count: ', llist.size)


if __name__ == "__main__":
    start_server()
