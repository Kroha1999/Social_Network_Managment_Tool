import tkinter as tk
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
 
        for F in (StartPage, ChooseCategory): # for each page
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew") # grid it to container
 
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
        tk.Frame.__init__(self, parent,bg="white")

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
        tk.Frame.__init__(self, parent,bg="white")
        cent_frame = tk.Frame(self, bg='white')
        
        label = tk.Label(cent_frame, text='Choose category of TASK', font=LARGE_FONT,bg = "white")
        label.pack(pady=10, padx=10,side=tk.TOP)

        global post_img
        global download_img
        global analyze_img
        
        mid_frame = tk.Frame(cent_frame, bg='white')

        post_img= tk.PhotoImage(file='icons\\post.png')
        bt1=tk.Button(mid_frame, text='POST',image=post_img,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(StartPage))
        bt1.pack(side = tk.LEFT,padx=50)
        
        download_img= tk.PhotoImage(file='icons\\download.png')
        bt2=tk.Button(mid_frame, text='DOWNLOAD',image=download_img,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(StartPage))
        bt2.pack(side = tk.LEFT,padx=50)
        
        analyze_img= tk.PhotoImage(file='icons\\analyze.png')
        bt3=tk.Button(mid_frame, text='ANALYZE',image=analyze_img,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(StartPage))
        bt3.pack(side = tk.LEFT,padx=50)

        mid_frame.pack(side=tk.TOP)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

 
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x300")
    m = MultipleWindows(root)
    m.pack(fill=tk.BOTH)
    
    root.mainloop()