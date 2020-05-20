import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import sys


# ==============================================================================
# noinspection PyPep8Naming
class HTTPHandler(BaseHTTPRequestHandler):
    """
        HTTP Request manager
    """

    # ------------------------------------------------------------------------
    def do_GET(self):
        # --------------------------------------------------------------------
        if self.path == '/':    # return msg working with socket
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!')

        if self.path == '/requestID':   # requests for id
            pass


# ******************************************************************************
class NDServer:
    """
        All server functions and server replies
    """

    # ------------------------------------------------------------------------
    def __init__(self, pid, port):
        # --------------------------------------------------------------------
        self.port = int(port)
        self.pid = pid

    # ------------------------------------------------------------------------
    @staticmethod
    def server_thread_load():
        # --------------------------------------------------------------------
        httpd = HTTPServer(('localhost', 62224), HTTPHandler)
        httpd.serve_forever()

    # ------------------------------------------------------------------------
    def server_start(self):
        # --------------------------------------------------------------------
        Thread(target=self.server_thread_load).start()


# ==============================================================================
class NDClient:
    """
        All requests made
    """

    # ------------------------------------------------------------------------
    def __init__(self):
        # --------------------------------------------------------------------
        self.pid_list = None
        self.port_list = None
        self.read_reg_flag = False

    # ------------------------------------------------------------------------
    def read_registry(self):
        # --------------------------------------------------------------------
        """
        Usage pid_list, port_list = read_reg()
        :return:
        int[]:pid_list, int[]:port_list
        """
        if not self.read_reg_flag:
            registry_filew = open("Registry.txt", "r")
            line = registry_filew.read()
            registry_filew.close()
            broken = line.split(sep=' ')
            broken.pop()
            broken = [xw for xw in broken if xw != '\n']
            left = broken[1::2]
            right = broken[2::2]
            self.pid_list = list(map(int, right))
            self.port_list = list(map(int, left))
            self.read_reg_flag = True
            return self.pid_list, self.port_list
        else:
            return self.pid_list, self.port_list

    # ------------------------------------------------------------------------
    @staticmethod
    def client_thread_load():
        # --------------------------------------------------------------------
        # payload = {'user_name': 'admin', 'password': 'password'}
        r = requests.get('http://localhost:62223/oops')
        print(r.url)
        print(r.text)

    # ------------------------------------------------------------------------
    def client_start(self):
        # --------------------------------------------------------------------
        Thread(target=self.client_thread_load).start()


# ******************************************************************************

# ------------------------------------------------------------------------
def main(argv):
    # --------------------------------------------------------------------
    s = NDServer(sys.argv[1], sys.argv[2])  # arg1 port, arg2 pid
    s.server_start()
    c = NDClient()
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
