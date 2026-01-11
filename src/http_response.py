class HTTPResponse:
    def __init__(self, status_code=200, status_message="OK"):
        self.status_code = status_code
        self.status_message = status_message
        self.headers = {
            "Content-Type": "text/html",
            "Connection": "close"
        } 
        self.body = b""

    def set_header(self, key, value):
        self.headers[key] = value

    def set_body(self, data):
        #set body and ensure it is on bytes
        if isinstance(data, str):
            self.body = data.encode('utf-8')
        else:
            self.body = data

    def response(self):
        #calculate content length
        self.headers["Content-Length"] = str(len(self.body))

        response_string = f"HTTP/1.1 {self.status_code} {self.status_message}\r\n"

        #headers
        header_section = ""
        for key, value in self.headers.items():
            header_section += f"{key}: {value}\r\n"

        final_response = response_string.encode('utf-8')
        final_response += header_section.encode('utf-8')
        final_response += b"\r\n"  
        final_response += self.body

        return final_response


    def send(self, client_socket):
        try:
            client_socket.sendall(self.response())
            print("Successful response")
        
        except Exception as e:
            print(f"Error sending response:{e}")
