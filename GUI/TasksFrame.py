import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from PIL import Image, ImageTk, ImageDraw 
import numpy as np
import json
import time
import copy

#my files
import languages

#CONSTANTS
LARGE_FONT = ("Colibri", 12) # font's family is Verdana, font's size is 12 
PATH_PROFILE_PICS = "ProfilePicsMin\\"
MAX_UI_X = 600
MAX_UI_Y = 314

#GLOBAL VARIABLES
global data
global Task_data
global choosePhotoImg
Task_data = {}
global myImg
myImg = {}

# ************************** FUNCTIONS *******************************
#_________________________DATA Functions______________________________
def resetTask():
    global Task_data
    Task_data = {
        'DateTimeCreated': None,
        'DateTimeFinished': None,
        'DateTimeSchedule': None,
        
        'SocialNetwork': None, #  'Instagram','Facebook','Twitter','Custom'
        'TaskType': None, # 'Post','Download','Analyze'
        'AllAccounts': {}, #All accounts in the system for that moment - must not be stored

        #Task[key] => key = Task_Data['SocialNetwork']+Task_Data['TaskType']
        'Task':{
            'InstagramPost':{          
                'chosen_acc':{            #chosen accounts to make post on
                    'Instagram':[],
                    'Facebook':[],
                    'Twitter':[]
                },          
                
                'choose_trans':{},        #chosen accounts to keep the description in original language
                
                'chosen_trans':{          #chosen accounts to translate post with account language
                    'Instagram':[],
                    'Facebook':[],
                    'Twitter':[]
                },        

                'mini_photo':None,        #filetype - minimized photo
                'photo_location': None,   #path
                'not_change_text1': None, #upper not changeble description
                'description':None,       #translateble text
                'not_change_text2': None, #lower not changeble description
            },
            'InstagramDownload':None,
            'InstagramAnalyze':None,
        
            'FacebookPost':None,
            'FacebookDownload':None,
            'FacebookAnalyze':None,

            'TwitterPost':None,
            'TwitterDownload':None,
            'TwitterAnalyze':None
        }  
    }
    #saving all accounts
    with open('data.json') as json_file:  
        Task_data['AllAccounts'] = json.load(json_file)
        #for acc in Task_data['AllAccounts']['Instagram']:


    #print(Task_data)

#ResetTaskVariable on opening the program
resetTask()

def upTask(value,lv_1,lv_3=None):
    resetTask()
    global Task_data
    
    if lv_3 == None:
        Task_data[lv_1] = value
    else:
        #lv_2 is always the same two components of lv_1-> look task data
        lv_2 = Task_data['SocialNetwork']+Task_data['TaskType']
        Task_data[lv_1][lv_2][lv_3] = value
    
    #print("\n"+str(Task_data['Task']))

#________________________Photo Functions______________________________
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

#________________________UI Functions_________________________________
def updateTree(tree,insert_data):
    i=0
    
    for acc in insert_data['Instagram']:
        global myImg
        try:
            ima = myImg[acc['nickname']+acc["imgUrl"]]
        except:
            ima = circle_img(Image.open(PATH_PROFILE_PICS+acc['nickname']+'.png'))
            myImg[acc['nickname']+acc["imgUrl"]]=ImageTk.PhotoImage(ima)

        
        
            
        tree.insert('', i, "Item"+str(i), text = str(acc["nickname"]),image = myImg[acc['nickname']+acc["imgUrl"]])
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

    if mydata['Instagram']==[] and mydata['Facebook']==[] and mydata['Twitter']==[]:
        tk.messagebox.showerror("Please choose accounts","At least 1 account must be chosen")
        return

    if func != None:
        Task_data['Task']['InstagramPost']['choose_trans'] = copy.deepcopy(Task_data['Task']['InstagramPost']['chosen_acc'])
        func()

def show_choose_trans(var,choose_frame,chooseTree=None,chosenTree=None):
    if var.get() != 2:
        try:
            choose_frame.pack_forget()
        except:
            pass
    else:
        try:
            choose_frame.pack()
            updateTree(chooseTree, Task_data['Task']['InstagramPost']['choose_trans'])
            updateTree(chosenTree, Task_data['Task']['InstagramPost']['chosen_trans'])
        except:
            pass

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

# ************************* MULTIPLE WINDOW CONTAINER ****************************************
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
 
    def show_frame(self, name,updateFrame=False):
        try:
            frame = self.frames[name]
        except KeyError:
            print("No such frame: "+ str(name))
            return
        
        if updateFrame:
            try:
                frame.updateView()
            except Exception as e:
                print(e)
                pass
        frame.tkraise()
 
# __________________________EVERY NEXT CLASS IS A SEPARATE WINDOW _____________________________
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
                                    command = lambda: (resetTask() , controller.show_frame(ChooseSocial))) 
        gif_button.pack()        
        cent_frame.place(relx=0.5,rely=0.48, anchor=tk.CENTER)

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
        inst_btn=tk.Button(mid_frame, text='Instagram account',image=gl_img4,bd=0,bg="white",activebackground="white", 
                            command=lambda : (upTask('Instagram','SocialNetwork'),controller.show_frame(ChooseCategory)))
        inst_btn.pack(side = tk.LEFT,padx=50)


        gl_img5 = tk.PhotoImage(file='icons\\facebook_btn.png')
        face_btn=tk.Button(mid_frame, text='Facebook account',image=gl_img5,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(None))
        face_btn.pack(side = tk.LEFT,padx=50)

        gl_img6 = tk.PhotoImage(file='icons\\twitter_btn.png')
        twit_btn=tk.Button(mid_frame, text='Twitter account',image=gl_img6,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(None))
        twit_btn.pack(side = tk.LEFT,padx=50)

        gl_img7 = tk.PhotoImage(file='icons\\custom_btn.png')
        cust_btn=tk.Button(mid_frame, text='Custom Accoun',image=gl_img7,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(None))
        cust_btn.pack(side = tk.LEFT,padx=50)

        mid_frame.pack(side=tk.TOP)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

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
        bt1=tk.Button(mid_frame, text='POST',image=gl_img1,bd=0,bg="white",activebackground="white", command=lambda : (upTask('Post','TaskType'),controller.show_frame(ChooseAccounts,True)))
        bt1.pack(side = tk.LEFT,padx=50)
        
        gl_img2= tk.PhotoImage(file='icons\\download.png')
        bt2=tk.Button(mid_frame, text='DOWNLOAD',image=gl_img2,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(None))
        bt2.pack(side = tk.LEFT,padx=50)
        
        gl_img3= tk.PhotoImage(file='icons\\analyze.png')
        bt3=tk.Button(mid_frame, text='ANALYZE',image=gl_img3,bd=0,bg="white",activebackground="white", command=lambda : controller.show_frame(None))
        bt3.pack(side = tk.LEFT,padx=50)

        mid_frame.pack(side=tk.TOP)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

class ChooseAccounts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        cent_frame = tk.Frame(self, bg='white')

        ft = ('Colibri',10)
        styleTree = ttk.Style()
        styleTree.configure('Calendar.Treeview',font=ft,rowheight=33)
        
        choose_frame = tk.Frame(cent_frame,bg='white')

        ## Treeview with objects to choose
        self.chooseTreeView = ttk.Treeview(choose_frame,height=15,style='Calendar.Treeview')
        self.chooseTreeView.config(columns =('soc','lan'))
        self.chooseTreeView.column('soc',width=75,anchor=tk.CENTER)
        self.chooseTreeView.heading('soc',text='Social')
        self.chooseTreeView.column('lan',width=75,anchor=tk.CENTER)
        self.chooseTreeView.heading('lan',text='Language')
        self.chooseTreeView.column('#0',width=150,anchor=tk.CENTER)
        self.chooseTreeView.heading('#0',text='Nickname')
        self.chooseTreeView.pack(side = tk.LEFT)
        
        ## choose buttons frame
        button_frame = tk.Frame(choose_frame,bg='white')
        btChoose = tk.Button(button_frame,text = "CHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(self.chooseTreeView,self.chosenTreeView,Task_data['AllAccounts'],Task_data['Task']['InstagramPost']['chosen_acc']))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        btChoose = tk.Button(button_frame,text = "UNCHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(self.chosenTreeView,self.chooseTreeView,Task_data['Task']['InstagramPost']['chosen_acc'],Task_data['AllAccounts']))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        button_frame.pack(side = tk.LEFT,fill="both", expand=True,pady=200)


        ## TreeView with chosen objects
        self.chosenTreeView = ttk.Treeview(choose_frame,height=15,style='Calendar.Treeview')
        
        self.chosenTreeView.config(columns =('soc','lan'))
        self.chosenTreeView.column('soc',width=75,anchor=tk.CENTER)
        self.chosenTreeView.heading('soc',text='Social')
        self.chosenTreeView.column('lan',width=75,anchor=tk.CENTER)
        self.chosenTreeView.heading('lan',text='Language')
        self.chosenTreeView.column('#0',width=150,anchor=tk.CENTER)
        self.chosenTreeView.heading('#0',text='Nickname')
        self.chosenTreeView.pack(side = tk.LEFT)

        #Button confirm
        btConfirm = tk.Button(cent_frame,text="SUBMIT",bg = 'white',
                                command = lambda *args: check_and_go(Task_data['Task']['InstagramPost']['chosen_acc'],lambda : controller.show_frame(ChooseTranslation,True)))
        btConfirm.pack(side= tk.BOTTOM)

        choose_frame.pack(side = tk.TOP, pady=10)
        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        self.updateView()
        
    def updateView(self):
        self.chosenTreeView.delete(*self.chosenTreeView.get_children())
        self.chooseTreeView.delete(*self.chooseTreeView.get_children())
        updateTree(self.chooseTreeView,Task_data['AllAccounts'])
        updateTree(self.chosenTreeView,Task_data['Task']['InstagramPost']['chosen_acc'])

class ChooseTranslation(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        cent_frame = tk.Frame(self, bg='white')
        
        self.var = tk.IntVar()
        self.var.set(0)

        label = tk.Label(cent_frame,text="HERE \nYOU NEED TO CHOOSE WHETHER \nTO TRANSLATE OPTION OF THE POST",
                             bg="white",font = "Calibri 20", fg = "#4A148C" )
        label.pack(side = tk.TOP,pady=20)

        radio_not_trans = tk.Radiobutton(cent_frame,text="Not translate (keep the description \nof the post in the same language for all account)",
                            bg="white",font = "Calibri 12", fg = "#4A148C", variable = self.var, value = 0,width = 100,command = lambda: show_choose_trans(self.var,self.choose_frame) )#36
        
        
        radio_trans = tk.Radiobutton(cent_frame,text="  Translate post according to the each account language",#53
                            bg="white",font = "Calibri 12", fg = "#4A148C", variable = self.var, value = 1,width = 100,command = lambda: show_choose_trans(self.var,self.choose_frame) )
        

        radio_trans_opt = tk.Radiobutton(cent_frame,text="Translate post according to the CHOSEN account language\nother accounts will keep the post description \nin original language",
                            bg="white",font = "Calibri 12", fg = "#4A148C", variable = self.var, value = 2,width = 100,command = lambda: show_choose_trans(self.var,self.choose_frame,self.chooseTransTree,self.chosenTransTree) )
        
        
        radio_not_trans.pack(side = tk.TOP,pady=5)
        radio_trans.pack(side = tk.TOP,pady=5)
        radio_trans_opt.pack(side = tk.TOP,pady=5)
        
        #this is hidden frame##########################################################
        self.choose_frame = tk.Frame(cent_frame,bg = 'white')
        
        ## Treeview with objects to choose
        self.chooseTransTree = ttk.Treeview(self.choose_frame,height=15,style='Calendar.Treeview')
        self.chooseTransTree.config(columns =('soc','lan'))
        self.chooseTransTree.column('soc',width=75,anchor=tk.CENTER)
        self.chooseTransTree.heading('soc',text='Social')
        self.chooseTransTree.column('lan',width=75,anchor=tk.CENTER)
        self.chooseTransTree.heading('lan',text='Language')
        self.chooseTransTree.column('#0',width=150,anchor=tk.CENTER)
        self.chooseTransTree.heading('#0',text='Nickname')
        self.chooseTransTree.pack(side = tk.LEFT)
        
         ## choose buttons frame
        button_frame = tk.Frame(self.choose_frame,bg='white')
        btChoose = tk.Button(button_frame,text = "CHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(self.chooseTransTree,self.chosenTransTree,Task_data['Task']['InstagramPost']['choose_trans'],Task_data['Task']['InstagramPost']['chosen_trans']))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        btChoose = tk.Button(button_frame,text = "UNCHOOSE\nSELECTED",width=13,command = lambda *args: moveEl(self.chosenTransTree,self.chooseTransTree,Task_data['Task']['InstagramPost']['chosen_trans'],Task_data['Task']['InstagramPost']['choose_trans']))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        button_frame.pack(side = tk.LEFT,fill="both", expand=True,pady=200)


        ## TreeView with chosen objects
        self.chosenTransTree = ttk.Treeview(self.choose_frame,height=15,style='Calendar.Treeview')
        
        self.chosenTransTree.config(columns =('soc','lan'))
        self.chosenTransTree.column('soc',width=75,anchor=tk.CENTER)
        self.chosenTransTree.heading('soc',text='Social')
        self.chosenTransTree.column('lan',width=75,anchor=tk.CENTER)
        self.chosenTransTree.heading('lan',text='Language')
        self.chosenTransTree.column('#0',width=150,anchor=tk.CENTER)
        self.chosenTransTree.heading('#0',text='Nickname')
        self.chosenTransTree.pack(side = tk.LEFT)

        #Button confirm
        btConfirm = tk.Button(cent_frame,text="SUBMIT",bg = 'white',
                                command = lambda *args: controller.show_frame(PostPage,True))
        btConfirm.pack(side= tk.BOTTOM)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
    
    def updateView(self):
        self.var.set(0)
        show_choose_trans(self.var,self.choose_frame)
        self.chosenTransTree.delete(*self.chosenTransTree.get_children())
        self.chooseTransTree.delete(*self.chooseTransTree.get_children())
        updateTree(self.chooseTransTree,Task_data['Task']['InstagramPost']['choose_trans'])
        updateTree(self.chooseTransTree,Task_data['Task']['InstagramPost']['choose_trans'])
        updateTree(self.chosenTransTree,Task_data['Task']['InstagramPost']['chosen_trans'])

class PostPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cent_frame = tk.Frame(self, bg='white')
        
        
        global choosePhotoImg
        choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        self.choosePh = tk.Button(cent_frame, image=choosePhotoImg,bd=1,bg="white",command = lambda *args: choosePhoto(self.choosePh))
        self.choosePh.pack(side=tk.TOP,pady=10)
        
        lab_nc1t=tk.Label(cent_frame,text= "This is permanent description field",bg="white",font=LARGE_FONT)
        lab_nc1t.pack(side=tk.TOP,pady=5)
        #At least one of 3 textboxes must be not empty
        #Unchangeble text Field 1 (This text will not be translated)
        self.no_change_1_text = tk.Text(cent_frame,bg='white',bd=1,width =50,height = 2)
        self.no_change_1_text.pack(side=tk.TOP,pady=5)
        

        lab_ct=tk.Label(cent_frame,text= "This is translateble description field",bg="white",font=LARGE_FONT)
        lab_ct.pack(side=tk.TOP,pady=5)
        #Changeble text Field (This text WILL BE translated, if translate option choosen)
        self.change_text = tk.Text(cent_frame,bg='white',bd=1,width =50,height = 10)
        self.change_text.pack(side=tk.TOP,pady=5)

        lab_nc2t=tk.Label(cent_frame,text= "This is permanent description field",bg="white",font=LARGE_FONT)
        lab_nc2t.pack(side=tk.TOP,pady=5)
        #Unchangeble text Field 2 (This text will not be translated)
        self.no_change_2_text = tk.Text(cent_frame,bg='white',bd=1,width =50,height = 2)
        self.no_change_2_text.pack(side=tk.TOP,pady=5)

        submit_btn = tk.Button(cent_frame,bd=1,width = 50,height = 2,bg='#4A148C',fg='#ffb300',activebackground="#ffb300",text = "SUBMIT",
                                    font='Calibri 12 bold',command=lambda : controller.show_frame(StartPage))#, command = lambda *args: sendPost(choosePhotoImg, no_change_1_text.get("1.0",'end-1c'), change_text.get("1.0",'end-1c'), no_change_2_text.get("1.0",'end-1c'),func=None) )
        submit_btn.pack(side=tk.TOP,pady=5)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        
    
    def updateView(self):
        global choosePhotoImg
        choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        self.choosePh.configure(image = choosePhotoImg)
        
        self.no_change_1_text.delete('1.0',tk.END)
        self.change_text.delete('1.0',tk.END)
        self.no_change_2_text.delete('1.0',tk.END)
        
        


class backBut(tk.Button):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Button.__init__(self, master=None, cnf={}, **kw)
