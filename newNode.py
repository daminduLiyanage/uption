import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from threading import Thread

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


def server_thread():
    httpd = HTTPServer(('localhost', 62224), SDTalk)
    httpd.serve_forever()


def client_thread():
    payload = {'user_name': 'admin', 'password': 'password'}
    r = requests.get('http://localhost:62223/oops')
    print(r.url)
    print(r.text)


Thread(target=server_thread()).start()
Thread(target=client_thread).start()

