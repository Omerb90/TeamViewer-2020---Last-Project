import sys
from PyQt4 import QtGui
from PIL.ImageQt import ImageQt

class Gui(QtGui.QWidget):
    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('Test', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # Show  image
        self.pic = QtGui.QLabel(self)
        self.pic.setGeometry(10, 10, 800, 800)
        # Show button 
        #btn = QtGui.QPushButton('Button', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        #btn.move(50, 50)
        self.setGeometry(300, 300, 2000, 1500)
        self.setWindowTitle('TeamViwer')
        self.show()

    # Connect button to image updating 
    def set(self, img):
        qim = ImageQt(img)
        pix = QtGui.QPixmap.fromImage(qim)
        self.pic.setPixmap(QtGui.QPixmap(pix))


    
