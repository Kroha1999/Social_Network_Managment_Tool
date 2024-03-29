import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw 
from tkinter.filedialog import askopenfilename
import time
import numpy as np

from FuncFiles import languages 
from FuncFiles import globalVal

#CONSTants
PATH_PROFILE_PICS = "ProfilePicsMin\\"
MAX_UI_X = 600
MAX_UI_Y = 314

# ************************** FUNCTIONS *******************************
#_________________________DATA UI Functions______________________________
def upTask(value,lv_1,lv_3=None):
    globalVal.resetTask()
    
    if lv_3 == None:
        globalVal.Task_data[lv_1] = value
    else:
        #lv_2 is always the same two components of lv_1-> look task data
        lv_2 = globalVal.Task_data['SocialNetwork']+globalVal.Task_data['TaskType']
        globalVal.Task_data[lv_1][lv_2][lv_3] = value
    
    #print("\n"+str(globalVal.Task_data))


def updateTree(tree,insert_data):
    tree.delete(*tree.get_children())
    i=0
    
    for acc in insert_data['Instagram']:
        globalVal.myImg
        try:
            ima = globalVal.myImg[acc['nickname']+acc["imgUrl"]]
        except:
            ima = circle_img(Image.open(PATH_PROFILE_PICS+acc['nickname']+'.png'))
            globalVal.myImg[acc['nickname']+acc["imgUrl"]]=ImageTk.PhotoImage(ima)

        
        
            
        tree.insert('', i, "Item"+str(i), text = str(acc["nickname"]),image = globalVal.myImg[acc['nickname']+acc["imgUrl"]])
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
    
    updateTree(trVFrom,datasetFrom)
    updateTree(trVTo,datasetTo)

#________________________Photo Functions______________________________
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

def choosePhoto(mybtn):
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
            

        globalVal.choosePhotoImg = ImageTk.PhotoImage(im)
        print("After: "+ str(int(im.height))+"   "+str(int(im.width)))
        mybtn.configure(image = globalVal.choosePhotoImg, text = str(path))


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