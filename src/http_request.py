class HTTPRequest:
    def __init__(self, raw_data):
        self.raw_text = raw_data.decode('utf-8', errors='ignore')

        self.method = ""
        self.path = ""
        self.language_version = ""
        self.headers = {}
        self.body = ""

        self.process_data()

    def process_data(self):
        try:
            if '\r\n\r\n' in self.raw_text:
                header_section, self.body = self.raw_text.split('\r\n\r\n', 1)
            else:
                header_section = self.raw_text
                self.body = ""

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

        except Exception as e:
            print(f"Error: {e}")
    
    def __str__(self):
        return f"<HTTPRequest Method={self.method}, Path={self.path}, Headers={len(self.headers)}>"
