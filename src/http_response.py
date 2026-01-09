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
        status_messages = {200: "OK", 404: "Not Found", 403: "Forbidden"}
        msg = status_messages.get(self.status_code, "OK")

        body_bytes = self.body.encode('utf-8') if isinstance(self.body, str) else self.body
        self.set_header("Content-Length", len(body_bytes))

        response_string = f"HTTP/1.1 {self.status_code} {msg}\r\n"

        for key, value in self.headers.items():
            response_string += f"{key}: {value}\r\n"

        response_string += "\r\n"

        final_response = response_string.encode('utf-8') + body_bytes

        try:
            client_socket.sendall(final_response)
            print("Successful response")
        
        except Exception as e:
            print(f"Error sending response:{e}")
