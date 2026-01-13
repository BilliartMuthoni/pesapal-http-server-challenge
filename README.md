A WEB SERVER BUILT IN PYTHON USING SOCKETS.

PROJECT DESCRIPTION:
The project is of a server that talks to browser and uses sockets to communicate between two devices. It uses Hypertext Transfer Protocols rules. HTTP/1.1 enables us to request for the HTML and CSS in one connection instead of creating separate connections. The server relies on TCP sockets to provide ordered data transmission.

PROJECT IMPLEMENTATION:
I created a socket that allows the server to send and receive data by instantiating a socket object. The server creates a TCP socket so that data is delivered in order without losing any. It is bound to an IP address (http://127.0.0.1) and a port number (8080). The server listens to any requests made. When a browser goes to http://127.0.0.1:8080, the request is sent to the program.

When a browser connects (type http://127.0.0.1:8080/signup), the browser connects to the server, and the server creates a client_socket. This allows communication between the user's browser and the server.

The server receives raw bytes from the browser. We pass the request to request = HTTPRequest(raw_request) in the HTTPRequest class. It splits the headers and the body to extract the method(GET/POST), path(/signup), headers and body(username and password).

When a browser sends data to the server, the data arrives in chunks. The server reads upto 4096 bytes. If bigger than that, the other data arrives in chunks. The server checks the content-length header to see how big the message should be. The server keeps listening until everything is received.

If the request comes without a content-type header, the server cannot tell the type of data being received. It only accespts the 8192 bytes of data. Anything suspicious or too large might fill up the memory and is truncated.

If it is a post (eg a sign up), the server extracts the username, password, and confirm password. It checks if the passwords match. If so, it saves in the users.txt file. It navigates to the home page. If it is a get request, such as getting the home page, it checks the path being requested (/index), and routes to that page. If page does not exist gives a 404 error.

The server creates a response using response = HTTPResponse(), which builds the reply to the browser with the HTTP version, status code, content type, content length, and the response body. The server sends the response to the browser. The browser reads the headers and checks the content-type and the path and displays the page on the screen. The connection between the browser is closed. The socket is closed after every response, to free the resources be used by other requests.

FEATURES:

1. Handles GET and POST requests.
2. Handles HTML and CSS files.
3. Stires username and password details in users.txt.
4. Handles large requests using content-length.
5. Truncates requests to 8192 bytes.
6. Returns 200 is status is OK, if page not found returns 404.

SETUP AND INSTALLATION:

1. Clone the repository.
2. Using VSCode, have the Microsoft Python extension.
3. Open the terminal and redirect to the pesapal-http-server-challenge (cd pesapal-http-server-challenge)
4. Start the server. Run python -m src.server
5. Open any browser. Type http://127.0.0.1:8080
6. Login or Sign up with the paths. /login and /signup.

LIMITATIONS:
It can have duplicate users yet the same user. As I tested using postman, with long data without username and password and sent it multiple times, it created user None with password None.

The passwords are stored in plaintext and are displayed on the terminal.

REFERENCES:
ByteMonk. (2025, May 10). How Sockets Actually Work [Video]. YouTube. https://www.youtube.com/watch?v=NvZEZ-mZsuI&t=180s

Rivaan Ranawat. (2024, April 9). Build Your Own Web Server from Scratch using Python! [Video]. YouTube. https://www.youtube.com/watch?v=Hncp0mPfUvk
