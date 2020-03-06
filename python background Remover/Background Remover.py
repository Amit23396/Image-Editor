from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter.colorchooser import *
import cv2 as cv
import numpy as np
class Root(Tk):
    name = ""
    files_name =""
    def __init__(self):

        super(Root, self).__init__()
        
        #self.labelFrame = ttk.LabelFrame(self, text = 'Open A File ')
        #self.labelFrame.pack(padx=10, pady=10)
        
        
        photo = PhotoImage(file='')
        
        tki = Tk()
        tki.geometry("600x400")
        
        u_w1 = Scale(tki, from_=0, to=255, orient='horizontal', length='100px', cursor='arrow', label="B", sliderlength='10px', troughcolor='blue', bd='0px')
        u_w2 = Scale(tki, from_=0, to=255, orient='horizontal', length='100px', cursor='arrow', label="G", sliderlength='10px', troughcolor='green', bd='0px')
        u_w3 = Scale(tki, from_=0, to=255, orient='horizontal', length='100px', cursor='arrow', label="R", sliderlength='10px', troughcolor='red', bd='0px')
        
        l_w1 = Scale(tki, from_=0, to=255, orient='horizontal', length='100px', cursor='arrow', label="LB", sliderlength='10px', troughcolor='blue', bd='0px')
        l_w2 = Scale(tki, from_=0, to=255, orient='horizontal', length='100px', cursor='arrow', label="LG", sliderlength='10px', troughcolor='green', bd='0px')
        l_w3 = Scale(tki, from_=0, to=255, orient='horizontal', length='100px', cursor='arrow', label="LR", sliderlength='10px', troughcolor='red', bd='0px')
        
        btn1 = Button(tki, text='Select Forground Image', command = self.fileDialog1)
        btn2 = Button(tki, text='Select Background Image', command = self.fileDialog2)
        btn3 = Button(tki, text='Remove Background', command = self.cvOperation)

        sec1 = Label(tki, text="Upper BGR chroma value  ")
        sec2 = Label(tki, text="Lower BGR chroma value  ")
        
        btn1.pack(anchor=NW)
        btn2.pack(anchor=NW)
        btn3.pack(anchor=NW)

        ### Future Editing###

        #sec1.pack(padx=0, pady=0, anchor=N, side=LEFT)
        #u_w1.pack(padx=0, pady=0, anchor=NW, side=LEFT)
        #u_w2.pack(padx=5, pady=0, anchor=NW, side=LEFT)
        #u_w3.pack(padx=10, pady=0, anchor=NW, side=LEFT)

        #sec2.pack(padx=0, pady=0, anchor=W, side=LEFT)
        
        #l_w1.pack(padx=0, pady=0, anchor=W, side=LEFT)
        #l_w2.pack(padx=0, pady=0, anchor=W, side=LEFT)
        #l_w3.pack(padx=0, pady=0, anchor=W, side=LEFT)

        ### Future Editing End###

    
    def fileDialog1(self):
        global name
        self.filename1 = filedialog.askopenfilename(initialdir = "/", title = "Select A File", filetype = (("jpeg", "*.jpg"), ("All Files", "*.jpg")))
        
        name = self.name+self.filename1+","

    def fileDialog2(self):
        global name
        global files_name
        self.filename2 = filedialog.askopenfilename(initialdir = "/", title = "Select A File", filetype = (("jpeg", "*.jpg"), ("All Files", "*.jpg")))

        files_name = name+self.filename2

    def cvOperation(self):
        global files_name
        global panelA
        panelA = None
        
        files_name = files_name.split(',')
        img = cv.imread(files_name[0])
        
        x = cv.imread(files_name[1],1)
        
        frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        image_copy = np.copy(img)

        fgbg = cv.createBackgroundSubtractorMOG2()
        fgmask = fgbg.apply(img)
        
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        lower_blue = np.array([0, 0, 10])     
        upper_blue = np.array([185, 225, 255]) 

        mask = cv.inRange(hsv, lower_blue, upper_blue)
        
        bit = cv.bitwise_and(frame,mask)
        
        res = cv.bitwise_and(img,img,mask = bit)

        height, width = img.shape[:2]

        resize_x = cv.resize(x, (width, height), interpolation = cv.INTER_LINEAR)
        
        #display image on Tkinter window
        
        #image = Image.fromarray(img)
        #image = ImageTk.PhotoImage(image)
        #if panelA is None:
        #    panelA = Label(image=image)
        #    panelA.image = image
        #    panelA.pack(side="bottom", fill="both", expand="yes")
        #else:
        #    panelA.configure(image=image)
        #    panelA.image = image
        
        #image display end here

        
        for i in range(width):
            for j in range(height):
                pixel = res[j, i]
                if np.all(pixel == [0, 0, 0]):
                    try:
                        res[j, i] = x[j, i]
                    except(Exception):
                        pass

        cv.imshow("Original", img)
        cv.imshow("Edited", res)
        
if __name__ == '__main__':
    root = Root()
    root.mainloop()


