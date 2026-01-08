import socket

class Server:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            print(f"Successfully using address {self.host}, and port {self.port}")

        except Exception as e:
            print(f"Error using connecting to port{self.port}")
            return
        
        self.server_socket.listen(5)
        print("Server listening to client connection")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"The {client_address}, has connected")

            raw_request = client_socket.recv(1024)

            if not raw_request:
                client_socket.close()
                continue

            print(f"The raw request from {client_address}: ")
            print(raw_request.decode('utf-8'))

if __name__ == "__main__":
    server = Server()
    server.start_server()
