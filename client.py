import socket, io
import pickle
from PIL import ImageGrab, ImageChops, Image
import time
 
def get_difference(img1, img2):
    r1, g1, b1 = img1.split()
    r2, g2, b2 = img2.split()
    r3 = ImageChops.subtract_modulo(r2, r1)
    b3 = ImageChops.subtract_modulo(b2, b1)
    g3 = ImageChops.subtract_modulo(g2, g1)
    img3 = Image.merge('RGB', (r3, g3, b3))
    return img3 
 
HEADERSIZE = 10
SERVER_IP = '127.0.0.1'
SERVER_PORT = 50001
old_img = ImageGrab.grab()
old_img.load()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))
s.setblocking(0)
buf = io.BytesIO()
old_img.save(buf, format='PNG')
msg = buf.getvalue()
msg = bytes('%-100d' % (len(msg),)) + msg
s.sendall(msg)
print len(msg)
print old_img.size
while True:
    new_img = ImageGrab.grab() 
    old_img.load()
    diff_img = get_difference(old_img , new_img) 
    diff_img.save('abc.png')
    buf = io.BytesIO()
    old_img.save(buf, format='PNG')
    msg = buf.getvalue()
    msg = bytes('%-100d' % (len(msg),)) + msg
    print len(msg)
    try:
        s.send(msg)
    except:
        continue
    old_img = new_img

