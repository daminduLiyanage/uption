import requests
from threading import Thread
import sys
import time
from conn import ConnectWithHTTP


# ******************************************************************************
class NDTalk:
    """
        All server functions and server replies
    """
    master_id = None

    # ------------------------------------------------------------------------
    def __init__(self, port, pid):
        # --------------------------------------------------------------------
        self.port = int(port)
        self.pid = pid
        self.pid_list = None
        self.port_list = None
        self.read_reg_flag = False
        self.server1 = ConnectWithHTTP(self.pid)

    # ------------------------------------------------------------------------

    def main_class_server(self, port):
        self.server1.server_start(port)

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
    def client_example():
        # --------------------------------------------------------------------
        try:
            # payload = {'user_name': 'admin', 'password': 'password'}
            r = requests.get('http://localhost:62223/oops')
            print(r.url)
            print(r.text)
        except Exception as e:
            print("**Failed client_example method**\n")
            print(e)

    # ------------------------------------------------------------------------
    @staticmethod
    def ask_node_id(port):
        # --------------------------------------------------------------------
        url = 'http:/localhost:' + str(port) + "/requestID"
        r = requests.get(url)
        print(r.text)
        pid = int(r.text)
        return pid

    # ------------------------------------------------------------------------
    def bully(self, port_list):
        # --------------------------------------------------------------------
        self.master_id = self.pid

        max_id = self.master_id
        while True:
            time.sleep(20)
            for each_port in port_list:
                pid = self.ask_node_id(each_port)
                if self.master_id > pid:
                    max_id = pid
            if self.pid > max_id:
                max_id = self.pid
            self.master_id = max_id

    # ------------------------------------------------------------------------
    def main_class_client(self):
        # --------------------------------------------------------------------
        Thread(target=self.client_example).start()  # some e.g.


# end NDTalk class


# ******************************************************************************
# ------------------------------------------------------------------------
def main(argv):
    # --------------------------------------------------------------------

    s = NDTalk(sys.argv[1], sys.argv[2])  # arg1 port, arg2 pid
    s.main_class_server(s.port)
   #  s.main_class_client()


if __name__ == "__main__":
    main(sys.argv)

# end main method

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
