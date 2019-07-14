import tkinter as tk
from tkinter import ttk


root = tk.Tk()

# ********** Sub Menu **********
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

def doIt():
    print("I'm dooooooooing!!!!!!!!")

#####################################################HERE IT STARTS#############

statusbar_frame = tk.Frame(root)
statusbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

toolbar_frame = tk.Frame(root, bg="#68217a")
toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)

#main_frame = tk.Frame(root)
#main_frame.pack(side=tk.RIGHT,fill=tk.X)



# ********** Toolbar **********
#but_1 = tk.Button(toolbar_frame, text="Insert Image",command = doIt, width=10,bg="#68217a", bd=0)
#but_1.pack(side=tk.TOP, padx=0,pady=0)
#but_2 = tk.Button(toolbar_frame, text="Print Image",command = doIt, width=10,bg="#68217a", bd=0)
#but_2.pack(side=tk.TOP, padx=0,pady=0)


# ********** Status Bar **********
status = tk.Label(statusbar_frame,text = "Preparing to do it...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status.pack(side = tk.BOTTOM,fill=tk.X)

# ********* Notebook ***********
#style = ttk.Style(root)
#style.configure('lefttab.TNotebook',tabposition='wn')
style=ttk.Style()
style.theme_create( "body", parent="classic", settings={
        "TNotebook": {"configure": {"tabmargins": [-2, -2, -2, -2] , "background": "#68217a", "tabposition":'wn' }},
        "TNotebook.Tab": {
            "configure": {"padding": [17, 20], "background": "#68217a" , "foreground":"black"},
            "map":       {"background": [("selected", "white")],
                          "expand": [("selected", [2, 5, 5, 2])] }
                        }
                                                   
            })
 
style.theme_use("body")



nb = ttk.Notebook(toolbar_frame) # nb - notebook

page1 = ttk.Frame(nb,width=1000,height=500)
nb.add(page1,text = "Tab 1")
page2 = ttk.Frame(nb,width=1000,height=500)
nb.add(page2,text = "Tab 2")
nb.pack()
#nb.grid(row=1,column=0,columnspan=50, rowspan= 49, sticky='NESW')




root.mainloop()
