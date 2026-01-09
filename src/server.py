import socket
import os 

from src.http_request import HTTPRequest
from src.http_response import HTTPResponse

template_folder = "frontend_template"

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

            #POST REQUESTS
            if request.method == "POST":
                response = HTTPResponse()
                response.set_header("Server", "Server/1.0")

                if request.path == "/signup":
                    print(f"SIGNUP DATA: {request.body}")
                    response.set_body("<h1>Registration Successful</h1>")
                elif request.path == "/login":
                    print(f"LOGIN DATA: {request.body}")
                    response.set_body("<h1>Login Successful</h1>")

                response.send(client_socket)
                client_socket.close()
                continue

            # GET REQUESTS
            response = HTTPResponse()
            response.set_header("Server", "Server/1.0")
                        
            if request.path == "/" or request.path == "/index":
                file_path = os.path.join(template_folder, "index.html")
                content_type = "text/html"

            elif request.path == "/login":
                file_path = os.path.join(template_folder, "login.html")
                content_type = "text/html"

            elif request.path == "/signup":
                file_path = os.path.join(template_folder, "signup.html")
                content_type = "text/html"

            else:
                file_path = request.path.lstrip("/")
                if file_path.endswith(".css"):
                    content_type = "text/css"
                elif file_path.endswith(".html"):
                    content_type = "text/html"
                elif file_path.endswith(".png"):
                    content_type = "image/png"
                else:
                    content_type = "text/plain"

            if os.path.exists(file_path):
                with open (file_path, 'rb') as f:
                    content = f.read()
                response.status_code = 200
                response.set_header("Content-Type", content_type)
                response.set_body(content)
                
            else:
                response.status_code = 404
                response.set_body("<h1>404-Template Missing</h1>")

            response.send(client_socket)
            client_socket.close()

if __name__ == "__main__":
    server = Server()
    server.start_server()
