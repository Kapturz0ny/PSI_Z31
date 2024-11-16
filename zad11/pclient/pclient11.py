import socket
import io
import struct
import argparse

BUFFER = 1024
HOST = 'localhost'
PORT = 8000


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        dest="host",
        help="IP address of host, default localhost",
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
    parser.add_argument(
        "sizes",
        nargs="*",
        type=int,
        help="what sizes of datagrams will be transmitted",
        default=[100, 200, 500, 1000]
    )

    return parser.parse_args()


def generate_data(size: int) -> bytes:
    if size < 2:
        raise ValueError("parameter: size >= 2")

    binary_stream = io.BytesIO()
    packed = struct.pack("!H", size)

    binary_stream.write(packed)
    for i in range(size - 2):  # 2 bytes taken by size
        shift = i % 26
        character = chr(ord("A") + shift)
        binary_stream.write(character.encode("ascii"))
    binary_stream.seek(0)
    return binary_stream.read()


if __name__ == "__main__":

    args = get_args()

    print("Python client for zadanie 1.1")
    print("Will send to ", args.host, ":", args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for size in args.sizes:
            data = generate_data(size)
            print(f"sending dgram of {size=}")
            s.sendto(data, (args.host, args.port))

            response, address = s.recvfrom(BUFFER)
            print(f"{response=}")
