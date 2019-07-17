#UI
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import font

#instagram
import instaloader
from instaloader import Profile

#outer libs
from PIL import Image, ImageTk, ImageDraw
from io import BytesIO
import numpy as np
import os
import requests
import json


#my files
import languages 
import TasksFrame  




#******************** CONSTANTS *************************
PATH_PROFILE_PICS = "ProfilePicsMin\\"
PATH_SESSIONS_INSTAGRAM = "sessions\\"

#******************** GlobalVariables *******************
CurrentSocialNetwork = "Instagram"
Accounts={".!frame2.!frame.!button":"Instagram",".!frame2.!frame.!button2":"Facebook",".!frame2.!frame.!button3":"Twitter"}

#here will be saved opened from file sessions Instagram 
accountsInstancesInsta={}

#General accounts data representation
data_accounts = {}
data_accounts["Instagram"] = []
data_accounts["Facebook"] = []
data_accounts["Twitter"] = []

global myImg
myImg = {}




#PROJECT DIRECTORIES creation if absent###########
if not os.path.exists(PATH_PROFILE_PICS):
    os.makedirs(PATH_PROFILE_PICS)
if not os.path.exists(PATH_SESSIONS_INSTAGRAM):
    os.makedirs(PATH_SESSIONS_INSTAGRAM)


#******************** FUNCTIONS *******************

#INSTALOADER$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def getSavedAccSessionsInsta():
    global accountsInstancesInsta
    for acc in data_accounts['Instagram']:
        nick = acc['nickname']
        session = acc['session']
        accountsInstancesInsta[nick] = instaloader.Instaloader()
        accountsInstancesInsta[nick].load_session_from_file(nick,session)
        #print(accountsInstancesInsta[nick].test_login())
        
def submit2FA(L,code,nick,password,lan,popup,popup2):
    try:
        L.two_factor_login(code.get())
        
        if L.test_login()!=None:
            data = getProfileData(L,nick)#Not needed now
            addAccount(nick,password,lan,data,L)
            
            popup.destroy()
            popup2.destroy()

    except Exception as e:
        print(str(e))
        tk.messagebox.showerror("Wrong Credentials",str(e))
    
    
def getInstaloader(username, password,popup,lan):
    L = instaloader.Instaloader()
    try:
        L.login(username,password)
        
        if L.test_login()!=None:
            data = getProfileData(L,username)
            addAccount(username,password,lan,data,L)
            popup.destroy()
            return L

    except instaloader.TwoFactorAuthRequiredException as a:
        popup2=tk.Toplevel(popup)
        popup2.transient(popup)
        popup2.configure(background="white")
        popup2.title("Follow instruction")
        popup2.geometry("340x120")
        popup2.resizable(0, 0)
        
        #info about 2FA
        mes = tk.Label(popup2, text=str(a),bg="#f9f8e2")
        mes.grid(row=0,column=1,columnspan=4,pady=7,padx=0)
        f = font.Font(mes, mes.cget("font"))
        f.configure(underline = True)
        mes.configure(font=f)

        #enter code
        codeL = tk.Label(popup2, text="2FA code:",width = 13,anchor ='w')
        codeL.grid(row=1,column=1)
        code = tk.Entry(popup2,bg="#e1e1e1",width = 22)
        code.grid(row=1,column=2,columnspan=3)

        #submit
        ButConfirm = tk.Button(popup2,text="Submit",width=10,bg="white",command=lambda *args: submit2FA(L,code,username,password,lan,popup,popup2))
        ButConfirm.grid(row=2,column=3,sticky=tk.N)
        

    except Exception as e:
        print(str(e))
        tk.messagebox.showerror("Wrong Credentials",str(e))

def getProfileData(loginInstance,nickname):
    data = {}
    profile = Profile.from_username(loginInstance.context, nickname)
    data['fullName']=profile.full_name
    data['biography']=profile.biography
    data['imgUrl']=profile.profile_pic_url
    
    return data
        
    
    


#OTHER FUNCS$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#change of leftbar buttons + changing accounts social

def updateTreeView():
    #insertTreeview
    global data_accounts
    #deleting old ite,s
    myTreeView.delete(*myTreeView.get_children())
    #read saved data
    with open('data.json') as json_file:  
        data_accounts = json.load(json_file)
    #insert
    i=0
    
    for p in data_accounts[CurrentSocialNetwork]:
        if CurrentSocialNetwork == 'Instagram':
            
            global myImg
            #ima = Image.open(PATH_PROFILE_PICS+p['nickname']+'.png')            
            ima = circle_img(Image.open(PATH_PROFILE_PICS+p['nickname']+'.png'))
            myImg[p["imgUrl"]]=ImageTk.PhotoImage(ima)
            
            
            myTreeView.insert('', i, "Item"+str(i), text = str(p["nickname"]),image = myImg[p["imgUrl"]])
            myTreeView.set("Item"+str(i),'lan',languages.LANGTOCODES[p['language']])
            #myTreeView.insert("Item"+str(i), 3, str(i)+"ElSubItem"+str(3), text = str(p["password"]))
            try:
                myTreeView.insert("Item"+str(i), 0, str(i)+"ElSubItem"+str(0), text = str(p["fullName"]))
            except:
                pass
            try:
                myTreeView.insert("Item"+str(i), 1, str(i)+"ElSubItem"+str(1), text = str(p["biography"]))
            except:
                pass
            #myTreeView.insert("Item"+str(i), 2, str(i)+"ElSubItem"+str(2), text = str(p["imgUrl"]))
        i+=1
   
def updateAccountsData():
    with open('data.json', 'w') as outfile:  
        json.dump(data_accounts, outfile)
        
#Buttons Funcs############################
def chooseSocial(button):
    global CurrentSocialNetwork
    but_1.configure(bg="#4A148C")
    but_2.configure(bg="#4A148C")
    but_3.configure(bg="#4A148C")
    button.configure(bg="white")
    CurrentSocialNetwork = Accounts[str(button)]
    topLable.configure(text=CurrentSocialNetwork+" accounts")
    updateTreeView()

def deleteAll():
    global CurrentSocialNetwork
    answer = tk.messagebox.askokcancel("WARNING","YOU ARE TRYING TO DELETE ALL THE ACCOUNTS DATA\nAre you sure?",parent=root)
    if answer==True:
        data_accounts[CurrentSocialNetwork]=[]
        updateAccountsData()
        updateTreeView()

def deleteSelected():
    global CurrentSocialNetwork
    curItems = myTreeView.selection()    
    answer = tk.messagebox.askokcancel("WARNING","Would you like to delete selected data?",parent=root)
    if answer==True:
        #Comparing Selected Items with Items in the datafile and removing selected
        for delEl in curItems:

            for el in data_accounts[CurrentSocialNetwork]:

                if(el['nickname'] == myTreeView.item(delEl)['text']):

                    data_accounts[CurrentSocialNetwork].remove(el)
        
        updateAccountsData()
        updateTreeView()
    
def selectAll():
    children = myTreeView.get_children() 
    myTreeView.selection_set(children)

def removeSelection():
    children = myTreeView.get_children() 
    myTreeView.selection_toggle(children)
    myTreeView.selection_remove(children)

def compareStrings(a,b):
    a = a.toLowerCase()
    b = b.toLowerCase()

    if(a<b):
        return -1
    elif(a>b):
        return 1
    else:
        return 0

def sortAccounts():
    global CurrentSocialNetwork
    if data_accounts[CurrentSocialNetwork] != sorted(data_accounts[CurrentSocialNetwork], key = lambda i: i['nickname']):
        data_accounts[CurrentSocialNetwork] = sorted(data_accounts[CurrentSocialNetwork], key = lambda i: i['nickname'])
    else:
        data_accounts[CurrentSocialNetwork] = sorted(data_accounts[CurrentSocialNetwork], key = lambda i: i['nickname'],reverse=True)
    updateAccountsData()
    updateTreeView()


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

#promt user to enter nickname and password to the account
def addAccount(name,password,lan,other_data,loginInstance):
    global CurrentSocialNetwork
    isNotSameAcc = True
    for acc in data_accounts[CurrentSocialNetwork]:
        if acc['nickname'] == name:
            loginInstance.save_session_to_file(PATH_SESSIONS_INSTAGRAM+name+'.se')
            acc['password']=password
            acc['language']=lan
            acc['fullName']=other_data['fullName']
            acc['biography']=other_data['biography']
            acc['imgUrl']=other_data['imgUrl']
            acc['session']=PATH_SESSIONS_INSTAGRAM+name+'.se'
            
            #Saving image
            response = requests.get(other_data['imgUrl'])
            ima = Image.open(BytesIO(response.content)) 
            ima = ima.resize((32,32),Image.ANTIALIAS)
            ima.save(PATH_PROFILE_PICS+name+'.png')


            isNotSameAcc=False
            break
    
    if(isNotSameAcc):
        loginInstance.save_session_to_file(PATH_SESSIONS_INSTAGRAM+name+'.se')
        data_accounts[CurrentSocialNetwork].append({
            'nickname':name,
            'password':password,
            'language':lan,
            'fullName':other_data['fullName'],
            'biography':other_data['biography'],
            'imgUrl': other_data['imgUrl'],
            'session': PATH_SESSIONS_INSTAGRAM+name+'.se'
        })

        #Saving image locally
        response = requests.get(other_data['imgUrl'])
        ima = Image.open(BytesIO(response.content)) 
        ima = ima.resize((32,32),Image.ANTIALIAS)
        ima.save(PATH_PROFILE_PICS+name+'.png')

    updateAccountsData()
    updateTreeView()

def createAccount(nickEnt,passwordEnt,var,popup):
    snick = nickEnt.get()
    spass=passwordEnt.get()
    slan=var.get()
    
    if snick == '' or spass == '' or slan=='Untilted':
        tk.messagebox.showinfo("All data fields must be entered", "Please check all the fields",parent=popup)
        return
    #checking the credentials and getting login instance
    getInstaloader(snick,spass,popup,slan)
    
    
#OTHER (CUSTOM) WINDOWS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def addAccountPopUp():
    popup=tk.Toplevel(root)
    popup.transient(root)
    popup.configure(background="white")
    popup.title("Enter this data to create the account")
    popup.geometry("380x170")
    popup.resizable(0, 0)
    
    #Begining
    mes = tk.Label(popup, text="by entering already existing Nickname in the system, \nyou will update it's account data (such as img, language, etc)",bg="#f9f8e2")
    mes.grid(row=0,column=1,columnspan=4,pady=7,padx=0)
    f = font.Font(mes, mes.cget("font"))
    f.configure(underline = True)
    mes.configure(font=f)
    
    #Center
    qNick = tk.Label(popup, text="?",bg="white")
    qNick.grid(row=1,column=0)
    qNick.configure(font=f)
    nick = tk.Label(popup, text="Nickname:",width = 13,anchor ='w',bg="white")
    nick.grid(row=1,column=1)
    nickEnt = tk.Entry(popup,bg="#e1e1e1",width = 22)
    nickEnt.grid(row=1,column=2,columnspan=3)

    qPassword = tk.Label(popup, text="?",pady=4,bg="white")
    qPassword.configure(font=f)
    qPassword.grid(row=2,column=0)
    password = tk.Label(popup, text="Password:",width = 13,anchor ='w',bg="white")
    password.grid(row=2,column=1)
    passEnt = tk.Entry(popup,bg="#e1e1e1",width = 22)
    passEnt.grid(row=2,column=2,columnspan=3)

    qLan = tk.Label(popup, text="?",pady=4,width = 4,bg="white")
    qLan.configure(font=f)
    qLan.grid(row=3,column=0)
    lan = tk.Label(popup, text="Language:",width = 13,anchor ='w',bg="white")
    lan.grid(row=3,column=1)
    var = tk.StringVar(popup)
    var.set("Untilted")
    lanEnt = tk.OptionMenu(popup,var,"Untilted",*languages.CODESTOLANG.values())
    lanEnt.configure(font=('calibri',(10)),width = 13,background="#e1e1e1",relief=tk.GROOVE)
    lanEnt['menu'].config(font=('calibri',(10)), bg='white')
    lanEnt.grid(row=3,column=2,columnspan=3)

    #Bottom
    popupButConfirm = tk.Button(popup,text="Confirm",width=10,bg="white",command=lambda *args: createAccount(nickEnt,passEnt,var,popup))
    popupButConfirm.grid(row=4,column=1,pady=8,sticky=tk.N)
    popupButCancel = tk.Button(popup,text="Cancel",width=10,bg="white",command = popup.destroy)
    popupButCancel.grid(row=4,column=3)

#UI %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#************root****************
root = tk.Tk()
root.configure(background = "white")
root.title("Social Managment Tool")
# ********** Sub Menus **********
menu = tk.Menu(root)
root.config(menu=menu)

subMenu = tk.Menu(menu)
menu.add_cascade(label = "Settings", menu = subMenu)
subMenu.add_command(label = "SubItem 1")
subMenu.add_command(label = "SubItem 2")
subMenu.add_command(label = "SubItem 3")
subMenu.add_command(label = "SubItem 4")

subsubMenu = tk.Menu(subMenu)
subMenu.add_cascade(label = "SubSubMenu",menu = subsubMenu)
subsubMenu.add_command(label = "subsub 1")
subsubMenu.add_command(label = "subsub 2")
subsubMenu.add_command(label = "subsub 3")


##################################################### HERE IT STARTS #############

#***************** Main Frames ******************
statusbar_frame = tk.Frame(root)
statusbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

left_frame = tk.Frame(root, bg="white")
left_frame.pack(side=tk.LEFT, fill=tk.Y)

toolbar_frame = tk.Frame(left_frame, bg="#4A148C")
toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)




# ********** Toolbar **********
#setteling images
im = Image.open('icons//instagram.png')
#im.resize((32,32)).save('instagram.png')
insta = ImageTk.PhotoImage(im)

im = Image.open('icons//facebook.png')
#im.resize((32,32)).save('facebook.png')
face = ImageTk.PhotoImage(im)

im = Image.open('icons//twitter.png')
#im.resize((32,32)).save('twitter.png')
twit = ImageTk.PhotoImage(im)


but_1 = tk.Button(toolbar_frame,relief=tk.RAISED,command=lambda *args: chooseSocial(but_1), width=65,height=65,bg="white", bd=0,image = insta)
but_1.pack(side=tk.TOP, padx=0,pady=0,fill=tk.X)
but_2 = tk.Button(toolbar_frame,bg="#4A148C", command=lambda *args: chooseSocial(but_2), width=65,height=65, bd=0,image = face)
but_2.pack(side=tk.TOP, padx=0,pady=0,fill=tk.X)
but_3 = tk.Button(toolbar_frame,bg="#4A148C",command=lambda *args: chooseSocial(but_3), width=65,height=65, bd=0,image = twit)
but_3.pack(side=tk.TOP, padx=0,pady=0,fill=tk.X)



#**********Left workplace************
topFrame = tk.Frame(left_frame,bg="white",bd=0)
topFrame.pack(side=tk.TOP,fill = tk.X)

topBut1 = tk.Button(topFrame, width=10, text = "Sort",bd=1,bg="white",command=sortAccounts)
topBut1.pack(side=tk.RIGHT)
topBut2 = tk.Button(topFrame, width=10, text = "Deselect all",bd=1,bg="white",command=removeSelection)
topBut2.pack(side=tk.RIGHT)
topBut3 = tk.Button(topFrame, width=10, text = "Select all",bd=1,bg="white",command=selectAll)
topBut3.pack(side=tk.RIGHT)

topLable = tk.Label(topFrame,text="Instagram accounts",padx=10,bg="white",bd=1,width=20)
topLable.pack(side=tk.LEFT)

#$$$$$$$$$$$$$$$$$ ACCOUNTS MIDDLE PLATFORM $$$$$$$$$$$$$$$$$$$$$$$$

ft = font.Font(family='Colibri',size=10)
styleTree = ttk.Style()
styleTree.configure('Calendar.Treeview',font=ft,rowheight=33)
myTreeView = ttk.Treeview(left_frame,height=10,style='Calendar.Treeview')

myTreeView.pack(fill="both", expand=True)
myTreeView.config(columns =('lan'))
myTreeView.column('lan',width=50,anchor=tk.CENTER)
myTreeView.heading('#0',text='Nickname')
myTreeView.heading('lan',text='Language')
#preview images
#myTreeView.bind("<Double-1>", OnClickTreeview)   NOT NEEEDED


updateTreeView()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
downFrame = tk.Frame(left_frame,bg="white")
downFrame.pack(side=tk.BOTTOM,fill = tk.X)


botBut0 = tk.Button(downFrame, width=10, text = "Delete all",bd=1,bg="white",command=deleteAll)
botBut0.pack(side=tk.RIGHT)
botBut1 = tk.Button(downFrame, width=15, text = "Delete selected",bd=1,bg="white",command=deleteSelected)
botBut1.pack(side=tk.RIGHT)
botBut2 = tk.Button(downFrame, width=10, text = "Add",bd=1,bg="white",command=addAccountPopUp)
botBut2.pack(side=tk.RIGHT)


# ********** Status Bar **********
status = tk.Label(statusbar_frame,text = "Preparing to do it...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side = tk.BOTTOM,fill=tk.X)



#****************Right Workplace****************
taskBut = tk.Button(root, width=100,text = "TASK MENU")
taskBut.pack(fill=tk.X)

# ********************************* TASKS WINDOW ***********************************************
tasks =  TasksFrame.MultipleWindows(root)
tasks.pack(fill=tk.BOTH,expand=tk.YES)

getSavedAccSessionsInsta()#####getting saved accounts
root.mainloop()