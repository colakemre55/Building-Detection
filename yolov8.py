import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from ultralytics import YOLO
import shutil
#Murat Emre Çolak
#150180061
#

def frameAndLabel(text, width, height, frameRow, frameCol, labelRow, labelCol, font):
    frame = Frame(master=window, relief="groove", borderwidth=0, width=width, height=height, highlightbackground="green",highlightthickness = 5 )
    frame.grid(row=frameRow,column=frameCol, padx=(50,10))
    label = tk.Label(text=text, width=30, font=font, bg="#f4f6f3")
    label.grid(row=labelRow, column=labelCol)

def label(text, font, row, column):
    label = tk.Label(text=text, width=30, font=font, bg="#f4f6f3")
    label.grid(row=row, column=column, sticky="nsew", columnspan=3)

def imageShow(img, savedFile, size, row, col):
    img=Image.open(img) 
    img.save(savedFile)
    img=img.resize((size,size))
    img=ImageTk.PhotoImage(img)
    imageLabel =tk.Label(master=window, image=img)
    imageLabel.image = img
    imageLabel.grid(row=row,column=col, padx=(50,10))

def fileUpload():
    f_types = [ ('jpg files', '*.jpg') ,('png files','*.png')]   
    filename = tk.filedialog.askopenfilename(filetypes=f_types)
    imageShow(filename, "oriImg.png", 350, 1, 0)
    imageShow("blank.png", "blank.png", 350, 1, 2)

def buildingDetection():
    global buildingCount
    model = YOLO('best.pt')
    results = model(source="oriImg.png", save=True, conf=0.40, boxes=True)
    '''building_boxes = [box for box in results[0].boxes if box.get('name') == "building"]
    buildingNo = len(building_boxes)'''
    buildingCount = len(results[0].boxes)
    predImg = "runs/segment/predict/oriImg.png"
    imageShow(predImg, "predImg.png", 350, 1, 2)
    shutil.rmtree("runs/segment/predict")


window = tk.Tk()
window.title("Building Detection")
window.geometry("1280x720")  # Window size
window.iconbitmap("assets/satellite.ico")
window.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
window.columnconfigure([0, 1, 2, 3], minsize=50, weight=1)
window['background'] = "#F2F2F2"

buildingCount = 0
labelFont=('times', 16, 'bold')
captionFont=('times', 12, 'bold')

label("Choose satellite image", labelFont, 0, 0)
frameAndLabel("Original image", 500, 500, 1, 0, 2, 0, captionFont)

uploadButton = tk.Button(master=window, text="Upload Image", command=fileUpload)
uploadButton.grid(row=0, column=1, columnspan=2)

startImg = Image.open("assets/play.png")
startImg = startImg.resize((80,80))
startImg = ImageTk.PhotoImage(startImg)
startLabel = tk.Label(image=startImg)
algoButton = tk.Button(master=window, image=startImg, borderwidth=0, command=buildingDetection)
algoButton.grid(row=1, column=1)

frameAndLabel("Detected Buildings", 500, 500, 1, 2, 2, 2, captionFont)


window.mainloop()
