import socket
import argparse
import io

from linked_list import deserialize

HOST = "0.0.0.0"
PORT = 8000


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        dest="host",
        help="IP address of host, default 0.0.0.0",
        default=HOST,
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        help="port number, default 8000",
        default=PORT,
    )

    return parser.parse_args()


def main():

    args = get_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((args.host, args.port))
        print(f"Server started on {args.host}:{args.port}")
        server_socket.listen()
        print("Waiting for a connection...")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")
                total_size = 0
                bstream = io.BytesIO()
                while True:
                    portion = client_socket.recv(1024)
                    if not portion:
                        print(f"Closing connection with {client_address}")
                        break
                    bstream.write(portion)
                    total_size += len(portion)
            print(f"Closing connection with {client_address}")
            bstream.seek(0)

            llist = deserialize(bstream)
            llist.print_limited(10, llist.size - 10)
            print(f"Received {total_size} bytes of data")
            print("Node count: ", llist.size)


if __name__ == "__main__":
    main()
