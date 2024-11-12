import socket
import sys
import io
import struct

HOST = '127.0.0.1'

if  len(sys.argv) < 2:  
    print("no port given, using 8000")
    port=8000
else:
    port = int( sys.argv[1] )

print("Will send to ", HOST, ":", port)

sizes = [2, 8, 128, 1024, 4096]

def generate_data(size: int) -> bytes:
    if size < 2:
        raise ValueError('argument <size> ')
    binary_stream = io.BytesIO()

    packed = struct.pack('!H', size)

    binary_stream.write(packed)
    for i in range(size - 2):  # 2 bytes taken by size
        shift = i % 26
        character = chr(ord('A') + shift)
        binary_stream.write(character.encode('ascii'))
    binary_stream.seek(0)
    return binary_stream.read()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for size in sizes:
        data = generate_data(size)
        print(f'{len(data)=}, {data[0:2]=}, {size}')
        s.sendto(data, (HOST, port))

        response, address = s.recvfrom(1024)
        print(f'{response=}')