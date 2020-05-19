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

def read_reg():
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


def find_master(pid_listw, port_listw, my_pidw, my_portw, num_of_nodes):
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


def main(argv):
    #  port no, pid
    port_no = int(sys.argv[1])

    pid = int(sys.argv[2])
    print("printing PID below:")
    print(pid)

    print("Main() in MyNode.py started..")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), port_no))
    s.listen(5)
    while True:
        #  established
        print("server listening to port " + str(port_no))
        clientsocket, address = s.accept()
        print('Established connection with ' + str(address))
        msg = clientsocket.recv(5)
        msg = msg.decode(encoding='UTF-8', errors='ignore')
        if msg == 'SIG9':
            print("SIG9 received; server exiting..")
            s.close()
            exit()
        if msg == 'SIG3':
            s.close()
            print(" SIG3 received; server stopped; Creating nodes begins shortly")
        print(msg)
    # begin, methods added
    # pid_listing, port_listing = read_reg()


if __name__ == "__main__":
    main(sys.argv)
