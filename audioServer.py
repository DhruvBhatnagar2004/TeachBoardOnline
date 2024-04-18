import socket
import pyaudio

# Server-side

# Get the server's IP address
server_ip = input("Enter the server's IP address: ")  # Replace with your server's IP address

# Set up the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, 8000))
server_socket.listen(1)

print(f'Server listening on {server_ip}:8000')

# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

while True:
    print('Waiting for connection...')
    client_socket, addr = server_socket.accept()
    print(f'Got connection from {addr}')

    try:
        while True:
            data = stream.read(1024)
            client_socket.sendall(data)
    except KeyboardInterrupt:
        print('Stopping server...')
        client_socket.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        server_socket.close()
        break