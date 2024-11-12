import socket
import sys
import struct

HOST = '127.0.0.1'
BUFSIZE = 1 << 16

if len(sys.argv) < 2:
  print("no port, using 8000")
  port=8000
else:
  port = int( sys.argv[1] )

print("Will listen on ", HOST, ":", port)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
  s.bind((HOST, port))
  i=1
  while True:
    data, address = s.recvfrom( BUFSIZE )

    number = struct.unpack('!H', data[0:2])
    print(f'{number=}, {len(data)=} {data[-5:]}')

    if not data:
      print("Error in datagram?")  
      break

    response = f'datagram #{i}'.encode('ascii')

    s.sendto(response, address)
    print('sending dgram #', i)
    i+=1


