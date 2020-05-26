from threading import Thread
from http.server import HTTPServer
from HTTPHandler import HTTPHandler


class ConnectWithHTTP:

    def __init__(self, pid):
        self.pid = pid
        # start thread

    # ------------------------------------------------------------------------

    def server_start(self, port):
        # --------------------------------------------------------------------
        Thread(target=self.server_thread_load, args=[port, self.pid]).start()

    # ------------------------------------------------------------------------

    def server_thread_load(self, port, pid):
        # --------------------------------------------------------------------


        HTTPHandler.pid = pid
        httpd = HTTPServer(('localhost', port), HTTPHandler)
        httpd.serve_forever()

