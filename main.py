#UI
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from tkinter import font

#instagram
import instaloader
#from instaloader import Profile
from instagram_private_api import Client, ClientLoginRequiredError
#from instapy_cli import client

#outer libs
from PIL import Image, ImageTk, ImageDraw
from io import BytesIO
import numpy as np
import os, requests, json, pickle


#my files
from FuncFiles import languages, globalVal, funcs
from TFrame    import TasksFrame 





#******************** CONSTANTS *************************
PATH_PROFILE_PICS = "ProfilePicsMin\\"
PATH_SESSIONS_INSTALOADER = "sessions_instaloader\\"

#******************** GlobalVariables *******************
CurrentSocialNetwork = "Instagram"
Accounts={".!frame2.!frame.!button":"Instagram",".!frame2.!frame.!button2":"Facebook",".!frame2.!frame.!button3":"Twitter"}

#General accounts data representation
data_accounts = {}
data_accounts["Instagram"] = []
data_accounts["Facebook"] = []
data_accounts["Twitter"] = []


#PROJECT DIRECTORIES creation if absent###########
if not os.path.exists(PATH_PROFILE_PICS):
    os.makedirs(PATH_PROFILE_PICS)
if not os.path.exists(PATH_SESSIONS_INSTALOADER):
    os.makedirs(PATH_SESSIONS_INSTALOADER)


#******************** FUNCTIONS *******************

#INSTALOADER$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def getSavedAccSessionsInsta():
    global data_accounts
    check_logout = False
    for acc in data_accounts['Instagram']:
        nick = acc['nickname']
        password = acc['password']

        cook = []
        with open(PATH_SESSIONS_INSTALOADER+nick+'.se', "rb") as f:
            cook = pickle.load(f)
            f.close()
        globalVal.accountsInstancesInsta[nick] = Client(nick,password,cookie = cook )
        #check 
        #globalVal.accountsInstancesInsta[nick].presence_status()
        
        #Check on logout
        try:
            globalVal.accountsInstancesInsta[nick].presence_status()
            print(globalVal.accountsInstancesInsta[nick].authenticated_params)
            acc['login'] = True
        except ClientLoginRequiredError:
            acc['login'] = False
            print("Logout occured: "+nick)
            check_logout = True
    
    if check_logout:
        updateAccountsData()
        


    
def getInstaloader(username, password,popup,lan):
    cli = 0
    try:
        cli = Client(username,password)
        print(cli.authenticated_params)
        data = getProfileData(cli)
        addAccount(username,password,lan,data,cli)
        popup.destroy()
        return cli

    #IT doesn't support 2FA TODO: as soon as the library will be updated
    except Exception as ex:
        if str(ex) == 'bad_password':
            tk.messagebox.showerror("Wrong Credentials",'Wrong password.')
        elif str(ex) == 'invalid_user':
            tk.messagebox.showerror("Wrong Credentials",'Wrong username.')
        else:
            tk.messagebox.showerror("Wrong Credentials",'Unknown mistake. \nIt may be 2 factor authenication.\nPlease turn it off and try again.\n'+str(ex))


def getProfileData(cli):
    uid = int(cli.authenticated_params['_uid'])
    user_inf=cli.user_info(uid)


    data = {}
    data['uid'] = uid
    data['nickname'] = user_inf['user']['username']
    data['fullName']=user_inf['user']['full_name']
    data['biography']=user_inf['user']['biography']
    data['imgUrl']=user_inf['user']['profile_pic_url']
    data['cookie'] = PATH_SESSIONS_INSTALOADER+data['nickname']+'.se'
    with open(data['cookie'], "wb") as f:
        pickle.dump(cli.cookie_jar.dump(),f)
    
    return data
        
    
    


#OTHER FUNCS$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#change of leftbar buttons + changing accounts social

def updateTreeView():
    #insertTreeview
    global data_accounts
    #deleting old ite,s
    myTreeView.delete(*myTreeView.get_children())
    #read saved data
    with open('data\\data.json') as json_file:  
        data_accounts = json.load(json_file)
    #insert
    i=0
    
    for p in data_accounts[CurrentSocialNetwork]:
        if CurrentSocialNetwork == 'Instagram':

            
            

            try:
                ima = globalVal.myImg[p['nickname']+p["imgUrl"]]

            except:
                ima = circle_img(Image.open(PATH_PROFILE_PICS+p['nickname']+'.png'))
                #social image
                im2 = Image.open('icons//'+CurrentSocialNetwork+'.png')
                im2 = im2.resize((10,10),Image.ANTIALIAS)
                ima.paste(im2,(22,22))
                globalVal.myImg[p['nickname']+p["imgUrl"]]=ImageTk.PhotoImage(ima)
            
            #if logout occured
            if p['login'] == False:
                myTreeView.insert('', i, "Item"+str(i),tags = ('error',), text = 'NEEDS RELOGIN: '+str(p["nickname"]),image = globalVal.myImg[p['nickname']+p["imgUrl"]])
                myTreeView.tag_configure('error', background='#f9e6e6',foreground='black')
            else:
                myTreeView.insert('', i, "Item"+str(i), text = str(p["nickname"]),image = globalVal.myImg[p['nickname']+p["imgUrl"]])
            
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
    with open('data\\data.json', 'w') as outfile:  
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
def addAccount(name,password,lan,other_data,cli):
    global CurrentSocialNetwork
    isNotSameAcc = True    
    
    for acc in data_accounts[CurrentSocialNetwork]:

        if acc['nickname'] == other_data['nickname']:
            
            acc['password']=password
            acc['language']=lan
            acc['fullName']=other_data['fullName']
            acc['biography']=other_data['biography']
            acc['imgUrl']=other_data['imgUrl']
            acc['cookie']=other_data['cookie']
            acc['login'] = True
            
            #Saving image
            response = requests.get(other_data['imgUrl'])
            ima = Image.open(BytesIO(response.content)) 
            ima = ima.resize((32,32),Image.ANTIALIAS)
            ima.save(PATH_PROFILE_PICS+name+'.png')


            isNotSameAcc=False
            break
    
    if(isNotSameAcc):        
        data_accounts[CurrentSocialNetwork].append({
            'nickname': other_data['nickname'],
            'password': password,
            'language': lan,
            'fullName': other_data['fullName'],
            'biography':other_data['biography'],
            'imgUrl':   other_data['imgUrl'],
            'cookie':   other_data['cookie'],
            'login':    True
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
    passEnt = tk.Entry(popup,bg="#e1e1e1",show="*",width = 22)
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
root.geometry('1000x500')
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
styleTree.configure('Calendar.Treeview',font=ft,rowheight=64)
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
#taskBut = tk.Button(root, width=100,text = "TASK MENU")
#taskBut.pack(fill=tk.X)

# ********************************* TASKS WINDOW ***********************************************

tasks =  TasksFrame.MultipleWindows(root)
tasks.pack(fill=tk.BOTH,expand=tk.YES)

getSavedAccSessionsInsta()#####getting saved accounts
funcs.print(str(data_accounts))
root.mainloop()