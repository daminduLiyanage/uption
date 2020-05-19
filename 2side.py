import os
import datetime
import logging
import getpass
import random
import time
import paramiko
import sys
import socket

sys.stderr = open("/dev/null")
sys.stderr = sys.__stderr__


# ==============================================================================
class SCHandler:
    """ 
    Initiate the network and nodes

    """

    # --------------------------------------------------------------------------
    def __init__(self):
        # ----------------------------------------------------------------------

        self.logger = self.start_logger()
        self.max_nodes = 200
        self.logger.info("Maximum number of nodes are set to " + str(self.max_nodes)
                         + " nodes")
        number_of_nodes = input("How many Processes?\n")
        self.logger.info("User asked for " + number_of_nodes + " processes \n")
        self.number_of_nodes = int(number_of_nodes)
        self.registry_file = self.start_registry()
        self.read_reg_flag = False
        self.pid_reg = None
        self.port_reg = None

        self.port_list = self.generate_port_list()

    # end __init__ method

    # ------------------------------------------------------------------------
    @staticmethod
    def start_logger():
        # --------------------------------------------------------------------
        """
        logging configuration
        :return:
        """
        logging.basicConfig(
            filename="sidecar_log.txt",
            format='%(asctime)s %(message)s',
            filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.info("sideMy.py Initiated...")
        return logger

    # end start_logger method

    # ------------------------------------------------------------------------
    @staticmethod
    def start_registry():
        # --------------------------------------------------------------------
        """
        clear registry
        :return:
        """
        registry_file = open("Registry.txt", mode="w", encoding='utf-8')
        registry_file.write(" ")
        registry_file.close()
        return registry_file

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
            self.pid_reg = list(map(int, right))
            self.port_reg = list(map(int, left))
            self.read_reg_flag = True
            return self.pid_reg, self.port_reg
        else:
            return self.pid_reg, self.port_reg

    # end read_registry method

    # ------------------------------------------------------------------------
    @staticmethod
    def write_registry(pid_assignedw, port_assignedw):
        # --------------------------------------------------------------------
        """
        Creates the registry file with two entries pid and port

        :param port_assignedw:
        :param pid_assignedw:
        :return:
        """
        registry_filev = open("Registry.txt", "a")
        registry_filev.write(
            str(port_assignedw)
            + " "
            + str(pid_assignedw)
            + " \r\n "
        )
        registry_filev.close()

    # ------------------------------------------------------------------------
    @staticmethod
    def generate_ids():
        # --------------------------------------------------------------------
        """
        create node with <id, port> && write registry

        :return: int node_id
        """
        return int(str(time.time() * 1000000)[7:13])

    # ------------------------------------------------------------------------
    def generate_port_list(self):
        # --------------------------------------------------------------------
        """
        Generates a list of ports
        :return: list
        """
        port_list = []
        self.logger.info("generating ports list...\n")
        begin_port_at = 65001
        for i in range(self.number_of_nodes):
            port_list.append(begin_port_at + i)
        self.logger.info(("The port list is :" + str(port_list)) + "\n")
        return port_list

    # ------------------------------------------------------------------------
    def pid_and_port(self):
        # --------------------------------------------------------------------
        """

        :return:
        """
        port_assigned = self.port_list.pop()
        pid_assigned = self.generate_ids()
        return pid_assigned, port_assigned

    # ------------------------------------------------------------------------
    @staticmethod
    def ssh_client():
        # --------------------------------------------------------------------
        """
        Generates a list of ports
        :return: list
        """
        class AllowAllKeys(paramiko.MissingHostKeyPolicy):
            def missing_host_key(self, client, hostname, key):
                return
        hostname = 'localhost'
        username = "dumi"
        # password = getpass.getpass()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.load_system_host_keys()
        client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        client.set_missing_host_key_policy(AllowAllKeys())
        key_file = open("KeyFile.txt", mode="r", encoding='utf-8')
        password = key_file.read()
        key_file.close()
        client.connect(hostname, username=username, password=password)
        channel = client.invoke_shell()
        stdin = channel.makefile("wb")
        stdout = channel.makefile("rb")
        return client, stdout, stdin

    # end ssh_client

    # ------------------------------------------------------------------------
    @staticmethod
    def get_sock_obj(host_addr):
        # --------------------------------------------------------------------
        """
        Generates a list of ports
        :return: list
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), host_addr))
        return s

    # ------------------------------------------------------------------------
    def main_class(self):
        # --------------------------------------------------------------------
        """
        ssh and put to backgrund
        :return:
        """
        for x in range(self.number_of_nodes):
            client, stdout, stdin = self.ssh_client()
            pid_assigned, port_assigned = self.pid_and_port()
            self.write_registry(pid_assigned, port_assigned)
            self.logger.info(pid_assigned)
            tmux_name = x
            stdin.write('''
                tmux new -d -s '''
                        + str(tmux_name)
                        + ''' /Users/dumi/PycharmProjects/untitled1/job.sh '''
                        + str(port_assigned)
                        + ''' '''
                        + str(pid_assigned)
                        + '''
                        ''')
            time.sleep(3)
            stdout.close()
            stdin.close()
            self.logger.info("Executing: $ nohup python MyNode.py &")
            client.close()
            print("SSH Connection closed..")

        # get values from registry

        #  all done send <client:SIG3, 1>
        # for each in range(0, self.number_of_nodes-1):
        #     s = self.get_sock_obj(self.port_list[each])
        #     s.send(b'SIG3')

    # end main_class method

# **********************************************************


def main():
    s = SCHandler()
    s.main_class()


if __name__ == "__main__":
    main()

#  listen <server:masterId, 2> && log

#  listen work <server:range,id, 3>
#  break if <server:SIG9, 4>

# SIG9 Kill
# SIG3 STOP
