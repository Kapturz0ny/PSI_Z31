import socket
import struct
import argparse

BUFFER = 1 << 16
HOST = '0.0.0.0'
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

    return parser.parse_args()


def validate_data(data: bytes) -> bool:
    size = len(data)
    if size < 3:
        print("ERROR: datagram too small")
        return False
    received_size = struct.unpack("!H", data[0:2])[0]
    received_number = int.from_bytes(data[2:3])

    if size != received_size:
        print(
            f"ERROR: mismatch between supposed size ({received_size}) \
            and size of received datagram ({size})"
        )
        return False

    print(
        f"received good datagram of {size = } and sequence number = {received_number}")
    return True


if __name__ == "__main__":

    args = get_args()

    print("Server for zadanie 1.2")
    print("Will listen on ", args.host, ":", args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((args.host, args.port))
        while True:
            data, address = s.recvfrom(BUFFER)

            number = struct.unpack("!B", data[2:3])[0]

            if validate_data(data):
                text = f"CORRECT datagram #{number}"
            else:
                text = f"INCORRECT datagram #{number}"

            response = text.encode("ascii")

            s.sendto(response, address)
            print(f"sending: {response}")
