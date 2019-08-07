import tkinter as tk
from tkinter import ttk
import copy



import instapy_cli
from instagram_private_api import Client,MediaRatios
from instagram_private_api_extensions import media

import pickle

#my files
from FuncFiles import languages, globalVal, funcs 
from TFrame.Task import Task

#CONSTANTS
LARGE_FONT = ("Colibri", 12) 
#________________________UI Functions_________________________________


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
        #Choose on double click
        self.chooseTreeView.bind('<Double-1>',lambda *args: funcs.moveEl(self.chooseTreeView,self.chosenTreeView,globalVal.Task_data['AllAccounts'],globalVal.Task_data['Task']['InstagramPost']['chosen_acc']))
        
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
        self.chosenTreeView.bind('<Double-1>',lambda *args: funcs.moveEl(self.chosenTreeView,self.chooseTreeView,globalVal.Task_data['Task']['InstagramPost']['chosen_acc'],globalVal.Task_data['AllAccounts']))
        

        #Button confirm
        btConfirm = tk.Button(cent_frame,text="SUBMIT",bg = 'white',
                                command = lambda *args: self.check_and_go(globalVal.Task_data['Task']['InstagramPost']['chosen_acc'],lambda : controller.show_frame(ChooseTranslation,True)))
        btConfirm.pack(side= tk.BOTTOM)

        choose_frame.pack(side = tk.TOP, pady=10)
        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        self.updateView()
    
    def check_and_go(self,mydata,func=None):

        if mydata['Instagram']==[] and mydata['Facebook']==[] and mydata['Twitter']==[]:
            tk.messagebox.showerror("Please choose accounts","At least 1 account must be chosen")
            return

        if func != None:
            globalVal.Task_data['Task']['InstagramPost']['choose_trans'] = copy.deepcopy(globalVal.Task_data['Task']['InstagramPost']['chosen_acc'])
            func()
        
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

        radio_not_trans = tk.Radiobutton(cent_frame,text="Not translate (keep the description \nof the post in the same language for all accounts)",
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
        #Choose by double click
        self.chooseTransTree.bind('<Double-1>',lambda *args: funcs.moveEl(self.chooseTransTree,self.chosenTransTree,globalVal.Task_data['Task']['InstagramPost']['choose_trans'],globalVal.Task_data['Task']['InstagramPost']['chosen_trans']))
        
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
        #Unchoose by double click
        self.chosenTransTree.bind('<Double-1>',lambda *args: funcs.moveEl(self.chosenTransTree,self.chooseTransTree,globalVal.Task_data['Task']['InstagramPost']['chosen_trans'],globalVal.Task_data['Task']['InstagramPost']['choose_trans']))

        #Button confirm
        btConfirm = tk.Button(cent_frame,text="SUBMIT",bg = 'white',
                                command = lambda *args: self.save_and_move(controller))
        btConfirm.pack(side= tk.BOTTOM)

        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

    def save_and_move(self,controller):

        if self.var.get() == 0:
            #description will be in original language
            globalVal.Task_data['Task']['InstagramPost']['chosen_trans'] = {'Instagram':[],'Facebook':[],'Twitter':[]}
            globalVal.Task_data['Task']['InstagramPost']['choose_trans'] = copy.deepcopy(globalVal.Task_data['Task']['InstagramPost']['chosen_acc'])
        
        elif self.var.get() == 1:
            #will be translated to each acc lang
            globalVal.Task_data['Task']['InstagramPost']['chosen_trans'] = copy.deepcopy(globalVal.Task_data['Task']['InstagramPost']['chosen_acc'])
            globalVal.Task_data['Task']['InstagramPost']['choose_trans'] = {'Instagram':[],'Facebook':[],'Twitter':[]}
        
        else:
            # all translated and not translated accs are chosen during the process (option 3)
            pass

        controller.show_frame(PostPage,True)

    
    def updateView(self):
        self.var.set(0)
        show_choose_trans(self.var,self.choose_frame)
        self.chosenTransTree.delete(*self.chosenTransTree.get_children())
        self.chooseTransTree.delete(*self.chooseTransTree.get_children())
        funcs.updateTree(self.chooseTransTree,globalVal.Task_data['Task']['InstagramPost']['choose_trans'])
        #funcs.updateTree(self.chooseTransTree,globalVal.Task_data['Task']['InstagramPost']['choose_trans'])
        funcs.updateTree(self.chosenTransTree,globalVal.Task_data['Task']['InstagramPost']['chosen_trans'])






class PostPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cent_frame = tk.Frame(self, bg='white')
        
        

        globalVal.choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        
        self.choosePh = tk.Button(cent_frame, image=globalVal.choosePhotoImg,bd=1,bg="white",command = lambda *args: funcs.choosePhoto(self.choosePh))
        self.choosePh.pack(side=tk.LEFT,pady=10)
        
        #_Frame just to keep place between buttons and image after pack/unpack actions
        self.keep_place_frame = tk.Frame(cent_frame,bg = 'white') 
        
        #__Frame to be hidden on preview
        self.desc_frame = tk.Frame(self.keep_place_frame,bg = 'white')
        


        #TODO:location
        self.chosen_location = None
        self.lab_loc=tk.Label(self.desc_frame,text= "This is Location field, (double click to choose)",bg="white",font=LARGE_FONT)
        self.lab_loc.pack(side=tk.TOP,pady=5)
        
        self.loc_find_frame = tk.Frame(self.desc_frame,bg='white')
        self.locate = tk.Entry(self.loc_find_frame)
        self.locate.pack(side = tk.LEFT)
        self.locate_btn = tk.Button(self.loc_find_frame, text = "FIND",command=self.loc)
        self.locate_btn.pack(side = tk.LEFT,padx=15)
        self.loc_find_frame.pack()

        self.loc_hid_frame = tk.Frame(self.desc_frame,bg='white')
        self.loc_hid_frame.pack()
        #__preview results
        self.loc_tree = ttk.Treeview(self.loc_hid_frame,height=5)

        self.loc_tree.config(columns =('position','id'))
        self.loc_tree.column('position',width=125,anchor=tk.CENTER)
        self.loc_tree.heading('position',text='Position')
        self.loc_tree.column('id',width=125,anchor=tk.CENTER)
        self.loc_tree.heading('id',text='ID')
        self.loc_tree.column('#0',width=150,anchor=tk.CENTER)
        self.loc_tree.heading('#0',text='Title')
        self.loc_tree.bind('<Double-1>',self.choose_loc)
        #self.loc_tree.pack()
        #TODO:location end


        self.lab_nc1t=tk.Label(self.desc_frame,text= "This is permanent description field",bg="white",font=LARGE_FONT)
        self.lab_nc1t.pack(side=tk.TOP,pady=5)
      
        #____At least one of 3 textboxes must be not empty
        #____Unchangeble text Field 1 (This text will not be translated)
        self.no_change_1_text = tk.Text(self.desc_frame,bg='white',bd=1,width =50,height = 2)
        self.no_change_1_text.pack(side=tk.TOP,pady=5)

        self.lab_ct=tk.Label(self.desc_frame,text= "This is translateble description field",bg="white",font=LARGE_FONT)
        self.lab_ct.pack(side=tk.TOP,pady=5)
        #____Changeble text Field (This text WILL BE translated, if translate option choosen)
        self.change_text = tk.Text(self.desc_frame,bg='white',bd=1,width =50,height = 3)
        self.change_text.pack(side=tk.TOP,pady=5)

        self.lab_nc2t=tk.Label(self.desc_frame,text= "This is permanent description field",bg="white",font=LARGE_FONT)
        self.lab_nc2t.pack(side=tk.TOP,pady=5)
        #____Unchangeble text Field 2 (This text will not be translated)
        self.no_change_2_text = tk.Text(self.desc_frame,bg='white',bd=1,width =50,height = 2)
        self.no_change_2_text.pack(side=tk.TOP,pady=5)

        self.desc_frame.pack(side = tk.TOP)
        
        #__Preview Lable
        self.prev_text = tk.Label(self.keep_place_frame,bg="white")

        self.keep_place_frame.pack(side= tk.TOP)


        
        self.prev_text_btn = tk.Button(cent_frame,bd=1,width = 30,height = 2,bg='#4A148C',fg='#ffb300',activebackground="#ffb300",text = "Preview Description",
                                    font='Calibri 12 bold',command = lambda : self.previewTask())
        self.prev_text_btn.pack(side = tk.TOP)

        final_btns = tk.Frame(cent_frame)

        submit_btn = tk.Button(final_btns,bd=1,width = 30,height = 2,bg='#4A148C',fg='#ffb300',activebackground="#ffb300",text = "PUBLISH NOW",
                                    font='Calibri 12 bold',command = lambda : self.implementTask(controller))
        submit_btn.pack(side=tk.LEFT)

        sched_btn = tk.Button(final_btns,bd=1,width = 30,height = 2,bg='#4A148C',fg='#ffb300',activebackground="#ffb300",text = "SCHEDULE TASK",
                                    font='Calibri 12 bold')
        sched_btn.pack(side=tk.LEFT,padx=10)
        
        final_btns.pack(side=tk.TOP,pady=5)
        cent_frame.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        

    def previewTask(self):
        if self.desc_frame.winfo_ismapped():
            self.prev_text_btn.configure(text = 'Change Description')
            
            
            loc = 'Not chosen\n'
            if self.chosen_location != None:
                loc = self.chosen_location['text'] + "\n"
            #show preview
            self.prev_text.configure(text = 'location: ' + loc + self.no_change_1_text.get('1.0',tk.END)[:-1]+self.change_text.get('1.0',tk.END)[:-1]+self.no_change_2_text.get('1.0',tk.END)[:-1]) 
            self.prev_text.pack(side = tk.TOP)
            #hide description field
            self.desc_frame.pack_forget()
        else:
            self.prev_text_btn.configure(text = 'Preview Description')
            self.prev_text.pack_forget()
            self.desc_frame.pack(side = tk.TOP)
    
    
    
    
    def implementTask(self,controller):

        answer = tk.messagebox.askquestion('','Are you shure about publishing?')
        if answer == 'yes':   
            
            #each field automatically ads the '\n' in the end - manual remove 
            not_translate_text1 = self.no_change_1_text.get('1.0',tk.END)[:-1]
            translate_text = self.change_text.get('1.0',tk.END)[:-1]
            not_translate_text2 = self.no_change_2_text.get('1.0',tk.END)[:-1]
            
            #because of missing last '\n' after translation, we need to add it manually
            x = ''
            print("\nSYMBOL: " + translate_text[-1:] )
            if translate_text[-1:] == '\n':
                x = '\n'
            


            print("\nTRANSLATED ACCOUNTS Insta:")
            for acc in globalVal.Task_data['Task']['InstagramPost']['chosen_trans']['Instagram']:
                
                acc['postText']= not_translate_text1 + languages.translate(translate_text,acc['language']) + x + not_translate_text2
                funcs.print("\n"+acc['nickname']+"  lan: "+acc['language']+"  text = "+acc['postText'])

            print("\nNOT TRANSLATED ACCOUNTS Insta:")
            for acc in globalVal.Task_data['Task']['InstagramPost']['choose_trans']['Instagram']:
                acc['postText'] = not_translate_text1 + translate_text + not_translate_text2 
                funcs.print("\n"+acc['nickname']+"  lan: "+acc['language']+"  text = "+acc['postText'])
            
            try:
                im_path = globalVal.Task_data['Task']['photo_path']
                if im_path == '':
                    raise Exception                
            except:
                tk.messagebox.showerror('No image chosen', 'Please choose an image in order to make an Instagram post')
                return

            loc = None
            try:
                #choosing location
                loc = globalVal.accountsInstancesInsta[globalVal.Task_data['Task']['InstagramPost']['chosen_trans']['Instagram'][0]['nickname']].location_info(self.chosen_location['id'])['location']
                # the bug in the instagram private api -> next line fixes it
                loc['address'] = loc['lat']
            except:
                #no location
                loc = None
            
            #Publishing with translation    
            for acc in globalVal.Task_data['Task']['InstagramPost']['chosen_trans']['Instagram']:
                photo_data, photo_size = media.prepare_image(im_path, aspect_ratios=MediaRatios.standard)
                globalVal.accountsInstancesInsta[acc['nickname']].post_photo(photo_data, photo_size, acc['postText'],location = loc)#POSTING FUNCTION
                #Client.locat

            #Publishing without translation
            for acc in globalVal.Task_data['Task']['InstagramPost']['choose_trans']['Instagram']:
                photo_data, photo_size = media.prepare_image(im_path, aspect_ratios=MediaRatios.standard)
                globalVal.accountsInstancesInsta[acc['nickname']].post_photo(photo_data, photo_size, acc['postText'],location = loc)#POSTING FUNCTION

            
            #go to the first page
            controller.show_frame(None,False,True)
    

    #TODO: Settle locations
    def loc(self):
        if self.locate_btn['text'] == 'FIND':
            self.loc_tree.pack(fill='x')
            uuid = globalVal.accountsInstancesInsta[globalVal.Task_data['Task']['InstagramPost']['chosen_trans']['Instagram'][0]['nickname']].generate_uuid()
            self.locs = globalVal.accountsInstancesInsta[globalVal.Task_data['Task']['InstagramPost']['chosen_trans']['Instagram'][0]['nickname']].location_fb_search(self.locate.get(),uuid)

            self.loc_tree.delete(*self.loc_tree.get_children())

            iter = 0
            for i in self.locs['items']:
                self.loc_tree.insert('',iter, "Item"+str(iter),text = str(i['title']))
                self.loc_tree.set("Item"+str(iter),'position',str(i['location']['lng']) + ', ' + str(i['location']['lat']))
                self.loc_tree.set("Item"+str(iter),'id',str(i['location']['facebook_places_id']))
                
                iter = iter + 1
        else:
            self.chosen_location = None
            self.locate_btn.configure(text = 'FIND')
            self.locate.delete(0,tk.END)
            self.locate.configure(fg = 'black',state = tk.NORMAL)  
            self.loc_tree.delete(*self.loc_tree.get_children())          
            

    def choose_loc(self,event):
        try:
            item = self.loc_tree.selection()[0]
        except IndexError:
            return

        if self.loc_tree.item(item,"text") != '':
            
            text = str(self.loc_tree.item(item,"text"))
            print(text +'\n')
            self.locate.delete(0,tk.END)
            self.locate.insert(0,text)
            
            self.chosen_location = {'text':text, 'id':self.loc_tree.item(item,"values")[1]}
            self.locate.configure(fg = 'green',state = 'readonly')
            
            self.locate_btn.configure(text = "RESET")
            self.loc_tree.pack_forget()

            
            
            
        
        
        
    
    def updateView(self):

        globalVal.choosePhotoImg = tk.PhotoImage(file='icons\\choosephoto.png')
        self.choosePh.configure(image = globalVal.choosePhotoImg)
        
        self.prev_text_btn.configure(text = 'Preview Description')
        self.prev_text.pack_forget()
        self.desc_frame.pack(side = tk.TOP)

        self.no_change_1_text.delete('1.0',tk.END)
        self.change_text.delete('1.0',tk.END)
        self.no_change_2_text.delete('1.0',tk.END)

        self.chosen_location = None
        self.locate_btn.configure(text = 'FIND')
        self.locate.delete(0,tk.END)
        self.locate.configure(fg = 'black',state = tk.NORMAL)    
        self.loc_tree.delete(*self.loc_tree.get_children()) 


        

