import threading, json
from socket import *
import pyautogui
import sys
from PIL import Image, ImageTk, ImageGrab, ImageChops
import tkinter as tk 
from gui import *
import io

def server():
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 50001
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(1)
    old_img = None
    while True:
        conn, addr = server.accept()
        print('New client has connected' ,addr)
        pictures = []
        HEADERSIZE = 100
        while True:
            full_msg = b''
            new_msg = True
            remaining = None
            while True:
                if len(pictures) == 15:
                    return pictures
                msg = conn.recv(512 * 60)
                if new_msg:ex
                    if remaining:
                        msg = remaining + msg
                    print("new msg len:",msg[:HEADERSIZE])
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False


                full_msg += msg

                if len(full_msg)-HEADERSIZE >= msglen:
                    d = len(full_msg) - HEADERSIZE - msglen
                    if d > 0:
                        msg = full_msg[HEADERSIZE: -1*d]
                        remaining = full_msg[-1*d: ]
                    else:
                        msg = full_msg[HEADERSIZE:]
                    
                    stream = io.BytesIO(msg)
                    pic = Image.open(stream).convert('RGBA')
                    if not old_img:
                        pictures.append(pic)
                    else:
                        new_img = merge_with_difference(old_img, pic)
                        pictures.append(new_img)
                        old_img = new_img
                    new_msg = True
                    full_msg = b""
                    
            

def merge_with_difference(old_img, difference_img):
    r1, g1, b1 = old_img.split()
    r2, g2, b2 = difference_img.split()
    r_new = ImageChops.add_modulo(r2, r1)
    g_new = ImageChops.add_modulo(g2, g1)
    b_new = ImageChops.add_modulo(b2, b1)
    new_img = Image.merge('RGB', (r_new, g_new, b_new))
    return new_img
    
    
if __name__ == '__main__':
    pictures = server()
    for pic in pictures:
        pic.save('%d.jpg' %pictures.index(pic))