import socket
import struct
import argparse

BUFF_SIZE = 2**16
HOST = '0.0.0.0'
PORT = 8000
MAX_SEQ_NUMBER = 256


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


def is_corrupted(data: bytes) -> bool:

    size = len(data)
    if size < 3:
        print("ERROR: datagram too small")
        return False

    declared_size = struct.unpack("!H", data[0:2])[0]
    if size != declared_size:
        # print(
        #     f"ERROR: mismatch between supposed size ({declared_size}) \
        #     and size of received datagram ({size})"
        # )
        return True

    declared_number = int.from_bytes(data[2:3])
    # print(
    #     f"received good datagram of {size = } and sequence number = {declared_number}")
    return False


if __name__ == "__main__":

    args = get_args()

    print("Server for zadanie 1.2")
    print("Will listen on ", args.host, ":", args.port)
    awaited_number = 1

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((args.host, args.port))

        while True:
            data, address = s.recvfrom(BUFF_SIZE)

            received_number = int.from_bytes(data[2:3])

            if is_corrupted(data):
                print("Datagram corrupted.")
                continue
            if received_number == awaited_number:
                print(f"Received datagram  # {received_number}")
                awaited_number = (awaited_number + 1) % MAX_SEQ_NUMBER
            else:
                print(
                    f"Received datagram #{received_number} - datagram may be duplicated or out of order")
                print(f"Awaiting for datagram #{awaited_number}...")

            message = f"ACK #{received_number}"
            response = message.encode("ascii")
            s.sendto(response, address)
