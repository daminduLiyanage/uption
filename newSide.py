from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import socketserver


class SDTalk(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!')

        if self.path == '/oops':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'reached path')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 62223), SDTalk)
httpd.serve_forever()
