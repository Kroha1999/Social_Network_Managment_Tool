import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import json

root = tk.Tk()
root.configure(background = "white")
root.title("Social Managment Tool")

#******************** GlobalVariables *******************
CurrentSocialNetwork = "Instagram"
Accounts={".!frame2.!frame.!button":"Instagram",".!frame2.!frame.!button2":"Facebook",".!frame2.!frame.!button3":"Twitter"}

data_accounts = {}
data_accounts["Instagram"] = []
data_accounts["Facebook"] = []
data_accounts["Twitter"] = []

#******************** FUNCTIONS *******************
#change of leftbar buttons + changing accounts social
def chooseSocial(button):
    global CurrentSocialNetwork
    but_1.configure(bg="#68217a")
    but_2.configure(bg="#68217a")
    but_3.configure(bg="#68217a")
    button.configure(bg="white")
    CurrentSocialNetwork = Accounts[str(button)]
    topLable.configure(text=CurrentSocialNetwork+" accounts")
    updateTreeView()

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
        myTreeView.insert('', i, "Item"+str(i), text = str(p["nickname"]))
        myTreeView.insert("Item"+str(i), 0, str(i)+"ElSubItem"+str(0), text = str(p["password"]))
        i+=1
        
def deleteAll():
    global CurrentSocialNetwork
    data_accounts[CurrentSocialNetwork]=[]
    answer = tk.messagebox.askokcancel("WARNING","YOU ARE TRYING TO DELETE ALL THE ACCOUNTS DATA\nAre you sure?",parent=root)
    if answer==True:
        with open('data.json', 'w') as outfile:  
            json.dump(data_accounts, outfile)
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
        
        with open('data.json', 'w') as outfile:  
            json.dump(data_accounts, outfile)
        updateTreeView()
        


#promt user to enter nickname and password to the account
def addAccount():
    global CurrentSocialNetwork
    if CurrentSocialNetwork == "Instagram":
        
        answer_name = simpledialog.askstring("Authenication Data", "Add Nickname",parent=root)
        if answer_name is not None and answer_name!="":

            answer_pass = simpledialog.askstring("Authenication Data", "Add Password",parent=root)
            if answer_pass is not None and answer_pass!="":

                global data_accounts
                data_accounts[CurrentSocialNetwork].append({
                    'nickname':answer_name,
                    'password':answer_pass
                })
                with open('data.json', 'w') as outfile:  
                    json.dump(data_accounts, outfile)
                updateTreeView()

            elif answer_pass=="":
                tk.messagebox.showerror("Error", "No password entered\nAccount not added")

        elif answer_name=="":
            tk.messagebox.showerror("Error", "No nickname entered\nAccount not added")


# ********** Sub Menus **********
menu = tk.Menu(root)
root.config(menu=menu)

subMenu = tk.Menu(menu)
menu.add_cascade(label = "1 ITEM", menu = subMenu)
subMenu.add_command(label = "SubItem 1")
subMenu.add_command(label = "SubItem 2")
subMenu.add_command(label = "SubItem 3")
subMenu.add_command(label = "SubItem 4")

subsubMenu = tk.Menu(subMenu)
subMenu.add_cascade(label = "SubSubMenu",menu = subsubMenu)
subsubMenu.add_cascade(label = "subsub 1")
subsubMenu.add_cascade(label = "subsub 2")
subsubMenu.add_cascade(label = "subsub 3")


#####################################################HERE IT STARTS#############

#***************** Main Frames ******************
statusbar_frame = tk.Frame(root)
statusbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

left_frame = tk.Frame(root, bg="white")
left_frame.pack(side=tk.LEFT, fill=tk.Y)

toolbar_frame = tk.Frame(left_frame, bg="#68217a")
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
but_2 = tk.Button(toolbar_frame,bg="#68217a", command=lambda *args: chooseSocial(but_2), width=65,height=65, bd=0,image = face)
but_2.pack(side=tk.TOP, padx=0,pady=0,fill=tk.X)
but_3 = tk.Button(toolbar_frame,bg="#68217a",command=lambda *args: chooseSocial(but_3), width=65,height=65, bd=0,image = twit)
but_3.pack(side=tk.TOP, padx=0,pady=0,fill=tk.X)


#**********Left workplace************
topFrame = tk.Frame(left_frame,bg="white",bd=0)
topFrame.pack(side=tk.TOP,fill = tk.X)

topBut1 = tk.Button(topFrame, width=10, text = "Sort",bd=1,bg="white")
topBut1.pack(side=tk.RIGHT)
topBut2 = tk.Button(topFrame, width=10, text = "Deselect all",bd=1,bg="white")
topBut2.pack(side=tk.RIGHT)
topBut3 = tk.Button(topFrame, width=10, text = "Select all",bd=1,bg="white")
topBut3.pack(side=tk.RIGHT)

topLable = tk.Label(topFrame,text="Instagram accounts",padx=10,bg="white",bd=1,width=20)
topLable.pack(side=tk.LEFT)

#$$$$$$$$$$$$$$$$$ ACCOUNTS MIDDLE PLATFORM $$$$$$$$$$$$$$$$$$$$$$$$
myTreeView = ttk.Treeview(left_frame,height=30, show="tree")
myTreeView.pack(fill="both", expand=True)

updateTreeView()

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
downFrame = tk.Frame(left_frame,bg="white")
downFrame.pack(side=tk.BOTTOM,fill = tk.X)


botBut0 = tk.Button(downFrame, width=10, text = "Delete all",bd=1,bg="white",command=deleteAll)
botBut0.pack(side=tk.RIGHT)
botBut1 = tk.Button(downFrame, width=15, text = "Delete selected",bd=1,bg="white",command=deleteSelected)
botBut1.pack(side=tk.RIGHT)
botBut2 = tk.Button(downFrame, width=10, text = "Add",bd=1,bg="white",command=addAccount)
botBut2.pack(side=tk.RIGHT)


# ********** Status Bar **********
status = tk.Label(statusbar_frame,text = "Preparing to do it...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side = tk.BOTTOM,fill=tk.X)



#****************Right Workplace****************
Tasks = tk.Label(root, width=100,text = "TASK MENU")
Tasks.pack(fill=tk.X)


root.mainloop()