# -*- coding: utf-8 -*-

import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def DealOut(s):
    while True:
        try:
            outString = raw_input()
            s.send(outString)
            print 'send>>'+ outString
        except:
            pass

        
 
def DealIn(s):
    while True:
        try:
            inString = s.recv(1024)
            print 'receive<<' + inString
        except:
            pass




if __name__ == '__main__':

    global outString, flag_sent, inString

    outString =''
    flag_sent = False

#    HOST = raw_input('input the IP:')
#    PORT = raw_input('input the PORT:')
    HOST = '127.0.0.1'
    PORT = 30000
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, int(PORT)))

    print 'have connect!'
    
    thin = threading.Thread(target = DealIn, args = (sock,))
    thin.start()
    thout = threading.Thread(target = DealOut, args = (sock,))
    thout.start()    


