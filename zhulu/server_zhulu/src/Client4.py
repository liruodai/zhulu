#coding=utf-8

# 虚拟服务器界面
from Tkinter import *
import socket
import threading
from Queue import Queue

class App:


    FORCE_DIC = {'Yan':900, 'Qi':901, 'Qin':902, 'Chu':903}
    FORCE = ('Yan', 'Qi', 'Qin', 'Chu')


    CMD = [ 'NONE',
            'LOGIN',
            'DONE#init',
            'DONE#march',
            'DONE#turn',
            'AUCTION',
            'MARCH',
            'GUARD',
            'BUILD',
            'RECRUIT',
            ]

    def __init__(self, master, host = '127.0.0.1', port = 30000):

        self.host = host
        self.port = port
        # initial the network
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # put data recv from socket
        self.recv_queue = Queue(32)

        # push data into the send_queue
        self.send_queue = Queue(32)


        # draw the GUI
        self.master = master

        self.frm_top = Frame(self.master)
        self.frm_top.pack(side=TOP)

        self.info_group = LabelFrame(self.frm_top, text='info', padx=2, pady=2)

        self.info_group.pack(padx=2, pady=2, side=LEFT)
        Label(self.info_group, text='nick name:', padx=2, pady=2).pack(side=LEFT)

        self.nick_var = StringVar()
        self.nick_var.set('Player4')

        Entry(self.info_group, textvariable=self.nick_var, width=25).pack(padx=5, pady=5, side=LEFT)

        Label(self.info_group, text='force:', padx=2, pady=2).pack(side=LEFT)

        self.force_var = StringVar()

        Entry(self.info_group, textvariable=self.force_var, width=25, state='readonly').pack(padx=5, pady=5, side=LEFT)



        self.frm_middle = Frame(self.master)
        self.frm_middle.pack(side=TOP)

        # the group of cmds
        self.cmd_group = LabelFrame(self.frm_middle, text='cmd', padx=2, pady=2)

        self.cmd_group.pack(padx=2, pady=2, side=LEFT)

        self.radio_var = IntVar()

        Label(self.cmd_group, text='请选择需要发送的指令', padx=2, pady=2).pack()

        self.cmd_radiobtn = [Radiobutton(self.cmd_group, text=cmd, variable=self.radio_var, value=idx) for idx, cmd in enumerate(self.CMD)]

        map(lambda x:x.pack(anchor=W), self.cmd_radiobtn)



        # group the force dst 
        self.log_group = LabelFrame(self.frm_middle, text='log', padx=2, pady=2)

        self.log_group.pack(padx=2, pady=2, side=LEFT)

    
        # the log text widget
        sb = Scrollbar(self.log_group)
        sb.pack(side=RIGHT, fill=Y)

        self.log_text = Text(self.log_group, width=40, height=13, yscrollcommand=sb.set, state='disabled')

        self.log_text.focus_set()

        self.log_text.pack(padx=5, pady=5, side=LEFT, fill=Y) 

        sb.config(command=self.log_text.yview)
        

        self.frm_bottom = Frame(self.master)
        self.frm_bottom.pack(side=BOTTOM)


        # entry and send button
        
        self.edit_send_group = LabelFrame(self.frm_bottom, text='send 发送指令(消息)', padx=2, pady=2)
        self.edit_send_group.pack(padx=2, pady=2)

        Label(self.edit_send_group, text='指令:').pack(side=LEFT, padx=2, pady=2)

        self.cmd_var = StringVar()

        Entry(self.edit_send_group, textvariable=self.cmd_var, width=52).pack(padx=5, pady=5, side=LEFT)

        Button(self.edit_send_group, text='发送', padx=2, pady=2, width=8, command=self.callback).pack( padx=2, pady=2, side=LEFT)

        # self.master.mainloop()
        # print '222'



    # 按下发送按钮时候，获取发送消息，并发送   
    def callback(self):
        # 被选中的按钮
        cmd = self.radio_var.get()
        if cmd == 0:
            msg = self.cmd_var.get()
        elif cmd == 1: # login info
            msg = self.CMD[cmd] + '#' + self.nick_var.get()
            # print msg
        elif 2<=cmd<=4: # three done info
            msg = self.CMD[cmd]
        else: # other info
            msg = self.CMD[cmd] + '#' + self.cmd_var.get()
        
        # 清除输入框的内容，一遍下次更好的输入
        self.cmd_var.set('')
        # 把消息放入队列中
        self.send_queue.put(msg, 1)



    ## 从服务器接收消息，并且放入接收消息队列中
    # @param conn, socket变量
    def recv_data(self, conn):
        while True:
            try:
                raw_data = conn.recv(1024)
                # put message into the queue
                self.recv_queue.put(raw_data, 1)
                # print 'recv_data: ' + msg
            except:
                pass


    ## 从发送队列去取得消息发送
    # @param conn, the socket connection
    def send_data(self, conn):
        while True:
            # try to obtain the message from the queue
            try:
                # obtain message from queue and send them
                data = self.send_queue.get(1)
                # display in the log
                self.log_text.insert(END, 'clt>> '+data+'\n')
                self.log_text.see(END)
                # print data
                try:
                    conn.send(data)
                    # print 'send_data:  ' + data
                except:
                    pass
            except:
                pass


    def run(self):
        # 此进程用来刷新Tk
        threading.Thread(target = self.master.mainloop , args = ()).start()

        self.sock.connect((self.host, self.port))

        # 开启两个收发线程
        threading.Thread(target = self.recv_data , args = (self.sock,)).start()
        threading.Thread(target = self.send_data , args = (self.sock,)).start()


        # # 获得势力号
        # msg = self.recv_queue.get(1)
        # self.force_var.set(msg.split('#')[1].split(',')[0])
        
        flag = False

        while True:
            # obtain the msg from the queue
            msg = self.recv_queue.get(1)
            # 显示来自server的消息
            self.log_text.insert(END, 'srv>> '+msg+'\n')
            self.log_text.see(END)
            if flag:
                pass
            else:
                if 'ALLOC' in msg:
                    self.force_var.set(msg.split('#')[1].split(',')[0])
                    flag = True

        self.sock.close()




if __name__ == '__main__':
    App(Tk()).run()
