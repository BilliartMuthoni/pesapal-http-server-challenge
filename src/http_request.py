import urllib.parse

class HTTPRequest:
    def __init__(self, raw_data):
        self.raw_text = raw_data.decode('utf-8', errors='ignore')

        self.method = ""
        self.path = ""
        self.language_version = ""
        self.headers = {}
        self.useragent = ""
        self.content_type = ""
        self.content_length = 0
        self.body = ""

        self.process_data()

    def process_data(self):
        header_section = ""
        self.body = ""

        try:
            if '\r\n\r\n' in self.raw_text:
                header_section, self.body = self.raw_text.split('\r\n\r\n', 1)
            else:
                header_section = self.raw_text

            lines = header_section.split('\r\n')

            if len(lines) > 0 and lines[0]:
                request_line = lines[0]
                parts = request_line.split(' ')

                if len(parts) >= 3:
                    self.method = parts[0]
                    self.path = parts[1]
                    self.language_version = parts[2]
                    
                else:
                    self.method = parts[0] if len(parts) > 0 else ""
                    self.path = parts[1] if len(parts) > 1 else ""

                for line in lines[1:]:
                    if not line.strip():
                        continue

                    if ':' in line:
                        key, value = line.split(':', 1)
                        self.headers[key.strip().lower()] = value.strip()

                #identifying host and user-agent
                self.host = self.headers.get('host', 'Unknown')
                self.useragent = self.headers.get('user-agent', 'Uknown')
                
                #identify content type
                self.content_type = self.headers.get('content-type', '')

                #identify content length
                contentlength_value = self.headers.get('content-length', '0')

                #check if content length is a number and convert into integer
                self.content_length = int(contentlength_value) if contentlength_value.isdigit() else 0

        except Exception as e:
            print(f"Error: {e}")
    
    # to make messy text from the form and make it more readable
    def get_body_parameters(self):
        captured_data = {}

        if not self.body:
            return captured_data
        
        #breaking string 
        form_fields = self.body.split('&')

        for field in form_fields:
            if '=' in field:
                #split key and value
                key, raw_value = field.split('=', 1)

                #clean into understandable text
                clean_value = urllib.parse.unquote_plus(raw_value)
                captured_data[key] = clean_value

        return captured_data  
         
    def __str__(self):
        return f"<HTTPRequest Method={self.method}, Path={self.path}, Headers={len(self.headers)}>"
