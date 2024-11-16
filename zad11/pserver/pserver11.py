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
    if size < 2:
        print("ERROR: datagram too small")
        return False
    number = struct.unpack("!H", data[0:2])[0]

    if size != number:
        print(
            f"ERROR: mismatch between supposed size ({number}) \
            and size of received datagram ({size})"
        )
        return False

    print(f"received good datagram of {size=}")
    return True


if __name__ == "__main__":

    args = get_args()

    print("Python server for zadanie 1.1")
    print("Will listen on ", args.host, ":", args.port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((args.host, args.port))
        i = 1
        while True:
            data, address = s.recvfrom(BUFFER)

            size = len(data)
            number = struct.unpack("!H", data[0:2])[0]

            check = validate_data(data)

            check_text = "COR" if check else "ERR"
            response = f"{check_text}_dgram_#{i}".encode("ascii")

            s.sendto(response, address)
            print(f"sending: {response}")
            i += 1
