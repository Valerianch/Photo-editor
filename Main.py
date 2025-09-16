from PyQt5.QtWidgets import *
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageFilter import *

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700,500)
#виджеты
button1 = QPushButton('Папка')
button2 = QPushButton('Лево')
button3 = QPushButton('Право')
button4 = QPushButton('Зеркало')
button5 = QPushButton('Резкость')
button6 = QPushButton('Ч/Б')

fail_list = QListWidget()

kar = QLabel('Картинка')
#лаяуты
glav_line = QHBoxLayout()
lev_lin = QVBoxLayout()
cent_lin = QVBoxLayout()
niz_lin = QHBoxLayout()
#добавление
lev_lin.addWidget(button1)
lev_lin.addWidget(fail_list)
niz_lin.addWidget(button2)
niz_lin.addWidget(button3)
niz_lin.addWidget(button4)
niz_lin.addWidget(button5)
niz_lin.addWidget(button6)
cent_lin.addWidget(kar,95)
glav_line.addLayout(lev_lin)
glav_line.addLayout(cent_lin,80)
cent_lin.addLayout(niz_lin)

main_win.setLayout(glav_line)

main_win.show()

#Функции
workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    
def filter(files, extensions):
    resul = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                resul.append(filename)
    return(resul)

def showFilenamesList():
    extensions = ['.png', '.jpg', '.jpeg', '.gif']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    fail_list.clear()
    for filename in filenames:
        fail_list.addItem(filename)
#основнй код
button1.clicked.connect(showFilenamesList) 
#класс
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified__1/"
    def loadImage(self, dir, filename):
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        kar.hide()
        pixmapimage = QPixmap(path)
        w,h = kar.width(), kar.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        kar.setPixmap(pixmapimage)
        kar.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        #кнопки
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_up_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_up_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
workimage = ImageProcessor()
#код
def showChosenImage():
    if fail_list.currentRow() >= 0:
        filename = fail_list.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path=os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)
fail_list.currentRowChanged.connect(showChosenImage)
button2.clicked.connect(workimage.do_up_left)
button3.clicked.connect(workimage.do_up_right)
button4.clicked.connect(workimage.do_flip)
button5.clicked.connect(workimage.do_sharpen)
button6.clicked.connect(workimage.do_bw)

app.exec()
