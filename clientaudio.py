import socket
import pyaudio

# Client-side

# Set the server's IP address
server_ip = input("Enter the server's IP address: ")  # Replace with the server's IP address

# Set up the socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, 8000))

# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True,
                frames_per_buffer=1024)

try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        stream.write(data)
except KeyboardInterrupt:
    print('Stopping client...')
    stream.stop_stream()
    stream.close()
    p.terminate()
    client_socket.close()