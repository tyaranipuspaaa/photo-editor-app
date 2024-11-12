#step 1: import semua modules
#upload folder -> os (operation system, ex: windows, macOS, linux, dll)
import os

#install app, widget(halaman, ex: halaman utama, hal transaksi, dll)
#filedialog (mengetahui alamat folder yang di upload),
#label (kalimat yg ada di dalam halaman)
#push button (button yang ditekan)
#list widget (mencatat item2 yang perlu di list dan ditampilkan)
#hboxlayout (layar horizontal)
#vboxlayout (layar vertical)
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)

#install QtCore -> install yang penting2 (contoh yg digunain skrg: Qt.KeepAspectRatio)
#Qt.KeepAspectRatio -> untuk memberikan qualitas foto yang sama setiap kali kita edit
# / ganti ukuran layar
from PyQt5.QtCore import Qt # needs a Qt.KeepAspectRatio constant to resize while maintaining proportions

#QtGUI -> install Graphic User Interface (app / website)
#QPixMap -> mengetahui info mengenai foto tersebut (contoh: width & height)
#knp? karena setiap kali mau edit photo, hasil edit photonya mau ukuran yg sama
from PyQt5.QtGui import QPixmap # screen-optimised

#Image -> open, save photo
from PIL import Image
from PIL.ImageQt import ImageQt # to import the graphics from Pillow to Qt 

#ImageFilter -> edit (puter kiri, puter kanan, black n white, blur, dll)
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

#step 2: buat app & halaman utama
#app
app = QApplication([])

#halaman utama
win = QWidget()       
win.resize(700, 700) 
win.setWindowTitle('Easy Editor')

#label image -> untuk tempat penampungan photo agar bisa di tampilkan
lb_image = QLabel("Image")

#lw_files -> untuk menyimpan list photo2 yang ada di folder yg kita upload
lw_files = QListWidget()

#btn
btn_dir = QPushButton("Folder")
btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
btn_flip = QPushButton("Mirror")
btn_sharp = QPushButton("Sharpness")
btn_bw = QPushButton("B/W")

#step 3: pembuatan layout / desain tempat
#halaman utama -> dibagi menjadi 2 secara horizontal
row = QHBoxLayout()          # Main line

#dibagi menjadi 2 kolom
col1 = QVBoxLayout()         # divided into two columns
col2 = QVBoxLayout()

#kolom 1 hanya berisikan btn upload folder & list photo
col1.addWidget(btn_dir)      # in the first - directory selection button
col1.addWidget(lw_files)     # and file list

#kolom 2 hanya berisikan image & btn2
col2.addWidget(lb_image, 95) # 95% dari layar

#layout btn secara horizontal
row_tools = QHBoxLayout()    # and button bar
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

#masukin layout btn ke dalam kolom 2
col2.addLayout(row_tools)

#set layout c1 dan c2 ke dalam row (layout halaman utama)
row.addLayout(col1, 20) #20% dari layar
row.addLayout(col2, 80) #80% dari layar

#set layout row ke dalam halaman utama
win.setLayout(row)

#tampilin halaman utama
win.show()

#step 4: fungsi untuk folder
workdir = '' #menyimpan alamat folder di file exploler, contoh: 'c:/Users/Tyara/Downloads'

#fungsi untuk filter file2 yang khusus photo doang
def filter(files, extensions):
   result = []
   for filename in files:
       for ext in extensions:
           if filename.endswith(ext):
               result.append(filename)
   return result

#fungsi untuk mengetahui alamat dari folder yg km upload
#contoh: upload folder di downloads
#variable workdir akan berisikan 'c:/Users/Tyara/Downloads'
def chooseWorkdir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()

#filtering dan tampilin hasil file yg udh di filter
def showFilenamesList():
   extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
   chooseWorkdir()
   filenames = filter(os.listdir(workdir), extensions)


   lw_files.clear()
   for filename in filenames:
       lw_files.addItem(filename)

#btn upload akan menjalankan fungsi showfilenameslist
btn_dir.clicked.connect(showFilenamesList)

#step 5: buat kelas
class ImageProcessor():
    #karakteristik
   def __init__(self):
       self.image = None
       self.dir = None #directory -> alamat file / folder contoh: c:/Users/Tyara/Downloads
       self.filename = None #contoh: cars.png
       self.save_dir = "Modified/" #C:\Users\tyara\Downloads\gamelabirin-mario
                                   #\ -> alamat folder
                                   #/ -> buka folder

    #fungsi untuk loading -> open image
   def loadImage(self, filename):
       '''When loading, remember the path and file name'''
       self.filename = filename
       #fullname -> os.path.join (dia mau tau, path yang berisikan workdir(c:/Users/Tyara/Downloads))
       #apakah ada filename tsb atau tidak
       fullname = os.path.join(workdir, filename)
       #kalau ada, maka open the image
       self.image = Image.open(fullname)

    #fungsi u/ simpen image ke dalam sub folder
   def saveImage(self):
       '''saves a copy of the file in a sub-folder'''
       #cari tau, apakah ada path yang berisikan workdir(c:/Users/Tyara/Downloads) dan didalamnya
       #ada folder self.save_dir ('Modified/')
       path = os.path.join(workdir, self.save_dir)
       #jika tidak ada path tersebut (c:/Users/Tyara/Downloads/Modified/)
       if not(os.path.exists(path) or os.path.isdir(path)):
           #bikin folder tersebut dgn path / alamat yg udh di tentuin
           #mkdir -> command / perintah untuk bikin folder
           os.mkdir(path)

        #fullname -> os.path.join (dia mau tau, path yang berisikan workdir(c:/Users/Tyara/Downloads))
        #apakah ada filename tsb atau tidak
       fullname = os.path.join(path, self.filename)

        #baru di save
       self.image.save(fullname)

    #fungsi untuk edit photo
   def do_bw(self): #black n white
       self.image = self.image.convert("L") #filter image
       self.saveImage() #save ke dalam folder modified
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       #tampilin hasil filter image
       self.showImage(image_path)


   def do_left(self):
       self.image = self.image.transpose(Image.ROTATE_90)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


   def do_right(self):
       self.image = self.image.transpose(Image.ROTATE_270)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

    #mirroring
   def do_flip(self):
       self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

    #sharpen -> mempertajam warna
   def do_sharpen(self):
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)

    #fungsi untuk tampilin image
   def showImage(self, path):
       #mengilangkan photo sebelumnya
       lb_image.hide()
       #mengetahui ukuran photo original
       pixmapimage = QPixmap(path)
       #simpen ukuran photo original, ke dalam variable w dan h
       w = lb_image.width()
       h = lb_image.height()
       #set ukuran, kualitas, dll ke dalam photo yg di edit
       pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
       lb_image.setPixmap(pixmapimage)
       #tampilin
       lb_image.show()

#fungsi untuk mengetahui photo mana yg kita klik
def showChosenImage():
    #jika ternyata photo yg di klik itu urutan >=0
    #urutan 1 -> indeks 0
   if lw_files.currentRow() >= 0:
       #cari tau nama file
       filename = lw_files.currentItem().text()
       #open
       workimage.loadImage(filename)
       #show
       workimage.showImage(os.path.join(workdir, workimage.filename))

#step 6: 
workimage = ImageProcessor() #current workimage for work
#kamu buat object sebuah image prosesor

#cara untuk mengetahui perubahan klik
#jika ada row yg di klik itu berubah
#maka harus show photo yg dipilih
lw_files.currentRowChanged.connect(showChosenImage)

#koneksiin semua button dengan fungsi2nya
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)

#jalanin app
app.exec()

