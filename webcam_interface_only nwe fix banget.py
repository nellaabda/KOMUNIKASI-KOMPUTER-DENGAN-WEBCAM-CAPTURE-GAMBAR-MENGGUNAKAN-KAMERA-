# import paket yang diperlukan
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

# Defining CreateWidgets() function to create necessary tkinter widgets
def CreateWidgets():
    root.webcamLabel = Label(root, bg="red", fg="white", text="WEBCAM FEED", font=('Arial',20))
    root.webcamLabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.saveLocationEntry = Entry(root, width=50, textvariable = destPath)
    root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)

    root.browseButton = Button(root, width=10, text="BROWSE", command=destBrowse)
    root.browseButton.grid(row=3, column=2, padx=10, pady=10)

    root.captureButton = Button(root, text="CAPTURE", command = Capture, bg="red", font=('Arial',10), width=20)
    root.captureButton.grid(row=4, column=1, padx=10, pady=10)

    root.cameraButton = Button(root, text="STOP CAMERA", command = StopCAM,  bg="red", font=('Arial',10), width=20)
    root.cameraButton.grid(row=4, column=4)

    root.previewlabel = Label(root, bg="red", fg="white", text="IMAGE PREVIEW", font=('Arial',20))
    root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

    root.imageLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    
    root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)
    
    root.resizeButton = Button(root, text="resize", command = resize,  bg="red", font=('Arial',10), width=20)
    root.resizeButton.grid(row=4, column=6)
    
    root.resizepreview = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    
    root.resizepreview.grid(row=2, column=6, padx=10, pady=10, columnspan=2)
    ShowFeed()

    root.resizelabel = Label(root, bg="red", fg="white", text="RESIZE PREVIEW", font=('Arial',20))
    root.resizelabel.grid(row=1, column=6, padx=10, pady=10, columnspan=2)

# Mendefinisikan fungsi ShowFeed() untuk menampilkan webcam feed pada cameraLabel;
def ShowFeed():
    # Capture frame per frame
    ret, frame = root.cap.read()
    
    if ret:
        # Membuat frame secara vertikal
        frame = cv2.flip(frame, 1)
        
        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
        
        # Mengubah warna frame dari BGR ke RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
        # Membuat memori gambar dari interface array pengekspor frame di atas
        videoImg = Image.fromarray(cv2image)
        
        # Membuat objek kelas PhotoImage() untuk menampilkan frame
        imgtk = ImageTk.PhotoImage(image = videoImg)
        
        # Mengkonfigurasi label untuk menampilkan frame
        root.cameraLabel.configure(image=imgtk)
        
        # Menyimpan Referensi
        root.cameraLabel.imgtk = imgtk
        
        # Memanggil fungsi setelah 10 milidetik
        root.cameraLabel.after(10, ShowFeed)
    else:
        # Mengkonfigurasi label untuk menampilkan frame
        root.cameraLabel.configure(image='')
        
def destBrowse():
    destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
    destPath.set(destDirectory)
    
def Capture():
    global global_path
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')
    
    if destPath.get() != '':
        image_path = destPath.get()
    else:
        image_path = "YOUR DEFAULT DIRECTORY PATH"
    imgName = image_path + '/' + image_name + ".jpg"
    global_path = imgName
    ret, frame = root.cap.read()
    
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    success = cv2.imwrite(imgName, frame)
    
    saved_image = Image.open(imgName)
    
    saved_image = ImageTk.PhotoImage(saved_image)
    
    root.imageLabel.config(image=saved_image)
    
    root.imageLabel.photo = saved_image
    
    if success :
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)
    
def StopCAM():
    root.cap.release()
    root.cameraButton.config(text="START CAMERA", command=StartCAM)
    root.cameraLabel.config(text="CAMERA IS OFF", font=('Arial',15))
    
def StartCAM():
    root.cap = cv2.VideoCapture(0)
    
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)
    root.cameraButton.config(text="STOP CAMERA", command=StopCAM)
    root.cameraLabel.config(text="")
    ShowFeed()
    
def resize():
    src = cv2.imread(global_path, cv2.IMREAD_UNCHANGED)
    #percent by which the image is resized
    scale_percent = 75
    
    #calculate the  percent of original dimensions
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)
    
    # resize
    resize = (width, height)
    
    # resize image
    output = cv2.resize(src, resize)
    
#    root.resizepreview.config(image=output)
    
    imageView = Image.fromarray(output)
    
      # Creating object of PhotoImage() class to display the frame
    imageDisplay = ImageTk.PhotoImage(imageView)

    # Configuring the label to display the frame
    root.resizepreview.config(image=imageDisplay)

    # Keeping a reference
    root.resizepreview.photo = imageDisplay

# Membuat objek pada kelas tk
root = tk.Tk()

# Membuaut objek pada kelas VideoCapture dengan webcam index
root.cap = cv2.VideoCapture(0)

# Mengatur width dan Height
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Mengatur judul, ukuran window, warna background dan menonaktifkan properti pengubah ukuran
root.title("Webcam")
root.geometry("1990x1024")
root.resizable(False, False)
root.configure(background = "darkred")
    
destPath = StringVar()
imagePath = StringVar()

# Panggil fungsi CreateWidgets()
CreateWidgets()


# DMendefinisikan loop tak terbatas untuk menjalankan aplikasi
root.mainloop()
