#!/usr/bin/env python3

import base64, os
import numpy as np
import cv2, imghdr
import tkinter.font as tkf
from tkinter import Tk, messagebox, ttk, Label, filedialog, simpledialog
from PIL import Image, ImageTk
from icon import iconImg
#import sympy

#global image path
initpath = ''
#set resize parameters
maxwidth, maxheight = 540, 540
#icon
tmpIcon = open('tmp.ico','wb+')
tmpIcon.write(base64.b64decode(iconImg))
tmpIcon.close()

class ImageProcessingGUI:
    def __init__(self, master):
    
        self.master = master
        master.title("AIP61075013H")
        master.geometry('1280x720')
        master.configure(background='white')
        master.iconbitmap('tmp.ico')
        os.remove('tmp.ico')
        fs = tkf.Font(family="Yu Gothic Light", size=16)
        self.im = ''
        
        #choose button
        self.choose_button = ttk.Button(master, text="檔案", command=self.imgselect)
        self.choose_button.place(x=40,y=40)

        #close button
        self.close_button = ttk.Button(master, text="關閉", command=self.closeapp)
        self.close_button.place(x=135,y=40)

        #choose homework
        hw = ['HW1','HW2','HW3','HW4','HW5','HW6','裁切']
        self.combobox = ttk.Combobox(master, values = hw, state="readonly", width = 10)
        self.combobox.current(0)
        self.combobox.place(x=865,y=42)

        #process button
        self.process_button = ttk.Button(master, text="處理", command=self.run)
        self.process_button.place(x=965,y=40)

        #save left image
        self.save_l_button = ttk.Button(master, text="儲存左圖為..", command=self.saveleftfile)
        self.save_l_button.place(x=1060,y=40)

        #save right image
        self.save_button = ttk.Button(master, text="儲存右圖為..", command=self.saverightfile)
        self.save_button.place(x=1155,y=40)

        #photo info
        self.imginfo = Label(master, text="", bg="white")
        self.imginfo.place(x=235,y=43)

        #display image
        self.resizedrawimg = Label(master, image="", bg="white")
        self.resizedrawimg.place(x=60,y=110)

        #show processed image
        self.resizedproimg = Label(master, image="", bg="white")
        self.resizedproimg.place(x=670,y=110)

        #left image info
        self.linfo = Label(master, font=fs, justify="center", width=45, bg="white")
        self.linfo.place(x=60,y=80)

        #right image indo
        self.rinfo = Label(master, font=fs, justify="center", width=45, bg="white")
        self.rinfo.place(x=670,y=80)

    def closeapp(self):
        MsgBox = messagebox.askquestion(title='Information', message='確定要關閉嗎？')
        if MsgBox == 'yes':
            root.destroy()

    def imgselect(self):
        global initpath
        #open image as jpg(RGB)
        files = [('Image Files', 
        ('*.jpg','*.jpeg','*.jpe','*.jfif','*.png','*.bmp','*.dib','*.ppm')),
        ('All Files', '*.')]
        initpath = filedialog.askopenfilename(filetypes = files)
        img = cv2.imdecode(np.fromfile(initpath,dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.limg = img
        #show left panel
        self.showpreview()
        self.linfo.configure(text="Input image")
        self.imginfo.configure(
            text="解析度："+str(img.shape[1])+"x"+str(img.shape[0])
            +"      檔案格式："+str(imghdr.what(initpath)))

    def showpreview(self):
        #resize image
        img = self.limg
        f1 = maxwidth / img.shape[1]
        f2 = maxheight / img.shape[0]
        f = min(f1, f2)  # resizing factor
        fdim = (int(img.shape[1] * f), int(img.shape[0] * f))
        reimg = cv2.resize(img, fdim)
        im = Image.fromarray(reimg)
        photo = ImageTk.PhotoImage(im)
        self.resizedrawimg.configure(image=photo)
        self.resizedrawimg.image = photo

    def loadimage(self):
        #check if image is choosed
        if  initpath == '':
            MsgBox = messagebox.showinfo(title='Warning', message='請先選擇圖片！')
            return 'Failed'
        #read image to rawimg
        img = cv2.imdecode(np.fromfile(initpath,dtype=np.uint8), cv2.IMREAD_COLOR)
        self.rawimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def run(self):
        #run homework choosed from combobox
        functions = {
            'HW1': self.hw1,
            'HW2': self.hw2,
            'HW3': self.hw3,
            'HW4': self.hw4,
            'HW5': self.hw5,
            'HW6': self.hw6,
            '裁切': self.crop
        }
        processhomework = functions[self.combobox.get()]()
    
    def showresult(self):
        #resize image
        f1 = maxwidth / self.proimg.shape[1]
        f2 = maxheight / self.proimg.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(self.proimg.shape[1] * f), int(self.proimg.shape[0] * f))
        reimg = cv2.resize(self.proimg, dim)
        #save as Tk.image to show on label
        self.pim = Image.fromarray(self.proimg)
        #incase for other format, e.g.HW2, convert to RGB mode before save
        if self.pim.mode !='RGB':
            self.pim = self.pim.convert('RGB')
        self.reim = Image.fromarray(reimg)
        #Tk.photoImage
        photo = ImageTk.PhotoImage(self.reim)
        #Display resized image
        self.resizedproimg.configure(image=photo)
        self.resizedproimg.image = photo

    def saveleftfile(self):
        files = [('JPEG Files', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
        ('PNG Files', '*.png'),
        ('PPM Files', '*.ppm'),
        ('BMP Files', ('*.bmp', '*.dib'))]
        #check if image exist
        if self.limg == '':
            MsgBox = messagebox.showinfo(title='Warning', message='請先進行影像處理！')
            return
        limg = Image.fromarray(self.limg)
        #incase for other format, e.g.HW2, convert to RGB mode before save
        if limg.mode !='RGB':
            limg = limg.convert('RGB')
        filename = filedialog.asksaveasfile(mode='wb+', filetypes = files, defaultextension = files)
        if not filename:
            return
        limg.save(filename)

    def saverightfile(self):
        files = [('JPEG Files', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
        ('PNG Files', '*.png'),
        ('PPM Files', '*.ppm'),
        ('BMP Files', ('*.bmp', '*.dib'))]
        #check if image is processed
        if self.pim == '':
            MsgBox = messagebox.showinfo(title='Warning', message='請先進行影像處理！')
            return
        filename = filedialog.asksaveasfile(mode='wb+', filetypes = files, defaultextension = files)
        if not filename:
            return
        self.pim.save(filename)

    def hw1(self):
        #load raw image & check if image is chosen
        if self.loadimage() == 'Failed':
            return
        #start image process
        self.proimg = self.rawimg
        #resize & show result
        self.rinfo.configure(text="Output input image")
        self.showresult()

    def hw2(self):
        #load raw image & check if image is chosen
        if self.loadimage() == 'Failed':
            return
        #set hist parameters
        hist_height = 540
        hist_width = 540
        nbins = 256
        bin_width = hist_width/nbins
        #turn rawimage to greyscale(or r/g/b)
        img = cv2.cvtColor(self.rawimg, cv2.COLOR_RGB2GRAY)
        #create histogram image
        h = np.zeros((hist_height,hist_width))
        #create array for the bins
        bins = np.arange(nbins,dtype=np.int32).reshape(nbins,1)
        #calculate and normalise the histogram
        hist_item = cv2.calcHist([img],[0],None,[nbins],[0,256])
        cv2.normalize(hist_item,hist_item,hist_height,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        #Loop through each bin and plot the rectangle in white
        for x,y in enumerate(hist):
            cv2.rectangle(h,(int(x*bin_width),int(y)),(int(x*bin_width + bin_width-1),int(hist_height)),255,-1)
        #Flip upside down
        self.proimg = np.flipud(h) #output of the image is float32(F)
        #resize & show result
        self.limg = img
        self.showpreview()
        self.showresult()
        self.linfo.configure(text="Greyscale image")
        self.rinfo.configure(text="Greyscale histogram")

    def hw3(self):
        #load raw image & check if image is chosen
        if self.loadimage() == 'Failed':
            return
        #set AWGN parameters
        awgn = awgnparams(title="AWGN Parameters", parent=self.master)
        print(awgn.var)
        #start image process
        img = self.rawimg
        self.proimg = img
        #resize & show result
        self.showresult()

    def hw4(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業4！')

    def hw5(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業5！')

    def hw6(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業6！')

    def crop(self):
        #load raw image & check if image is chosen
        if self.loadimage() == 'Failed':
            return
        d = cropcoords(title="Crop with coords", parent=self.master)
        if d.report == 0:
            return
        img = self.rawimg
        #image crop
        img = img[d.y:d.y+d.h, d.x:d.x+d.w]
        self.pimg = img
        self.showresult()
    
# class tkinter.simpledialog.Dialog (for cropping image)
# https://docs.python.org/zh-tw/3/library/dialog.html
class cropcoords(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.report = None
        super().__init__(parent, title)
    def body(self, slave):
        self.x_label = Label(slave, text="upper left x").pack()
        self.x_entry = ttk.Entry(slave)
        self.x_entry.pack()
        self.y_label = Label(slave, text="upper left y").pack()
        self.y_entry = ttk.Entry(slave)
        self.y_entry.pack()
        self.w_label = Label(slave, text="crop width").pack()
        self.w_entry = ttk.Entry(slave)
        self.w_entry.pack()
        self.h_label = Label(slave, text="crop height").pack()
        self.h_entry = ttk.Entry(slave)
        self.h_entry.pack()

        return slave
    def confirm(self):
        x = self.x_entry.get()
        y = self.y_entry.get()
        w = self.w_entry.get()
        h = self.h_entry.get()
        if x=="" or y=="" or w=="" or h=="":
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入值！')
            return
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.destroy()
    def cancel(self):
        self.report = 0
        self.destroy()
    def buttonbox(self):
        self.ok_button = ttk.Button(self, text='OK', width=10, command=self.confirm)
        self.ok_button.pack(side="left")
        cancel_button = ttk.Button(self, text='Cancel', width=10, command=self.cancel)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.confirm())
        self.bind("<Escape>", lambda event: self.cancel())

# class tkinter.simpledialog.Dialog (for hw3 AWGN Variance & Deviation)
# https://docs.python.org/zh-tw/3/library/dialog.html
class awgnparams(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.vd = None
        self.report = None
        super().__init__(parent, title)
    def body(self, slave):
        self.vd_frame = ttk.Frame(self)
        self.vd_frame.pack(side="bottom")
        self.vd_label = Label(slave, text="Input Variance or Standard Deviation\n VAR = σ^2").pack()
        self.vd_entry = ttk.Entry(slave)
        self.vd_entry.pack()
        return slave
    def variance(self):
        vd = self.vd_entry.get()
        if vd=="":
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入值！')
            return
        self.var = int(vd)
        self.destroy()
    def deviation(self):
        vd = self.vd_entry.get()
        if vd=="":
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入值！')
            return
        self.var = pow(int(vd),2)
        self.destroy()
    def cancel(self):
        self.report = 0
        self.destroy()
    def buttonbox(self):
        self.var_button = ttk.Button(self, text='VAR', command=self.variance)
        self.var_button.pack(side="left")
        self.dev_button = ttk.Button(self, text='σ', command=self.deviation)
        self.dev_button.pack(side="right")
        cancel_button = ttk.Button(self, text='Cancel', command=self.cancel)
        cancel_button.pack()

root = Tk()
my_gui = ImageProcessingGUI(root)
root.mainloop()
