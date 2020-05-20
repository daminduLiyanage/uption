import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from threading import Thread
import sys


class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!')

        if self.path == '/oops':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'reached path')



class SDServer:
    def server_thread(self):
        httpd = HTTPServer(('localhost', 62224), HTTPHandler)
        httpd.serve_forever()

    def server_start(self):
        Thread(target=self.server_thread).start()


class SDClient:

    def client_thread(self):
        payload = {'user_name': 'admin', 'password': 'password'}
        r = requests.get('http://localhost:62223/oops')
        print(r.url)
        print(r.text)

    def client_start(self):
        Thread(target=self.client_thread).start()


# ==============================================================================


def main(argv):
    s = SDServer()
    s.server_start()
    c = SDClient()
    c.client_start()


if __name__ == "__main__":
    main(sys.argv)

    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length'])
    #     body = self.rfile.read(content_length)
    #     self.send_response(200)
    #     self.end_headers()
    #     response = BytesIO()
    #     response.write(b'This is POST request. ')
    #     response.write(b'Received: ')
    #     response.write(body)
    #     self.wfile.write(response.getvalue())
