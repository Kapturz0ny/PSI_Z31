import socket
import io
import struct
import argparse

BUFFER = 1024
HOST = 'localhost'
PORT = 8000
DGRAM_SIZE = 512
DGRAM_NUMBER = 10
TIMEOUT = 1.0


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
        "-n",
        "--number",
        dest="number",
        help="Number of dgrams to be send",
        default=DGRAM_NUMBER,
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


def generate_data(size: int, number: int) -> bytes:
    if size < 3:
        raise ValueError("parameter: size >= 3")

    binary_stream = io.BytesIO()
    packed = struct.pack("!H", size)
    binary_stream.write(packed)

    packed_number = struct.pack("!B", number % 256)
    binary_stream.write(packed_number)

    for i in range(size - 3):  # 2 bytes taken by size, 1 by number
        shift = i % 26
        character = chr(ord("A") + shift)
        binary_stream.write(character.encode("ascii"))
    binary_stream.seek(0)
    return binary_stream.read()


if __name__ == "__main__":

    args = get_args()

    print("Client for zadanie 1.2")
    print("Will send to ", args.host, ":", args.port)
    i = 0
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(TIMEOUT)
        while i < args.number:
            data = generate_data(DGRAM_SIZE, i)
            print(f"sending #{i} dgram of {DGRAM_SIZE=}")

            try:
                s.sendto(data, (args.host, args.port))
            except OSError as err:
                print(err)
                print(f'Could not send dgram of {DGRAM_SIZE=}')
                print(f'Max possible size is {DGRAM_SIZE-1}')
                break

            try:
                response, address = s.recvfrom(BUFFER)
                # success
                print(f"{response=}")
                i += 1
            except socket.timeout:
                print(
                    f"Timeout waiting for response for dgram #{i}. Dgram will be resent...")
            except OSError as err:
                print(f"Error receiving response for dgram #{i}: {err}")