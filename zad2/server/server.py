import socket
import struct
import io

from linked_list import deserialize

HOST = '0.0.0.0'
PORT = 8000

def main():
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

            llist = deserialize(bstream)
            llist.print_limited(10, llist.size - 10)
            print(f'Received {total_size} bytes of data')
            print('Node count: ', llist.size)


if __name__ == "__main__":
    main()
