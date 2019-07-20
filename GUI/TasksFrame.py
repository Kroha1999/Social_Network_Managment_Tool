import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from instapy_cli import client # TESTING
from instagram_private_api import client # TESTING
import instagram_private_api_extensions as ipae # TESTING

from PIL import Image, ImageTk, ImageDraw 
import numpy as np
import json
import time
import copy

#my files
import languages

LARGE_FONT = ("Colibri", 12) # font's family is Verdana, font's size is 12 
PATH_PROFILE_PICS = "ProfilePicsMin\\"

class MultipleWindows(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
        self.frames = {} # these are pages we want to navigate to
 
        for F in (StartPage, ChooseCategory,ChooseSocial,ChooseAccounts,ChooseTranslation,PostPage): # for each page
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
        inst_btn=tk.Button(mid_frame, text='Instagram account',image=gl_img4,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(ChooseAccounts))
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



def circle_img(img, offset=0):
    img=img.convert("RGB")
    npImage=np.array(img)
    h,w=img.size

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size,0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0,0,h,w],0,360,fill=255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)
    
    # Add alpha layer to RGB
    npImage=np.dstack((npImage,npAlpha))    
    
    result = Image.fromarray(npImage)
    return result


#GLOBAL CHOSEN ACCOUNTS VARIABLES
global data_chosen_acc 
global data_choose_acc

with open('data.json') as json_file:  
        data_choose_acc = json.load(json_file)
data_chosen_acc = {}

data_chosen_acc['Instagram'] = []
data_chosen_acc['Facebook'] = []
data_chosen_acc['Twitter'] = []

#GLOBAL CHOSEN TRANSLATION FOR ACCOUNTS VARIABLES
global data_choose_trans
global data_chosen_trans

data_choose_trans = {}
data_chosen_trans = {}

data_chosen_trans['Instagram'] = []
data_chosen_trans['Facebook'] = []
data_chosen_trans['Twitter'] = []


#GLOBAL IMAGE VARIABLE
global myImg
myImg = {}


def updateTree(tree,insert_data):
    i=0
    
    for acc in insert_data['Instagram']:
        global myImg
        ima = circle_img(Image.open(PATH_PROFILE_PICS+acc['nickname']+'.png'))
        myImg[acc["imgUrl"]]=ImageTk.PhotoImage(ima)
            
        tree.insert('', i, "Item"+str(i), text = str(acc["nickname"]),image = myImg[acc["imgUrl"]])
        tree.set("Item"+str(i),'soc',"Instagram")
        tree.set("Item"+str(i),'soc',)
        tree.set("Item"+str(i),'lan',languages.LANGTOCODES[acc['language']])

        i+=1
 

def moveEl(trVFrom,trVTo,datasetFrom,datasetTo):
    moveItems = trVFrom.selection()

    el_num=0
    for item in moveItems:
           
            for el in datasetFrom['Instagram']:
           
                if el['nickname'] == trVFrom.item(item)['text']:
                    datasetTo['Instagram'].append(datasetFrom['Instagram'].pop(el_num))

                el_num = el_num + 1
           
            el_num = 0
    
    trVFrom.delete(*trVFrom.get_children())
    trVTo.delete(*trVTo.get_children())
    updateTree(trVFrom,datasetFrom)
    updateTree(trVTo,datasetTo)


def check_and_go(mydata,func=None):
    global data_chosen_acc
    global data_choose_trans

    if mydata['Instagram']==[] and mydata['Facebook']==[] and mydata['Twitter']==[]:
        tk.messagebox.showerror("Please choose accounts","At least 1 account must be chosen")
        return

    if func != None:
        data_choose_trans = copy.deepcopy(data_chosen_acc)
        func()

class ChooseAccounts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        global data_chosen_acc 
        global data_choose_acc
        cent_frame = tk.Frame(self, bg='white')

        ft = ('Colibri',10)
        styleTree = ttk.Style()
        styleTree.configure('Calendar.Treeview',font=ft,rowheight=33)
        
        choose_frame = tk.Frame(cent_frame,bg='white')

        ## Treeview with objects to choose
        chooseTreeView = ttk.Treeview(choose_frame,height=15,style='Calendar.Treeview')
        chooseTreeView.config(columns =('soc','lan'))
        chooseTreeView.column('soc',width=75,anchor=tk.CENTER)
        chooseTreeView.heading('soc',text='Social')
        chooseTreeView.column('lan',width=75,anchor=tk.CENTER)
        chooseTreeView.heading('lan',text='Language')
        chooseTreeView.column('#0',width=150,anchor=tk.CENTER)
        chooseTreeView.heading('#0',text='Nickname')
        chooseTreeView.pack(side = tk.LEFT)
        
        ## choose buttons frame
        button_frame = tk.Frame(choose_frame,bg='white')
        btChoose = tk.Button(button_frame,text = "CHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(chooseTreeView,chosenTreeView,data_choose_acc,data_chosen_acc))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        btChoose = tk.Button(button_frame,text = "UNCHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(chosenTreeView,chooseTreeView,data_chosen_acc,data_choose_acc))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        button_frame.pack(side = tk.LEFT,fill="both", expand=True,pady=200)


        ## TreeView with chosen objects
        chosenTreeView = ttk.Treeview(choose_frame,height=15,style='Calendar.Treeview')
        
        chosenTreeView.config(columns =('soc','lan'))
        chosenTreeView.column('soc',width=75,anchor=tk.CENTER)
        chosenTreeView.heading('soc',text='Social')
        chosenTreeView.column('lan',width=75,anchor=tk.CENTER)
        chosenTreeView.heading('lan',text='Language')
        chosenTreeView.column('#0',width=150,anchor=tk.CENTER)
        chosenTreeView.heading('#0',text='Nickname')
        chosenTreeView.pack(side = tk.LEFT)

        #Button confirm
        btConfirm = tk.Button(cent_frame,text="SUBMIT",bg = 'white',
                                command = lambda *args: check_and_go(data_chosen_acc,lambda : controller.show_frame(ChooseTranslation)))
        btConfirm.pack(side= tk.BOTTOM)

        choose_frame.pack(side = tk.TOP, pady=10)
        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        
        updateTree(chooseTreeView,data_choose_acc)
        updateTree(chosenTreeView,data_chosen_acc)


def show_choose_trans(var,choose_frame,chooseTree=None,chosenTree=None):
    global data_chosen_trans 
    global data_choose_trans

    if var.get() != 2:
        try:
            choose_frame.pack_forget()
        except:
            pass
    else:
        try:
            choose_frame.pack()
            updateTree(chooseTree, data_choose_trans)
            updateTree(chosenTree, data_chosen_trans)
        except:
            pass

class ChooseTranslation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global data_chosen_trans
        global data_choose_trans
        cent_frame = tk.Frame(self, bg='white')
        
        
        var = tk.IntVar()
        var.set(0)
        

        label = tk.Label(cent_frame,text="HERE \nYOU NEED TO CHOOSE WHETHER \nTO TRANSLATE OPTION OF THE POST",
                             bg="white",font = "Calibri 20", fg = "#4A148C" )
        label.pack(side = tk.TOP,pady=20)

        radio_not_trans = tk.Radiobutton(cent_frame,text="Not translate (keep the description \nof the post in the same language for all account)",
                            bg="white",font = "Calibri 12", fg = "#4A148C", variable = var, value = 0,width = 100,command = lambda: show_choose_trans(var,choose_frame) )#36
        
        
        radio_trans = tk.Radiobutton(cent_frame,text="  Translate post according to the each account language",#53
                            bg="white",font = "Calibri 12", fg = "#4A148C", variable = var, value = 1,width = 100,command = lambda: show_choose_trans(var,choose_frame) )
        

        radio_trans_opt = tk.Radiobutton(cent_frame,text="Translate post according to the CHOSEN account language\nother accounts will keep the post description \nin original language",
                            bg="white",font = "Calibri 12", fg = "#4A148C", variable = var, value = 2,width = 100,command = lambda: show_choose_trans(var,choose_frame,chooseTransTree,chosenTransTree) )
        
        
        radio_not_trans.pack(side = tk.TOP,pady=5)
        radio_trans.pack(side = tk.TOP,pady=5)
        radio_trans_opt.pack(side = tk.TOP,pady=5)
        
        #this is hidden frame##########################################################
        choose_frame = tk.Frame(cent_frame,bg = 'white')
        lab = tk.Label(choose_frame,bg = 'white', text = "!!!!!!!!!!!!!HIDDEN FRAME!!!!!!!!!!!!!!!!")
        lab.pack(side = tk.TOP)
        
        ## Treeview with objects to choose
        chooseTransTree = ttk.Treeview(choose_frame,height=15,style='Calendar.Treeview')
        chooseTransTree.config(columns =('soc','lan'))
        chooseTransTree.column('soc',width=75,anchor=tk.CENTER)
        chooseTransTree.heading('soc',text='Social')
        chooseTransTree.column('lan',width=75,anchor=tk.CENTER)
        chooseTransTree.heading('lan',text='Language')
        chooseTransTree.column('#0',width=150,anchor=tk.CENTER)
        chooseTransTree.heading('#0',text='Nickname')
        chooseTransTree.pack(side = tk.LEFT)
        
         ## choose buttons frame
        button_frame = tk.Frame(choose_frame,bg='white')
        btChoose = tk.Button(button_frame,text = "CHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(chooseTransTree,chosenTransTree,data_choose_trans,data_chosen_trans))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        btChoose = tk.Button(button_frame,text = "UNCHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(chosenTransTree,chooseTransTree,data_chosen_trans,data_choose_trans))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        button_frame.pack(side = tk.LEFT,fill="both", expand=True,pady=200)


        ## TreeView with chosen objects
        chosenTransTree = ttk.Treeview(choose_frame,height=15,style='Calendar.Treeview')
        
        chosenTransTree.config(columns =('soc','lan'))
        chosenTransTree.column('soc',width=75,anchor=tk.CENTER)
        chosenTransTree.heading('soc',text='Social')
        chosenTransTree.column('lan',width=75,anchor=tk.CENTER)
        chosenTransTree.heading('lan',text='Language')
        chosenTransTree.column('#0',width=150,anchor=tk.CENTER)
        chosenTransTree.heading('#0',text='Nickname')
        chosenTransTree.pack(side = tk.LEFT)

        #Button confirm
        btConfirm = tk.Button(cent_frame,text="SUBMIT",bg = 'white',
                                command = lambda *args: controller.show_frame(PostPage))
        btConfirm.pack(side= tk.BOTTOM)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)


class PostPage(tk.Frame):
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
                                    font='Calibri 12 bold',command=lambda : controller.show_frame(StartPage))#, command = lambda *args: sendPost(choosePhotoImg, no_change_1_text.get("1.0",'end-1c'), change_text.get("1.0",'end-1c'), no_change_2_text.get("1.0",'end-1c'),func=None) )
        submit_btn.pack(side=tk.TOP,pady=5)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x300")
    m = MultipleWindows(root)
    m.pack(fill=tk.BOTH)
    
    root.mainloop()