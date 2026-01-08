import socket
from src.http_request import HTTPRequest

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
            print(f"Error using connecting to port{self.port}. Error: {e}")
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

            request = HTTPRequest(raw_request)

            print(f"The request from {client_address}: ")
            print(f"Method: {request.method}")
            print(f"Path: {request.path}")
            print(f"Language version: {request.language_version}")
            print(f"Headers: {len(request.headers)}")

            response = "HTTP/1.1 200 OK\r\n\r\nSuccessful Connection"
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()


if __name__ == "__main__":
    server = Server()
    server.start_server()
