class HTTPResponse:
    def __init__(self):
        self.status_code = 200
        self.headers = {} 
        self.body = ""

    def set_header(self, key, value):
        self.headers[key] = value

    def set_body(self, data):
        self.body = data

    def send(self, client_socket):
        response_string = f"HTTP/1.1 {self.status_code} OK\r\n"

        for key, value in self.headers.items():
            response_string += f"{key}: {value}\r\n"

        response_string += "\r\n"
        response_string += self.body

        response_bytes = response_string.encode('utf-8')

        try:
            client_socket.sendall(response_bytes)
            print("Successful response")
        
        except Exception as e:
            print(f"Error sending response:{e}")
