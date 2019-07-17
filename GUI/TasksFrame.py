import tkinter as tk
from tkinter.filedialog import askopenfilename
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
        root.update()
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
                                command=lambda *args: startPlayGif(cent_frame,gif_button,'icons\\plus1.gif',25,0.02,func=lambda : controller.show_frame(ChooseCategory)))
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

def choosePhoto(mybtn):
    global choosePhotoImg
    path = askopenfilename(filetypes=[("Image File",'.jpg'),("Image File",'.png')])
    #im = Image.open(path)
    if path != '':
        #im = Image.open(file = path)
        #choosePhotoImg = tk.PhotoImage(im)
        choosePhotoImg =  tk.PhotoImage(file = path)
        print(str(int(choosePhotoImg.height()/300))+str(int(choosePhotoImg.width()/200)))
        choosePhotoImg=choosePhotoImg.subsample(int(choosePhotoImg.width()/200),int(choosePhotoImg.height()/300))
        mybtn.configure(image = choosePhotoImg)



class PostFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cent_frame = tk.Frame(self, bg='white')
        global choosePhotoImg
        choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        choosePh = tk.Button(cent_frame, image=choosePhotoImg,command = lambda *args: choosePhoto(choosePh))
        choosePh.pack(side=tk.TOP)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x300")
    m = MultipleWindows(root)
    m.pack(fill=tk.BOTH)
    
    root.mainloop()