import tkinter as tk
from tkinter import ttk
import copy


import instapy_cli
import instagram_private_api

#my files
from FuncFiles import languages 
from FuncFiles import globalVal
from FuncFiles import funcs 

#CONSTANTS
LARGE_FONT = ("Colibri", 12) 
#________________________UI Functions_________________________________


def check_and_go(mydata,func=None):

    if mydata['Instagram']==[] and mydata['Facebook']==[] and mydata['Twitter']==[]:
        tk.messagebox.showerror("Please choose accounts","At least 1 account must be chosen")
        return

    if func != None:
        globalVal.Task_data['Task']['InstagramPost']['choose_trans'] = copy.deepcopy(globalVal.Task_data['Task']['InstagramPost']['chosen_acc'])
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
            funcs.updateTree(chooseTree, globalVal.Task_data['Task']['InstagramPost']['choose_trans'])
            funcs.updateTree(chosenTree, globalVal.Task_data['Task']['InstagramPost']['chosen_trans'])
        except:
            pass

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
        btChoose = tk.Button(button_frame,text = "CHOOSE\nSELECTED",width=13,command = lambda *args: funcs.moveEl(self.chooseTreeView,self.chosenTreeView,globalVal.Task_data['AllAccounts'],globalVal.Task_data['Task']['InstagramPost']['chosen_acc']))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        btChoose = tk.Button(button_frame,text = "UNCHOOSE\nSELECTED",width=13,command = lambda *args: funcs.moveEl(self.chosenTreeView,self.chooseTreeView,globalVal.Task_data['Task']['InstagramPost']['chosen_acc'],globalVal.Task_data['AllAccounts']))
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
                                command = lambda *args: check_and_go(globalVal.Task_data['Task']['InstagramPost']['chosen_acc'],lambda : controller.show_frame(ChooseTranslation,True)))
        btConfirm.pack(side= tk.BOTTOM)

        choose_frame.pack(side = tk.TOP, pady=10)
        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        self.updateView()
        
    def updateView(self):
        self.chosenTreeView.delete(*self.chosenTreeView.get_children())
        self.chooseTreeView.delete(*self.chooseTreeView.get_children())
        funcs.updateTree(self.chooseTreeView,globalVal.Task_data['AllAccounts'])
        funcs.updateTree(self.chosenTreeView,globalVal.Task_data['Task']['InstagramPost']['chosen_acc'])

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
        self.chooseTransTree = ttk.Treeview(self.choose_frame,height=10,style='Calendar.Treeview')
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
        btChoose = tk.Button(button_frame,text = "CHOOSE\nSELECTED",width=13,command = lambda *args: funcs.moveEl(self.chooseTransTree,self.chosenTransTree,globalVal.Task_data['Task']['InstagramPost']['choose_trans'],globalVal.Task_data['Task']['InstagramPost']['chosen_trans']))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        btChoose = tk.Button(button_frame,text = "UNCHOOSE\nSELECTED",width=13,command = lambda *args: funcs.moveEl(self.chosenTransTree,self.chooseTransTree,globalVal.Task_data['Task']['InstagramPost']['chosen_trans'],globalVal.Task_data['Task']['InstagramPost']['choose_trans']))
        btChoose.pack(side=tk.TOP,pady=10,padx=10)
        button_frame.pack(side = tk.LEFT,fill="both", expand=True,pady=20)


        ## TreeView with chosen objects
        self.chosenTransTree = ttk.Treeview(self.choose_frame,height=10,style='Calendar.Treeview')
        
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
        funcs.updateTree(self.chooseTransTree,globalVal.Task_data['Task']['InstagramPost']['choose_trans'])
        funcs.updateTree(self.chooseTransTree,globalVal.Task_data['Task']['InstagramPost']['choose_trans'])
        funcs.updateTree(self.chosenTransTree,globalVal.Task_data['Task']['InstagramPost']['chosen_trans'])

class PostPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cent_frame = tk.Frame(self, bg='white')
        
        

        globalVal.choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        self.choosePh = tk.Button(cent_frame, image=globalVal.choosePhotoImg,bd=1,bg="white",command = lambda *args: funcs.choosePhoto(self.choosePh))
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
                                    font='Calibri 12 bold',command=lambda : controller.show_frame(None,False,True))#, command = lambda *args: sendPost(globalVal.choosePhotoImg, no_change_1_text.get("1.0",'end-1c'), change_text.get("1.0",'end-1c'), no_change_2_text.get("1.0",'end-1c'),func=None) )
        submit_btn.pack(side=tk.TOP,pady=5)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        
    
    def updateView(self):

        globalVal.choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        self.choosePh.configure(image = globalVal.choosePhotoImg)
        
        self.no_change_1_text.delete('1.0',tk.END)
        self.change_text.delete('1.0',tk.END)
        self.no_change_2_text.delete('1.0',tk.END)
        
        

