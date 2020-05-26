from http.server import BaseHTTPRequestHandler

# ******************************************************************************
# noinspection PyPep8Naming
class HTTPHandler(BaseHTTPRequestHandler):
    """
        HTTP Request manager for server
    """
    pid = None


    # ------------------------------------------------------------------------
    def do_GET(self):
        # --------------------------------------------------------------------
        if self.path == '/':  # return msg working with socket
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!')

        if self.path == '/requestID':  # send id
            self.send_response(200)
            self.end_headers()
            master_id = self.pid
            self.wfile.write(str(master_id).encode(encoding='UTF-8', errors='ignore'))
