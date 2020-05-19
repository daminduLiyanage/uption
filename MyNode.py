import socket
import time
import logging
import os
import sys


#  save to registry file

#  listen <server:SIG3, 1> begin 


#  0. 
#  read & save registry
#  run bully
#  mark registry file

#  -- master
#  1. 
#  send to all <client:masterId, 2>

#  2. 
#  Read password file save to list
#  Divide work
#  send work <client: range, 3>

#  finish <client:SIG9, 4>

#  -- slave

#  1.
#  receive <server:masterId, 2>
#  get work <server:range, 3>

# ==============================================================================
class NDHandler:
    """
    Phase I server. Initiate node. Terminate when SIG received.
    """

    # ------------------------------------------------------------------------
    def __init__(self, port, pid):
        # --------------------------------------------------------------------
        self.port = int(port)
        self.pid = pid
        print("printing PID below:")
        print(self.pid)
        self.pid = int(pid)

    # ------------------------------------------------------------------------
    def read_reg(self):
        # --------------------------------------------------------------------
        """
        Reads the registry created by write_reg
        Note: It pops the last element. Use only once.
        :return:
        int:pid_list
        int:port_list
        Usage pid_list, port_list = read_reg()
        """
        registry_filew = open("Registry.txt", "r")
        line = registry_filew.read()
        registry_filew.close()
        broken = line.split(sep=' ')
        broken.pop()
        broken = [xw for xw in broken if xw != '\n']
        left = broken[1::2]
        right = broken[2::2]
        return list(map(int, right)), list(map(int, left))

    # ------------------------------------------------------------------------
    def find_master(self, pid_listw, port_listw, my_pidw, my_portw, num_of_nodes):
        # --------------------------------------------------------------------
        """
        Bully Algorithm to find master. Place in MyNode.py
        Obtains the pid list using two ways: using registry, using nodes
        :param pid_listw:
        :return:
        """
        # Assume master
        master_pidw = max(pid_listw)
        master_portw = port_listw[pid_listw.index(master_pidw)]
        # Assumed master receive pid from others
        flag = 1
        if my_pidw == master_pidw:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((socket.gethostname(), my_portw))
            s.listen(50)
            for _ in range(num_of_nodes):
                c, a = s.accept()
                m = c.recv(10)
                m = m.decode(encoding='UTF-8', errors='ignore')
                m = int(m)
                if m > master_pidw:
                    flag = 0
        # slaves send pid to master with TCP
        if my_pidw != master_pidw:
            time.sleep(1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((socket.gethostname(), master_portw))
            s.send(my_pidw)
        # check if masterw == received master are the same

        # if confirmed return master
        if flag == 0:
            return -1
        else:
            return master_pidw

    # ------------------------------------------------------------------------
    @staticmethod
    def server_sock_obj(port_no, max_clients=5):
        # --------------------------------------------------------------------
        """
        Create server socket. Bind. Listen.
        Returns server socket.
        :return:
        socket server_sock
        """
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((socket.gethostname(), port_no))
        server_sock.listen(max_clients)
        print("Node Init server listening on port: " + str(port_no))
        return server_sock

    # ------------------------------------------------------------------------
    @staticmethod
    def client_sock_obj(server_sock):
        # --------------------------------------------------------------------
        """
        Accept incoming.
        Returns client info.
        :return:
        socket client_sock, str client_ip, int client_port
        """
        client_sock, client_address = server_sock.accept()
        print('Node Init server established a connection with client: ' + str(client_address))
        client_ip = client_address[0]  # type str
        client_port = client_address[1]  # type int
        return client_sock, client_ip, client_port

    # ------------------------------------------------------------------------
    def get_client_msg(self, client_sock):
        # --------------------------------------------------------------------
        """
        Decode message. Return.
        :param client_sock:
        :return: string msg
        """
        msg = client_sock.recv(5)
        msg = msg.decode(encoding='UTF-8', errors='ignore')
        return msg

    # ------------------------------------------------------------------------
    def check_msg_action(self, msg, server_sock):
        # --------------------------------------------------------------------
        """
        For SIG only. Performs action
        :param server_sock:
        :param msg:
        :return: int action -1 for exit()
        """
        if msg == 'SIG9':
            action = -1
            print("SIG9 received; server exiting..")
            server_sock.close()
            exit()
        if msg == 'SIG3':
            print(" SIG3 received; server stopped; Begin next phase")
            action = 0
        print(msg)
        return action

    # ------------------------------------------------------------------------
    def main_method(self):
        # --------------------------------------------------------------------
        """
        Create server socket. Listen. Exit when SIG received.
        :return:
        """
        server_sock = self.server_sock_obj(self.port)
        action = 1
        while action:
            #  established
            client_sock, _, _ = self.client_sock_obj(server_sock)
            msg = self.get_client_msg(client_sock)
            action = self.check_msg_action(msg, server_sock)
        server_sock.close()

        # test
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), self.port))
        s.accept()
        s.close()


# **********************************************************

class NDTalk:
    """
    Class stays on chatting.
    """

    # ------------------------------------------------------------------------
    def __init__(self):
        # --------------------------------------------------------------------
        pass

    # ------------------------------------------------------------------------
    @staticmethod
    def server_sock_obj(port_no):
        # --------------------------------------------------------------------
        """
                Create server socket. Bind. Listen. Accept client.
                Returns server socket, client info.
                :return:
                socket server_sock, socket client_sock, str client_ip, int client_port
        """
        return NDHandler.server_sock_obj(port_no=port_no)

    # ------------------------------------------------------------------------
    def main_method(self):
        # --------------------------------------------------------------------
        action = 1



# ==============================================================================


def main(argv):
    # Get arguments from call. Start node server
    n = NDHandler(sys.argv[1], sys.argv[2])  # arg1 port, arg2 pid
    n.main_method()

    # starting chat phase
    print("Node Talk begins...")
    exit()


if __name__ == "__main__":
    main(sys.argv)
