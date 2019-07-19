import tkinter as tk
from instapy_cli import client # TESTING
from instagram_private_api import client # TESTING
import instagram_private_api_extensions as ipae # TESTING

from tkinter.filedialog import askopenfilename
from tkinter import tix
from PIL import Image, ImageTk
import time

LARGE_FONT = ("Colibri", 12) # font's family is Verdana, font's size is 12 
 
class MultipleWindows(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
        self.frames = {} # these are pages we want to navigate to
 
        for F in (StartPage, ChooseCategory,ChooseSocial,PostFrame): # for each page
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew") # grid it to container
            frame.configure(bg='white')
 
        self.show_frame(StartPage) # let the first page is StartPage
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
 

#Gif button function
def startPlayGif(root,btn,filepath,numb_of_frames,delay,func=None):
    global gif_img
    counter = 0
    while counter < numb_of_frames:
        gif_img = tk.PhotoImage(file = filepath, format="gif -index " + str(counter))
        btn.configure(image=gif_img)
        time.sleep(delay)
        root.update_idletasks()#update()
        counter +=1
    
    gif_img = tk.PhotoImage(file = filepath, format="gif -index " + str(0))
    btn.configure(image=gif_img)

    if func != None:
        func()
    


# *********************** EVERY NEXT CLASS IS A SEPARATE WINDOW ****************************
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        cent_frame = tk.Frame(self, bg='white')
        
        label = tk.Label(cent_frame , text='Here you can create different tasks about:'+
                                    '\n1. Posting different data for different social networks'+
                                    '\n2. Downloading different data from yours and other people accounts'+
                                    '\n3. Analize your accounts activities and custom data'
                                                                , font=LARGE_FONT, bg = "white")
        label.pack(pady=10, padx=10) # center alignment

        global gif_img
        gif_img =  tk.PhotoImage(file='icons\\plus1.gif', format="gif -index 0")
        gif_button = tk.Button(cent_frame,text="GIF",bd=0,bg="white",activebackground="white",image = gif_img,
                                command=lambda *args: startPlayGif(cent_frame,gif_button,'icons\\plus1.gif',25,0.005,func=lambda : controller.show_frame(ChooseCategory)))
        gif_button.pack()        
        cent_frame.place(relx=0.5,rely=0.48, anchor=tk.CENTER)

class ChooseCategory(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cent_frame = tk.Frame(self, bg='white')
        
        self.label1 = tk.Label(cent_frame, text='Choose category of TASK', font=LARGE_FONT,bg = "white")
        self.label1.pack(pady=10, padx=10,side=tk.TOP)

        global gl_img1
        global gl_img2
        global gl_img3
        
        mid_frame = tk.Frame(cent_frame, bg='white')

        gl_img1= tk.PhotoImage(file='icons\\post.png')
        bt1=tk.Button(mid_frame, text='POST',image=gl_img1,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(ChooseSocial))
        bt1.pack(side = tk.LEFT,padx=50)
        
        gl_img2= tk.PhotoImage(file='icons\\download.png')
        bt2=tk.Button(mid_frame, text='DOWNLOAD',image=gl_img2,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(ChooseSocial))
        bt2.pack(side = tk.LEFT,padx=50)
        
        gl_img3= tk.PhotoImage(file='icons\\analyze.png')
        bt3=tk.Button(mid_frame, text='ANALYZE',image=gl_img3,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(ChooseSocial))
        bt3.pack(side = tk.LEFT,padx=50)

        mid_frame.pack(side=tk.TOP)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)


class ChooseSocial(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cent_frame = tk.Frame(self, bg='white')
        
        label = tk.Label(cent_frame, text='Choose Social', font=LARGE_FONT,bg = "white")
        label.pack(pady=10, padx=10,side=tk.TOP)

        global gl_img4
        global gl_img5
        global gl_img6
        global gl_img7

        mid_frame = tk.Frame(cent_frame, bg='white')

        gl_img4 = tk.PhotoImage(file='icons\\instagram_btn.png')
        inst_btn=tk.Button(mid_frame, text='Instagram account',image=gl_img4,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(PostFrame))
        inst_btn.pack(side = tk.LEFT,padx=50)


        gl_img5 = tk.PhotoImage(file='icons\\facebook_btn.png')
        face_btn=tk.Button(mid_frame, text='Facebook account',image=gl_img5,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(StartPage))
        face_btn.pack(side = tk.LEFT,padx=50)

        gl_img6 = tk.PhotoImage(file='icons\\twitter_btn.png')
        twit_btn=tk.Button(mid_frame, text='Twitter account',image=gl_img6,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(StartPage))
        twit_btn.pack(side = tk.LEFT,padx=50)

        gl_img7 = tk.PhotoImage(file='icons\\custom_btn.png')
        cust_btn=tk.Button(mid_frame, text='Custom Accoun',image=gl_img7,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(StartPage))
        cust_btn.pack(side = tk.LEFT,padx=50)

        mid_frame.pack(side=tk.TOP)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)



global choosePhotoImg
MAX_UI_X = 600
MAX_UI_Y = 314

def choosePhoto(mybtn):
    global choosePhotoImg
    path = askopenfilename(filetypes=[("Image File",'.jpg'),("Image File",'.png')])
    if path != '':
        im = Image.open(str(path))
        print("\n")
        print("Before: "+str(int(im.height))+"   "+str(int(im.width)))
        
        if im.height > im.width:
            
            #portrait 300x240
            if (im.height/im.width) > 1.25:
                #looking for offset to crop
                offset = im.height-1.25*im.width
                print("offset "+str(offset))
                cut_side = int(offset/2)+1
                #cropping
                im = im.crop([0,cut_side,im.width,im.height-cut_side])
                
            #change to UI sizes by Y
    
            wpercent = (MAX_UI_Y/float(im.size[1]))
            prop_x = int((float(im.size[0])*float(wpercent)))
            im = im.resize((prop_x,MAX_UI_Y), Image.ANTIALIAS)

        elif im.height < im.width:
            #landscape 600x314
            if (im.width/im.height) > 1.91:
                #image will be cropped
                offset = im.width-1.91*im.height
                cut_side = int(offset/2)+1
                #cropping
                im = im.crop([cut_side,0,im.width-cut_side,im.height])
            
            #change to UI sizes by X
            wpercent = (MAX_UI_X/float(im.size[0]))
            prop_y = int((float(im.size[1])*float(wpercent)))
            im = im.resize((MAX_UI_X,prop_y), Image.ANTIALIAS)

        else:
            #square 314x314
            im = im.resize((MAX_UI_Y,MAX_UI_Y), Image.ANTIALIAS)
            

        choosePhotoImg = ImageTk.PhotoImage(im)
        print("After: "+ str(int(im.height))+"   "+str(int(im.width)))
        mybtn.configure(image = choosePhotoImg, text = str(path))


#USERNAME = "_testaccoun_"
#PASSWORD = ""
#def sendPost(photo, nc_text1, desc_text, nc_text2,func=None):
#    #TODO:UPLOAD PHOTOS AND COOKIE FILES ON REGISTER
#    with client(USERNAME,PASSWORD) as cli:
#        cli.upload(photo,nc_text1+desc_text+nc_text2)
#    if func != None:
#        func()


class PostFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cent_frame = tk.Frame(self, bg='white')

        global choosePhotoImg
        choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        choosePh = tk.Button(cent_frame, image=choosePhotoImg,bd=1,bg="white",command = lambda *args: choosePhoto(choosePh))
        choosePh.pack(side=tk.TOP,pady=10)

        lab_loc=tk.Label(cent_frame,text= "This is location field",bg="white",font=LARGE_FONT)
        lab_loc.pack(side=tk.TOP,pady=5)
        
        lab_nc1t=tk.Label(cent_frame,text= "This is permanent description field",bg="white",font=LARGE_FONT)
        lab_nc1t.pack(side=tk.TOP,pady=5)
        #At least one of 3 textboxes must be not empty
        #Unchangeble text Field 1 (This text will not be translated)
        no_change_1_text = tk.Text(cent_frame,bg='white',bd=1,width =50,height = 2)
        no_change_1_text.pack(side=tk.TOP,pady=5)
        

        lab_ct=tk.Label(cent_frame,text= "This is translateble description field",bg="white",font=LARGE_FONT)
        lab_ct.pack(side=tk.TOP,pady=5)
        #Changeble text Field (This text WILL BE translated, if translate option choosen)
        change_text = tk.Text(cent_frame,bg='white',bd=1,width =50,height = 10)
        change_text.pack(side=tk.TOP,pady=5)

        lab_nc2t=tk.Label(cent_frame,text= "This is permanent description field",bg="white",font=LARGE_FONT)
        lab_nc2t.pack(side=tk.TOP,pady=5)
        #Unchangeble text Field 2 (This text will not be translated)
        no_change_2_text = tk.Text(cent_frame,bg='white',bd=1,width =50,height = 2)
        no_change_2_text.pack(side=tk.TOP,pady=5)

        submit_btn = tk.Button(cent_frame,bd=1,width = 50,height = 2,bg='#4A148C',fg='#ffb300',activebackground="#ffb300",text = "SUBMIT",
                                    font='Calibri 12 bold', command = lambda *args: sendPost(choosePhotoImg, no_change_1_text.get("1.0",'end-1c'), change_text.get("1.0",'end-1c'), no_change_2_text.get("1.0",'end-1c'),func=None) )
        submit_btn.pack(side=tk.TOP,pady=5)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x300")
    m = MultipleWindows(root)
    m.pack(fill=tk.BOTH)
    
    root.mainloop()