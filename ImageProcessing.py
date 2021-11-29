#!/usr/bin/env python3

import base64, os, time
import numpy as np
import cv2, imghdr, random
import tkinter.font as tkf
import math as m
from tkinter import Tk, messagebox, ttk, Label, filedialog, simpledialog
from PIL import Image, ImageTk
from icon import iconImg
#import sympy

#global image path
initpath = ''
#set resize parameters
maxwidth, maxheight = 512, 512
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

        #choose button
        self.choose_button = ttk.Button(master, text="檔案", command=self.imgselect)
        self.choose_button.place(x=40,y=40)

        #close button
        self.close_button = ttk.Button(master, text="關閉", command=self.closeapp)
        self.close_button.place(x=135,y=40)

        #choose homework
        hw = ['HW1(原始輸出)','HW2(灰階直方圖)','HW3(高斯白雜訊)','HW4(離散小波轉換)','HW5(直方等化)','HW6','HW7','RGB AWGN(Very slow!)','裁切']
        self.combobox = ttk.Combobox(master, values = hw, state="readonly", width = 20)
        self.combobox.current(4)
        self.combobox.place(x=795,y=42)

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
        self.resizedrawimg.place(x=80,y=120)

        #display processed image
        self.resizedproimg = Label(master, image="", bg="white")
        self.resizedproimg.place(x=678,y=120)

        #left image info
        self.linfo = Label(master, font=fs, justify="center", width=45, bg="white")
        self.linfo.place(x=60,y=85)

        #right image indo
        self.rinfo = Label(master, font=fs, justify="center", width=45, bg="white")
        self.rinfo.place(x=660,y=85)

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
        if initpath == "":
            return
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
            'HW1(原始輸出)': self.hw1,
            'HW2(灰階直方圖)': self.hw2,
            'HW3(高斯白雜訊)': self.hw3,
            'HW4(離散小波轉換)': self.hw4,
            'HW5(直方等化)': self.hw5,
            'HW6': self.hw6,
            'HW7': self.hw7,
            'RGB AWGN(Very slow!)': self.rgbawgn,
            '裁切': self.crop
        }
        processhomework = functions[self.combobox.get()]()
    
    def showresult(self):
        if hasattr(self,'proimg') == False:
            return
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
        reim = Image.fromarray(reimg)
        #Tk.photoImage
        photo = ImageTk.PhotoImage(reim)
        #Display resized image
        self.resizedproimg.configure(image=photo)
        self.resizedproimg.image = photo

    def saveleftfile(self):
        files = [('JPEG Files', ('*.jpg','*.jpeg','*.jpe','*.jfif')),
        ('PNG Files', '*.png'),
        ('PPM Files', '*.ppm'),
        ('BMP Files', ('*.bmp', '*.dib'))]
        #check if image exist
        if hasattr(self,'limg') == False:
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
        if hasattr(self,'pim') == False:
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
        if awgn.report == 0:
            return
        #start image process
        img = cv2.cvtColor(self.rawimg, cv2.COLOR_RGB2GRAY)
        y = (img.shape[0])
        x = (img.shape[1])
        dev = awgn.sdev
        zall = []
        #AWGN Channel(Greyscale)
        for i in range (0,y):
            for j in range (0,x-1,2):
                phi = random.randint(1, 10000)/10000
                r = random.randint(1, 10000)/10000
                #gaussian random number
                z1 = dev * m.cos(6.283*phi) * m.sqrt(-2*m.log(r))
                z2 = dev * m.sin(6.283*phi) * m.sqrt(-2*m.log(r))
                zall.append(z1)
                zall.append(z2)
                if img[i,j] + z1 < 0:
                    img[i,j] = 0
                elif img[i,j] + z1 > 255:
                    img[i,j] = 255
                else:
                    img[i,j] = img[i,j] + z1
                #Apply gaussian noise to (x,y+1)
                if img[i,j+1] + z2 < 0:
                    img[i,j+1] = 0
                elif img[i,j+1] + z2 > 255:
                    img[i,j+1] = 255
                else:
                    img[i,j+1] = img[i,j+1] + z2
        #normalize z
        normz = 2 * (zall - np.min(zall)) / (np.max(zall) - np.min(zall)) -1
        #count
        bins = int(awgn.bins)
        hist = np.zeros(bins)
        for i in range(len(normz)):
            for j in range(bins-1):
                if normz[i] <= (2*j)/bins-1:
                    hist[j] += 1
                    normz[i] = 2
        hist = np.array([hist]).T
        #normalize histogram to 0-170
        hist = (hist - np.min(hist)) / (np.max(hist) - np.min(hist)) * 170
        #set hist parameters
        hist_height = 410
        hist_width = 410
        bin_width = hist_width/bins
        #create histogram image
        h = np.zeros((hist_height,hist_width))
        h.fill(128)
        #Loop through each bin and plot the rectangle in white
        for x,y in enumerate(hist):
            cv2.rectangle(h,(int(x*bin_width),int(y)),(int(x*bin_width + bin_width-1),int(hist_height)),255,-1)
        #create full histogram
        fullhist_height = 540
        fullhist_width = 540
        fh = np.zeros((fullhist_height,fullhist_width))
        fh.fill(255)
        cv2.line(fh,(60,480),(480,480),0,1)
        cv2.line(fh,(60,60),(60,480),0,1)
        for i in range(-10,12,2):
            a = abs(i/10)
            b = (i + 10) * 21
            cv2.putText(fh,str(a),(b+48,505),cv2.FONT_HERSHEY_SIMPLEX,0.5,0,1)
        for i in range(0,11):
            a = [1.0,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]
            b = i * 42
            cv2.putText(fh,str(a[i]),(20,64+b),cv2.FONT_HERSHEY_SIMPLEX,0.5,0,1)
        for i in range(0,430,21):
            cv2.rectangle(fh,(60+i,480),(60+i,490),0,1)
        for i in range(0,430,42):
            cv2.rectangle(fh,(60,60+i),(50,60+i),0,1)
        #cover hist to fullhist
        fh[70:480,61:471] = np.flipud(h) #Flip upside down
        #resize & show result
        self.proimg = fh # output of the image is float32(F)
        self.limg = img
        self.showpreview()
        self.showresult()
        self.linfo.configure(text="Image corrupted by AGWN, σ = " + str(dev))
        self.rinfo.configure(text="Gaussian Distribution (normalized to [-1,1])")
    def hw4(self):
        #load raw image & check if image is chosen
        if self.loadimage() == 'Failed':
            return
        #start image process
        dwtk = dwtkk(title="Get dwt params", parent=self.master)
        if dwtk.report == 0:
            return
        k = dwtk.k
        img = cv2.cvtColor(self.rawimg, cv2.COLOR_RGB2GRAY)
        #resize image
        width = 512
        height = 512
        img = cv2.resize(img, (height,width))
        #create empty image
        h = np.zeros((height,width), np.uint8)
        #dwt ll image cache
        sv = np.zeros((height,width), np.uint8)
        for kk in range(0,k):
            n = 2 ** kk
            for i in range(0,int(height/n),2):
                for j in range(0,int(width/n),2):
                    if n == 1:
                        ij00 = int(img[i,j])
                        ij01 = int(img[i,j+1])
                        ij10 = int(img[i+1,j])
                        ij11 = int(img[i+1,j+1])
                    else:
                        ij00 = int(sv[i,j])
                        ij01 = int(sv[i,j+1])
                        ij10 = int(sv[i+1,j])
                        ij11 = int(sv[i+1,j+1])
                    if kk == k-1:
                        h[int(i/2),int(j/2)] = int((ij00 + ij01 + ij10 + ij11)/4)
                    else:
                        sv[int(i/2),int(j/2)] = int((ij00 + ij01 + ij10 + ij11)/4)
                    h[int(i/2),int(j/2+width/2/n)] = int((ij00 - ij01 + ij10 - ij11)/4)
                    h[int(i/2+height/2/n),int(j/2)] = int((ij00 + ij01 - ij10 - ij11)/4)
                    h[int(i/2+height/2/n),int(j/2+width/2/n)] = int((ij00 - ij01 - ij10 + ij11)/4)

        print(h)
        #resize & show result
        self.rinfo.configure(text="Output of Haar Discrete Wavelet Image, k = " + str(k))
        self.proimg = h
        self.showresult()

    def hw5(self):
        #load raw image & check if image is chosen
        if self.loadimage() == 'Failed':
            return
        #start image process
        #maximum greysacle
        Grey = 256
        stack_height = 540
        stack_width = 540
        resize_height = 270
        resize_width = 540
        histarray = np.zeros(Grey, dtype = int)
        img = img = cv2.cvtColor(self.rawimg, cv2.COLOR_RGB2GRAY)
        y = (img.shape[0])
        x = (img.shape[1])
        for i in range(0,y):
            for j in range(0,x):
                histarray[img[i,j]] = histarray[img[i,j]] + 1
        #set hist parameters (original histogram)
        hist_height = 270
        hist_width = 540
        nbins = 255
        bin_width = hist_width/nbins
        #create histogram image
        oh = np.zeros((hist_height,hist_width))
        #calculate and normalise the histogram
        hist_item = np.zeros(Grey, dtype = int)
        cv2.normalize(histarray,hist_item,hist_height,cv2.NORM_MINMAX)
        hist=np.int32(np.around(hist_item))
        #Loop through each bin and plot the rectangle in white
        for x,y in enumerate(hist):
            cv2.rectangle(oh,(int(x*bin_width),int(y)),(int(x*bin_width + bin_width-1),int(hist_height)),256,-1)
        #Flip upside down
        oh = np.flipud(oh) #output of the image is float32(F)
        ofull = np.zeros((stack_height,stack_width))
        ofull.fill(255)
        #stack original image & histogram
        #resize originl image into 1/4
        f1 = resize_width / img.shape[1]
        f2 = resize_height / img.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(img.shape[1] * f), int(img.shape[0] * f))
        rimg = cv2.resize(img, dim)
        #stack originl image to ofull
        ofull[0:0+rimg.shape[0],270-m.floor(rimg.shape[1]/2):270+m.ceil(rimg.shape[1]/2)] = rimg
        #stack original histogram to ofull
        ofull[270:540,0:540] = oh

        #start histogram equalization
        ehistarray = np.zeros(Grey, dtype = int)
        ehistarray[0] = histarray[0]
        for i in range(1,Grey-1):
            ehistarray[i] = ehistarray[i-1] + histarray[i]
        hmin = sorted(set(histarray))[1]
        eimg = np.zeros((img.shape[0],img.shape[1]))
        Tt = np.round(((ehistarray-hmin)/(img.shape[0]*img.shape[1]-hmin))*(Grey-1))
        y = (img.shape[0])
        x = (img.shape[1])
        for i in range(0,y):
            for j in range(0,x):
                eimg[i,j] = Tt[img[i,j]]
        #create histogram image
        eh = np.zeros((hist_height,hist_width))
        #calculate and normalise the histogram
        ephistarray = np.zeros(Grey, dtype = int)
        for i in range(0,y):
            for j in range(0,x):
                ephistarray[int(eimg[i,j])] = ephistarray[int(eimg[i,j])] + 1
        cv2.normalize(ephistarray,ephistarray,hist_height,cv2.NORM_MINMAX)
        ehist=np.int32(np.around(ephistarray))
        #Loop through each bin and plot the rectangle in white
        for x,y in enumerate(ehist):
            cv2.rectangle(eh,(int(x*bin_width),int(y)),(int(x*bin_width + bin_width-1),int(hist_height)),255,-1)
        #Flip upside down
        efull = np.zeros((stack_height,stack_width))
        efull.fill(255)
        #stack original image & histogram
        #resize originl image into 1/4
        f1 = resize_width / eimg.shape[1]
        f2 = resize_height / eimg.shape[0]
        f = min(f1, f2)  # resizing factor
        dim = (int(eimg.shape[1] * f), int(eimg.shape[0] * f))
        eimg = cv2.resize(eimg, dim)
        #stack originl image to ofull
        efull[0:0+eimg.shape[0],270-m.floor(eimg.shape[1]/2):270+m.ceil(eimg.shape[1]/2)] = eimg
        #stack original histogram to ofull
        efull[270:540,0:540] = np.flipud(eh)
        #resize & show result
        self.proimg = efull
        self.limg = ofull
        self.rinfo.configure(text="Equalized image & Histogram")
        self.linfo.configure(text="Input image & Histogram")
        self.showpreview()
        self.showresult()

    def hw6(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業6！')

    def hw7(self):
        MsgBox = messagebox.showinfo(title='Information', message='還沒有作業7！')

    def rgbawgn(self):
        #load raw image & check if image is chosen
        if self.loadimage() == 'Failed':
            return
        #set AWGN parameters
        awgn = awgnparams(title="AWGN Parameters", parent=self.master)
        if awgn.report == 0:
            return
        #start image process
        img = self.rawimg
        B,G,R = cv2.split(img)
        x = (img.shape[0])
        y = (img.shape[1])
        dev = awgn.sdev
        #AWGN Channel(RGB)
        for i in range (1,y):
            for j in range (1,x-1):
                phi = random.randint(1, 10)/10
                r = random.randint(1, 10)/10
                #Blue Channel with gaussian
                z1 = dev * m.cos(2*3.14*phi) * m.sqrt(-2*m.log(r))
                z2 = dev * m.sin(2*3.14*phi) * m.sqrt(-2*m.log(r))
                #(x,y)
                if B[j,i] + z1 < 0:
                    B[j,i] = 0
                elif B[j,i] + z1 > 255:
                    B[j,i] = 255
                else:
                    B[j,i] = B[j,i] + z1
                #(x,y+1)
                if B[j+1,i] + z2 < 0:
                    B[j+1,i] = 0
                elif B[j+1,i] + z2 > 255:
                    B[j+1,i] = 255
                else:
                    B[j+1,i] = B[j+1,i] + z2
                #Green Channel with gaussian
                phi = random.randint(1, 10)/10
                r = random.randint(1, 10)/10
                z1 = dev * m.cos(2*3.14*phi) * m.sqrt(-2*m.log(r))
                z2 = dev * m.sin(2*3.14*phi) * m.sqrt(-2*m.log(r))
                #(x,y)
                if G[j,i] + z1 < 0:
                    G[j,i] = 0
                elif G[j,i] + z1 > 255:
                    G[j,i] = 255
                else:
                    G[j,i] = G[j,i] + z1
                #(x,y+1)
                if G[j+1,i] + z2 < 0:
                    G[j+1,i] = 0
                elif G[j+1,i] + z2 > 255:
                    G[j+1,i] = 255
                else:
                    G[j+1,i] = G[j+1,i] + z2
                #Red Channel with gaussian
                phi = random.randint(1, 10)/10
                r = random.randint(1, 10)/10
                z1 = dev * m.cos(2*3.14*phi) * m.sqrt(-2*m.log(r))
                z2 = dev * m.sin(2*3.14*phi) * m.sqrt(-2*m.log(r))
                #(x,y)
                if R[j,i] + z1 < 0:
                    R[j,i] = 0
                elif R[j,i] + z1 > 255:
                    R[j,i] = 255
                else:
                    R[j,i] = R[j,i] + z1
                #(x,y+1)
                if R[j+1,i] + z2 < 0:
                    R[j+1,i] = 0
                elif R[j+1,i] + z2 > 255:
                    R[j+1,i] = 255
                else:
                    R[j+1,i] = R[j+1,i] + z2
        img = cv2.merge([B,G,R])
        #resize & show result
        self.proimg = img
        #self.limg = img
        self.rinfo.configure(text="Image with Gaussian noise, σ = " + str(dev))
        self.showpreview()
        self.showresult()

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
        b = [20,40,80,160]
        self.bin_label = Label(slave, text="Number of histogram bins", ).pack()
        self.bin = ttk.Combobox(slave, values = b, state="readonly", width = 4)
        self.bin.current(2)
        self.bin.pack()
        return slave
    def variance(self):
        vd = self.vd_entry.get()
        self.bins = self.bin.get()
        if vd=="":
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入值！')
            return
        try:
            float(vd)
        except ValueError:
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入整數！')
            return
        if float(vd) <= 0:
            MsgBox = messagebox.showinfo(title='Warning', message='數值須大於0！')
            return
        self.sdev = round(m.sqrt(int(vd)),2)
        self.destroy()
    def deviation(self):
        vd = self.vd_entry.get()
        self.bins = self.bin.get()
        if vd=="":
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入值！')
            return
        try:
            float(vd)
        except ValueError:
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入整數！')
            return
        if float(vd) <= 0:
            MsgBox = messagebox.showinfo(title='Warning', message='數值須大於0！')
            return
        self.sdev = round(float(vd),2)
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

# class tkinter.simpledialog.Dialog (for hw3 AWGN Variance & Deviation)
# https://docs.python.org/zh-tw/3/library/dialog.html
class dwtkk(simpledialog.Dialog):
    def __init__(self, parent, title):
        self.k = None
        self.report = None
        super().__init__(parent, title)
    def body(self, slave):
        self.k_frame = ttk.Frame(self)
        self.k_frame.pack(side="bottom")
        self.k_label = Label(slave, text="Input level of dwt (k<10)").pack()
        self.k_entry = ttk.Entry(slave)
        self.k_entry.pack()
        return slave
    def getk(self):
        k = self.k_entry.get()
        if k=="":
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入值！')
            return
        try:
            int(k)
        except ValueError:
            MsgBox = messagebox.showinfo(title='Warning', message='請輸入正整數！')
            return
        if int(k) <= 0:
            MsgBox = messagebox.showinfo(title='Warning', message='數值須大於0！')
        if int(k) >= 10:
            MsgBox = messagebox.showinfo(title='Warning', message='數值須小於10！')
            return
        self.k = int(k)
        self.destroy()
    def cancel(self):
        self.report = 0
        self.destroy()
    def buttonbox(self):
        self.var_button = ttk.Button(self, text='Confirm', command=self.getk)
        self.var_button.pack(side="left")
        cancel_button = ttk.Button(self, text='Cancel', command=self.cancel)
        cancel_button.pack()

root = Tk()
my_gui = ImageProcessingGUI(root)
root.mainloop()
