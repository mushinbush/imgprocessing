#!/usr/bin/env python3

import numpy as np
import cv2
import imghdr
from tkinter import filedialog
from tkinter import Tk, messagebox, ttk, Label
from PIL import Image, ImageTk

initpath = 'image'
#image resize
maxwidth, maxheight = 540, 540

class ImageProcessingGUI:
    def __init__(self, master):
    
        self.master = master
        master.title("AIP61075013H")
        master.geometry('1280x720')
        master.configure(background='white')
        self.im = ''
        
        #choose button
        self.choose_button = ttk.Button(master, text="檔案", command=self.imgselect)
        self.choose_button.place(x=40,y=40)

        #close button
        self.close_button = ttk.Button(master, text="關閉", command=self.closeapp)
        self.close_button.place(x=135,y=40)

        #choose homework
        hw = ['hw1','hw2','hw3','hw4','hw5','hw6']
        self.combobox = ttk.Combobox(master, values = hw, state="readonly", width = 10)
        self.combobox.current(0)
        self.combobox.place(x=960,y=42)

        #process button
        self.hw6_button = ttk.Button(master, text="處理", command=self.run)
        self.hw6_button.place(x=1060,y=40)

        #save image
        self.save_button = ttk.Button(master, text="儲存為..", command=self.savefile)
        self.save_button.place(x=1155,y=40)

        #photo info
        self.imginfo = Label(master, text="", bg="white")
        self.imginfo.place(x=235,y=43)

        #display image
        self.rawimg = Label(master, image="", bg="white")
        self.rawimg.place(x=60,y=110)

        #show processed image
        self.proimg = Label(master, image="", bg="white")
        self.proimg.place(x=670,y=110)

    def imgselect(self):
        global initpath
        #open image as jpg(RGB)
        initpath = filedialog.askopenfilename()
        img = cv2.imdecode(np.fromfile(initpath,dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        dim = img.shape
        #resize image
        f1 = maxwidth / img.shape[1]
        f2 = maxheight / img.shape[0]
        f = min(f1, f2)  # resizing factor
        fdim = (int(img.shape[1] * f), int(img.shape[0] * f))
        reimg = cv2.resize(img, fdim)
        im = Image.fromarray(reimg)
        #display image
        photo = ImageTk.PhotoImage(im)
        self.rawimg.configure(image=photo)
        self.rawimg.image = photo
        self.imginfo.configure(
            text="解析度："+str(img.shape[1])+"x"+str(img.shape[0])
            +"      檔案格式："+str(imghdr.what(initpath)))

    def savefile(self):
        files = [('JPEG Files', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
        ('PNG Files', '*.png'),
        ('BMP Files', ('*.bmp', '*jdib'))]
        #check if image is processed
        if self.im == '':
            MsgBox = messagebox.showinfo(title='Warning', message='請先進行影像處理！')
            return
        filename = filedialog.asksaveasfile(mode='wb+', filetypes = files, defaultextension = files)
        if not filename:
            return
        self.im.save(filename)

    def closeapp(self):
        MsgBox = messagebox.askquestion(title='Information', message='確定要關閉嗎？')
        if MsgBox == 'yes':
            root.destroy()

    def run(self):
        #run homework choosed from combobox
        functions = {
            'hw1': self.hw1,
            'hw2': self.hw2,
            'hw3': self.hw3,
            'hw4': self.hw4,
            'hw5': self.hw5,
            'hw6': self.hw6
        }
        processhomework = functions[self.combobox.get()]()
    
    def showresult(self):
        #resize image
        f1 = maxwidth / self.pimg.shape[1]
        f2 = maxheight / self.pimg.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(self.pimg.shape[1] * f), int(self.pimg.shape[0] * f))
        img = self.pimg
        reimg = cv2.resize(img, dim)
        #save as Tk.image
        self.im = Image.fromarray(img)
        self.reim = Image.fromarray(reimg)
        #Tk.photoImage
        photo = ImageTk.PhotoImage(self.reim)
        #Display image
        self.proimg.configure(image=photo)
        self.proimg.image = photo

    def hw1(self):
        #check if image is choosed
        if  initpath == 'image':
            MsgBox = messagebox.showinfo(title='Warning', message='請先選擇圖片！')
            return
        #read image
        img = cv2.imdecode(np.fromfile(initpath,dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #start image process
        self.pimg = img
        #resize & show result
        self.showresult()

    def hw2(self):
        #Set hist parameters
        hist_height = 540
        hist_width = 540
        nbins = 64
        bin_width = hist_width/nbins
        #check if image is choosed
        if  initpath == 'image':
            MsgBox = messagebox.showinfo(title='Warning', message='請先選擇圖片！')
            return
        #start
        img = cv2.imdecode(np.fromfile(initpath,dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        #Create an empty image for the histogram
        h = np.zeros((hist_height,hist_width))
        #Create array for the bins
        bins = np.arange(nbins,dtype=np.int32).reshape(nbins,1)
        #Calculate and normalise the histogram
        hist_item = cv2.calcHist([img],[0],None,[nbins],[0,256])
        cv2.normalize(hist_item,hist_item,hist_height,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        pts = np.column_stack((bins,hist))
        #Loop through each bin and plot the rectangle in white
        for x,y in enumerate(hist):
            cv2.rectangle(h,(int(x*bin_width),int(y)),(int(x*bin_width + bin_width-1),int(hist_height)),255,-1)
        #Flip upside down
        h=np.flipud(h)
        self.pimg = h
        #resize & show result
        self.showresult()

    def hw3(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業3！')

    def hw4(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業4！')

    def hw5(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業5！')

    def hw6(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業6！')

root = Tk()
my_gui = ImageProcessingGUI(root)
root.mainloop()
