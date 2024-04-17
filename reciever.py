# Receiver side code
import socket
import cv2
import pickle
import struct

# Function to get the local IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# Input the server's IP address
receiver_ip = "192.168.170.247" #input("Enter the server's IP address: ")
port = 9999
socket_address = (receiver_ip, port)

# Create a socket and connect to the server
cln_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cln_sock.connect(socket_address)

data = b""
payload_size = struct.calcsize("Q")

while True:
    try:
        while len(data) < payload_size:
            packet = cln_sock.recv(4 * 1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += cln_sock.recv(4 * 1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Received Video", frame)
        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break
    except struct.error as e:
        print(f"Error: {e}")
        break

cln_sock.close()
cv2.destroyAllWindows()