import socket
import os 

from src.http_request import HTTPRequest
from src.http_response import HTTPResponse

template_folder = "frontend_template"

def save_user_to_database(username, password):
    with open("users.txt", "a") as database:
        database.write(f"{username}:{password}\n")
    print(f"Saved user {username} into the database")

def check_login_credentials(username, password):
    if not os.path.exists("users.txt"):
        return False
    
    with open("users.txt", "r") as database:
        for line in database:
            stored_user, stored_pass = line.strip().split(":")
            if username == stored_user and password == stored_pass:
                return True
            
    return False


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

            raw_request = client_socket.recv(4096)
            if not raw_request:
                client_socket.close()
                continue

            request = HTTPRequest(raw_request)

            if request.content_length > len(request.body):
                remaining_bytes = request.content_length - len(request.body)

                while remaining_bytes > 0:
                    chunk = client_socket.recv(min(remaining_bytes, 4096))
                    if not chunk:
                        break

                    request.body += chunk.decode('utf-8', errors='ignore')
                    remaining_bytes -= len(chunk)
            
            print(f"Path: {request.path}")
            print(f"Content-Type: {request.content_type}")
            print(f"Body Size: {len(request.body)} bytes")
            
            #POST REQUESTS
            if request.method == "POST":
                response = HTTPResponse()
                response.set_header("Server", "Server/1.0")

                form_data = request.get_body_parameters()

                if request.path == "/signup":
                    username = form_data.get("username")
                    password = form_data.get("new_password")
                    confirm  = form_data.get("confirm_password")

                    if password == confirm:
                        save_user_to_database(username, password)
                        print(f"Success: {username} registered.")
                        response.set_body(f"Welcome, {username}")
                    else:
                        response.set_body("Passwords do not match")

                elif request.path == "/login":
                    username = form_data.get("username")
                    password = form_data.get("password")

                    if check_login_credentials(username, password):
                        print(f"Successful login: {username}")
                        response.set_body(f"Login Successful, Welcome back {username}")

                    else:
                        print(f"Login Failed: Invalid Credentials fo {username}")
                        response.set_body("Login Failed. Invalid username or password.")
                        
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
                response.set_body("404-Page Missing")

            response.send(client_socket)
            client_socket.close()

if __name__ == "__main__":
    server = Server()
    server.start_server()
