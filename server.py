import threading, pickle
from socket import *
import pyautogui
import sys
from PIL import Image, ImageTk 
import tkinter as tk 
from gui import *


 
class ClientHandle(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.gui = Gui()
   
    def run(self):
        pictures = []
        HEADERSIZE = 100
        while True:
            full_msg = b''
            new_msg = True
            remaining = None
            while True:
                msg = self.conn.recv(512 * 60)
                if new_msg:
                    if remaining:
                        msg = remaining + msg
                    print("new msg len:",msg[:HEADERSIZE])
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False
 
                #print("msglen: %d"%msglen)
 
                full_msg += msg
 
               # print(len(full_msg))
 
                if len(full_msg)-HEADERSIZE >= msglen:
                    d = len(full_msg) - HEADERSIZE - msglen
                    if d>0:
                        msg = full_msg[HEADERSIZE:-1*d]
                        remaining = full_msg[-1*d:]
                    else:
                        msg = full_msg[HEADERSIZE:]
                    
                    pic = pickle.loads(msg)
                    print pic
                   # tkimage = ImageTk.PhotoImage(pic)
                   # tk.Label(self.root, image=tkimage).pack()
                    self.gui.set(pic)
                    pictures.append(pic)
                    new_msg = True
                    full_msg = b""
                    
                    if len(pictures) == 10:
                        self.conn.close()
                    
 
           
 
 
 
def main(ip, port):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)
    while True:
        conn, addr = server.accept()
        print('New client has connected' ,addr)
        c = ClientHandle(conn, addr)
        c.start()
        
        
 
if __name__ == "__main__":
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 50001
    app = QtGui.QApplication(sys.argv)
    main(SERVER_IP, SERVER_PORT)
    sys.exit(app.exec_())