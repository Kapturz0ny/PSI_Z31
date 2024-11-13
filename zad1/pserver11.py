import socket
import io
import struct
import argparse

BUFFER = 1 << 16

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", dest='host', help="IP address of host, default localhost", default="127.0.0.1")
    parser.add_argument("-p", "--port", dest='port', type=int, help="port number, default 8000", default=8000)
    
    return parser.parse_args()

def generate_data(size: int) -> bytes:
    if size < 2:
        raise ValueError('parameter: size >= 2')

    binary_stream = io.BytesIO()
    packed = struct.pack('!H', size)

    binary_stream.write(packed)
    for i in range(size - 2):  # 2 bytes taken by size
        shift = i % 26
        character = chr(ord('A') + shift)
        binary_stream.write(character.encode('ascii'))
    binary_stream.seek(0)
    return binary_stream.read()


def validate_data(data: bytes):
    pass


if __name__ == '__main__':

    args = get_args()

    print("Will listen on ", args.host, ":", args.port)


    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((args.host, args.port))
        i=1
        while True:
            data, address = s.recvfrom(BUFFER)

            number = struct.unpack('!H', data[0:2])
            print(f'{number=}, {len(data)=} {data[-5:]}')

            response = f'dgram_#{i}'.encode('ascii')

            s.sendto(response, address)
            print(f'sending: {response}')
            i+=1


