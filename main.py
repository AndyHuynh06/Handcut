import subprocess 
from tkinter import *
import pickle
from pynput.keyboard import Key, Listener 
from tkinter import ttk as ttk 
from tkinter.filedialog import askopenfilename 
from PIL import Image 
from PIL import ImageTk 
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox

onoffV = False 
keys = []
recordONOFF = False
num = 1
 
#Give value for each finger
index = 0
middle = 1
ring = 2
pinky = 3
im = 4
ip = 5
ti = 6
mr = 7
tip = 8
imr = 9
mrp = 10
tim = 11
four = 12
five = 13

#List of based function:
toolL = ['copy', 'paste']

try:
    functions = pickle.load(open('function.dat', 'rb')) 
except:
    functions = ['None','None','None','None','None','None','None','None','None','None','None','None','None','None','None','None'] 
print(functions)


#Function to open insturciton (will be run by clicking on the instruction button)
def instruction():
    import webbrowser
    webbrowser.open("https://sites.google.com/ais.edu.vn/handcut-instruction/home?authuser=1")

def website(n):
    def save_url():
        global functions
        functions[n]=f"url:{url_entry.get()}" 
        print(functions)
        saveF() 
        url_win.destroy() 
    url_win = Tk() 
    url_win.title("Enter a link")
 
    url_win.geometry('200x200') 
    url_entry = Entry(url_win)
    url_entry.pack() 
 
    url_button = Button(url_win, command=save_url, text="Finish") 
    url_button.pack()
 
    url_win.mainloop()

def saveF():
    global functions
    control() 
    print(functions)
    pickle.dump(functions,open("function.dat", "wb")) 

def dicInstruction():
    def dicOff():
        dic.destroy()
    dic = Tk()
    dicL = Label(dic,text = "None")
    dicL.pack()
    dicB = Button(dic,text = "Done", command = dicOff)
    dicB.pack()
    dic.mainloop()

#Function to start the recognition file
def run():
   global onoffV 
   saveF() 
   p = subprocess.Popen(['python3', 'handtracking.py'])
   while p.poll() is None: 
       if onoffV == False:
           print('Send TERMINATE')
           p.terminate()
       win.update()  
   onoffV = False
   print('returncode', p.returncode)
 
#Function to change the state of the on off button
def startSTOP():
   global onoffV
   if onoffV == True: 
       onoffV = False
   elif onoffV == False: 
       onoffV = True
       run() 


#Function to start the key recording for customzing shortcut
def start_record(n):
    global functions
    num = n
    pickle.dump(num,open("finger.dat", "wb")) 
    p = subprocess.Popen(['python3', 'changefunc.py'])
    while p.poll() is None:
        win.update()
    print('returncode', p.returncode) 
    functions = pickle.load(open('function.dat', 'rb'))
    control()
 
#Function for customizing finger's funtion of opening file or application 
def openApp(n):
    filename = askopenfilename() 
    filename1 = filename.replace(" ", "\ ") 
    functions[n] = f"app:{filename1}" 
    saveF()
    print(functions)
 
#Functions for customizing finger's functino of typing text automatically
def text(n):
    #Sub-function to save the text
    def save_text():
        global functions
        functions[n]=f"text:{text_entry.get()}" 
        print(functions)
        saveF() 
        text_win.destroy() 
    text_win = Tk() 
    text_win.title("Please enter your text below")
 
    text_win.geometry('200x200') 
    text_entry = Entry(text_win)
    text_entry.pack() 
 
    text_button = Button(text_win, command=save_text, text="Finish") 
    text_button.pack()
 
    text_win.mainloop()
 
#Function to load in the functions of each finger from the save file particually, it will read what the function is of each finger and set the button and the label associated with those functions
def pre_control():
    #index
    if functions[0] == "copy": 
        indexV.set("copy") 
        indexE.config(text="ctrl+c")
    elif functions[0] == "Dictionary":
        indexV.set("Dictionary")
        indexE.config(text="Click button below for instruciton")
        indexR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif functions[0] == "paste":
        indexV.set("paste")
        indexE.config(text="ctrl+v")
    elif type(functions[0]) != type(functions) and functions[0].find("text:") != -1:
        indexV.set("Custom text")
        indexE.config(text=f"{functions[0]}")
        indexR.config(command = lambda: text(0), text = "Add text", state=NORMAL)
    elif type(functions[0]) != type(functions) and functions[0].find("url:") != -1:
        indexV.set("Open website")
        indexE.config(text=f"{functions[0]}")
        indexR.config(command = lambda: website(0), text = "Add link", state=NORMAL)
    elif type(functions[0]) != type(functions) and functions[0].find("app:") != -1:
        indexV.set("Open file/application")
        indexE.config(state=NORMAL)
        app_name = functions[0].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        indexE.config(text=f"{appname}")
        indexR.config(command = lambda:openApp(0), text = "Select file/application", state=NORMAL)
    elif functions[0] == "None":
        indexE.config(text="None")
        indexV.set("None")
    else:
        if len(functions[0]) > 0:
            a = ""
            b = 0
            for i in functions[0]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            indexE.config(text=a)
        indexV.set("Custom keys")
        indexR.config(state=NORMAL, text = "Add key", command = lambda: start_record(0))

    #middle
    if functions[1] == "copy":
        middleV.set("copy")
        middleE.config(text="ctrl+c")
    elif functions[1] == "Dictionary":
        middleV.set("Dictionary")
        middleE.config(text="Click button below for instruciton")
        middleR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[1]) != type(functions) and functions[1].find("url:") != -1:
        middleV.set("Open website")
        middleE.config(text=f"{functions[1]}")
        middleR.config(command = lambda: website(1), text = "Add link", state=NORMAL)
    elif functions[1] == "paste":
        middleV.set("paste")
        middleE.config(text="ctrl+v")
    elif type(functions[1]) != type(functions) and functions[1].find("text:") != -1:
        middleV.set("Custom text")
        middleE.config(text=f"{functions[1]}")
        middleR.config(command = lambda: text(1), text = "Add text", state=NORMAL)
    elif type(functions[1]) != type(functions) and functions[1].find("app:") != -1:
        middleV.set("Open file/application")
        middleE.config(state=NORMAL)
        app_name = functions[1].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        middleE.config(text=f"{appname}")
        middleR.config(command = lambda:openApp(1), text = "Select file/application", state=NORMAL)
    elif functions[1] == "None":
        middleE.config(text="None")
        middleV.set("None")
    else:
        if len(functions[1]) > 0:
            a = ""
            b = 0
            for i in functions[1]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            middleE.config(text=a)
        middleV.set("Custom keys")
        middleR.config(state=NORMAL, text = "Add key", command = lambda: start_record(1))
    
    #ring
    if functions[2] == "copy":
        ringV.set("copy")
        ringE.config(text="ctrl+c")
    elif functions[2] == "Dictionary":
        ringV.set("Dictionary")
        ringE.config(text="Click button below for instruciton")
        ringR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[2]) != type(functions) and functions[2].find("url:") != -1:
        ringV.set("Open website")
        ringE.config(text=f"{functions[2]}")
        ringR.config(command = lambda: website(2), text = "Add link", state=NORMAL)
    elif functions[2] == "paste":
        ringV.set("paste")
        ringE.config(text="ctrl+v")
    elif type(functions[2]) != type(functions) and functions[2].find("text:") != -1:
        ringV.set("Custom text")
        ringE.config(text=f"{functions[2]}")
        ringR.config(command = lambda: text(2), text = "Add text", state=NORMAL)
    elif type(functions[2]) != type(functions) and functions[2].find("app:") != -1:
        ringV.set("Open file/application")
        ringE.config(state=NORMAL)
        app_name = functions[2].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        ringE.config(text=f"{appname}")
        ringR.config(command = lambda:openApp(2), text = "Select file/application", state=NORMAL)
    elif functions[2] == "None":
        ringE.config(text="None")
        ringV.set("None")
    else:
        if len(functions[2]) > 0:
            a = ""
            b = 0
            for i in functions[2]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            ringE.config(text=a)
        ringV.set("Custom keys")
        ringR.config(state=NORMAL, text = "Add key", command = lambda: start_record(2))
    
    #pinky
    if functions[3] == "copy":
        pinkyV.set("copy")
        pinkyE.config(text="ctrl+c")
    elif functions[3] == "Dictionary":
        pinkyV.set("Dictionary")
        pinkyE.config(text="Click button below for instruciton")
        pinkyR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[3]) != type(functions) and functions[3].find("url:") != -1:
        pinkyV.set("Open website")
        pinkyE.config(text=f"{functions[3]}")
        pinkyR.config(command = lambda: website(3), text = "Add link", state=NORMAL)
    elif functions[3] == "paste":
        pinkyV.set("paste")
        pinkyE.config(text="ctrl+v")
    elif type(functions[3]) != type(functions) and functions[3].find("text:") != -1:
        pinkyV.set("Custom text")
        pinkyE.config(text=f"{functions[3]}")
        pinkyR.config(command = lambda: text(3), text = "Add text", state=NORMAL)
    elif type(functions[3]) != type(functions) and functions[3].find("app:") != -1:
        pinkyV.set("Open file/application")
        pinkyE.config(state=NORMAL)
        app_name = functions[3].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        pinkyE.config(text=f"{appname}")
        pinkyR.config(command = lambda:openApp(3), text = "Select file/application", state=NORMAL)
    elif functions[3] == "None":
        pinkyE.config(text="None")
        pinkyV.set("None")
    else:
        if len(functions[3]) > 0:
            a = ""
            b = 0
            for i in functions[3]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            pinkyE.config(text=a)
        pinkyV.set("Custom keys")
        pinkyR.config(state=NORMAL, text = "Add key", command = lambda: start_record(3))
    
    #im
    if functions[im] == "copy": 
        imV.set("copy") 
        imE.config(text="ctrl+c")
    elif functions[im] == "Dictionary":
        imV.set("Dictionary")
        imE.config(text="Click button below for instruciton")
        imR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[im]) != type(functions) and functions[im].find("url:") != -1:
        imV.set("Open website")
        imE.config(text=f"{functions[im]}")
        imR.config(command = lambda: website(im), text = "Add link", state=NORMAL)
    elif functions[im] == "paste":
        imV.set("paste")
        imE.config(text="ctrl+v")
    elif type(functions[im]) != type(functions) and functions[im].find("text:") != -1:
        imV.set("Custom text")
        imE.config(text=f"{functions[im]}")
        imR.config(command = lambda: text(im), text = "Add text", state=NORMAL)
    elif type(functions[im]) != type(functions) and functions[im].find("app:") != -1:
        imV.set("Open file/application")
        imE.config(state=NORMAL)
        app_name = functions[im].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        imE.config(text=f"{appname}")
        imR.config(command = lambda:openApp(im), text = "Select file/application", state=NORMAL)
    elif functions[im] == "None":
        imE.config(text="None")
        imV.set("None")
    else:
        if len(functions[im]) > 0:
            a = ""
            b = 0
            for i in functions[im]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            imE.config(text=a)
        imV.set("Custom keys")
        imR.config(state=NORMAL, text = "Add key", command = lambda: start_record(im))

    #ip
    if functions[ip] == "copy": 
        ipV.set("copy") 
        ipE.config(text="ctrl+c")
    elif functions[ip] == "Dictionary":
        ipV.set("Dictionary")
        ipE.config(text="Click button below for instruciton")
        ipR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[ip]) != type(functions) and functions[ip].find("url:") != -1:
        ipV.set("Open website")
        ipE.config(text=f"{functions[ip]}")
        ipR.config(command = lambda: website(ip), text = "Add link", state=NORMAL)
    elif functions[ip] == "paste":
        ipV.set("paste")
        ipE.config(text="ctrl+v")
    elif type(functions[ip]) != type(functions) and functions[ip].find("text:") != -1:
        ipV.set("Custom text")
        ipE.config(text=f"{functions[ip]}")
        ipR.config(command = lambda: text(ip), text = "Add text", state=NORMAL)
    elif type(functions[ip]) != type(functions) and functions[ip].find("app:") != -1:
        ipV.set("Open file/application")
        ipE.config(state=NORMAL)
        app_name = functions[ip].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        ipE.config(text=f"{appname}")
        ipR.config(command = lambda:openApp(ip), text = "Select file/application", state=NORMAL)
    elif functions[ip] == "None":
        ipE.config(text="None")
        ipV.set("None")
    else:
        if len(functions[ip]) > 0:
            a = ""
            b = 0
            for i in functions[ip]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            ipE.config(text=a)
        ipV.set("Custom keys")
        ipR.config(state=NORMAL, text = "Add key", command = lambda: start_record(ip))
    
    #ti
    if functions[ti] == "copy": 
        tiV.set("copy") 
        tiE.config(text="ctrl+c")
    elif functions[ti] == "Dictionary":
        tiV.set("Dictionary")
        tiE.config(text="Click button below for instruciton")
        tiR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[ti]) != type(functions) and functions[ti].find("url:") != -1:
        tiV.set("Open website")
        tiE.config(text=f"{functions[ti]}")
        tiR.config(command = lambda: website(ti), text = "Add link", state=NORMAL)
    elif functions[ti] == "paste":
        tiV.set("paste")
        tiE.config(text="ctrl+v")
    elif type(functions[ti]) != type(functions) and functions[ti].find("text:") != -1:
        tiV.set("Custom text")
        tiE.config(text=f"{functions[ti]}")
        tiR.config(command = lambda: text(ti), text = "Add text", state=NORMAL)
    elif type(functions[ti]) != type(functions) and functions[ti].find("app:") != -1:
        tiV.set("Open file/application")
        tiE.config(state=NORMAL)
        app_name = functions[ti].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        tiE.config(text=f"{appname}")
        tiR.config(command = lambda:openApp(ti), text = "Select file/application", state=NORMAL)
    elif functions[ti] == "None":
        tiE.config(text="None")
        tiV.set("None")
    else:
        if len(functions[ti]) > 0:
            a = ""
            b = 0
            for i in functions[ti]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            tiE.config(text=a)
        tiV.set("Custom keys")
        tiR.config(state=NORMAL, text = "Add key", command = lambda: start_record(ti))
    
    #mr
    if functions[mr] == "copy": 
        mrV.set("copy") 
        mrE.config(text="ctrl+c")
    elif functions[mr] == "Dictionary":
        mrV.set("Dictionary")
        mrE.config(text="Click button below for instruciton")
        mrR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[mr]) != type(functions) and functions[mr].find("url:") != -1:
        mrV.set("Open website")
        mrE.config(text=f"{functions[mr]}")
        mrR.config(command = lambda: website(mr), text = "Add link", state=NORMAL)
    elif functions[mr] == "paste":
        mrV.set("paste")
        mrE.config(text="ctrl+v")
    elif type(functions[mr]) != type(functions) and functions[mr].find("text:") != -1:
        mrV.set("Custom text")
        mrE.config(text=f"{functions[mr]}")
        mrR.config(command = lambda: text(mr), text = "Add text", state=NORMAL)
    elif type(functions[mr]) != type(functions) and functions[mr].find("app:") != -1:
        mrV.set("Open file/application")
        mrE.config(state=NORMAL)
        app_name = functions[mr].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        mrE.config(text=f"{appname}")
        mrR.config(command = lambda:openApp(mr), text = "Select file/application", state=NORMAL)
    elif functions[mr] == "None":
        mrE.config(text="None")
        mrV.set("None")
    else:
        if len(functions[mr]) > 0:
            a = ""
            b = 0
            for i in functions[mr]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            mrE.config(text=a)
        mrV.set("Custom keys")
        mrR.config(state=NORMAL, text = "Add key", command = lambda: start_record(mr))

    #tip
    if functions[tip] == "copy": 
        tipV.set("copy") 
        tipE.config(text="ctrl+c")
    elif functions[tip] == "Dictionary":
        tipV.set("Dictionary")
        tipE.config(text="Click button below for instruciton")
        tipR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[tip]) != type(functions) and functions[tip].find("url:") != -1:
        tipV.set("Open website")
        tipE.config(text=f"{functions[tip]}")
        tipR.config(command = lambda: website(tip), text = "Add link", state=NORMAL)
    elif functions[tip] == "paste":
        tipV.set("paste")
        tipE.config(text="ctrl+v")
    elif type(functions[tip]) != type(functions) and functions[tip].find("text:") != -1:
        tipV.set("Custom text")
        tipE.config(text=f"{functions[tip]}")
        tipR.config(command = lambda: text(tip), text = "Add text", state=NORMAL)
    elif type(functions[tip]) != type(functions) and functions[tip].find("app:") != -1:
        tipV.set("Open file/application")
        tipE.config(state=NORMAL)
        app_name = functions[tip].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        tipE.config(text=f"{appname}")
        tipR.config(command = lambda:openApp(tip), text = "Select file/application", state=NORMAL)
    elif functions[tip] == "None":
        tipE.config(text="None")
        tipV.set("None")
    else:
        if len(functions[tip]) > 0:
            a = ""
            b = 0
            for i in functions[tip]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            tipE.config(text=a)
        tipV.set("Custom keys")
        tipR.config(state=NORMAL, text = "Add key", command = lambda: start_record(tip))



    #imr
    if functions[imr] == "copy": 
        imrV.set("copy") 
        imrE.config(text="ctrl+c")
    elif functions[imr] == "Dictionary":
        imrV.set("Dictionary")
        imrE.config(text="Click button below for instruciton")
        imrR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[imr]) != type(functions) and functions[imr].find("url:") != -1:
        imrV.set("Open website")
        imrE.config(text=f"{functions[imr]}")
        imrR.config(command = lambda: website(imr), text = "Add link", state=NORMAL)
    elif functions[imr] == "paste":
        imrV.set("paste")
        imrE.config(text="ctrl+v")
    elif type(functions[imr]) != type(functions) and functions[imr].find("text:") != -1:
        imrV.set("Custom text")
        imrE.config(text=f"{functions[imr]}")
        imrR.config(command = lambda: text(imr), text = "Add text", state=NORMAL)
    elif type(functions[imr]) != type(functions) and functions[imr].find("app:") != -1:
        imrV.set("Open file/application")
        imrE.config(state=NORMAL)
        app_name = functions[imr].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        imrE.config(text=f"{appname}")
        imrR.config(command = lambda:openApp(imr), text = "Select file/application", state=NORMAL)
    elif functions[imr] == "None":
        imrE.config(text="None")
        imrV.set("None")
    else:
        if len(functions[imr]) > 0:
            a = ""
            b = 0
            for i in functions[imr]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            imrE.config(text=a)
        imrV.set("Custom keys")
        imrR.config(state=NORMAL, text = "Add key", command = lambda: start_record(imr))

    #mrp
    if functions[mrp] == "copy": 
        mrpV.set("copy") 
        mrpE.config(text="ctrl+c")
    elif functions[mrp] == "Dictionary":
        mrpV.set("Dictionary")
        mrpE.config(text="Click button below for instruciton")
        mrpR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[mrp]) != type(functions) and functions[mrp].find("url:") != -1:
        mrpV.set("Open website")
        mrpE.config(text=f"{functions[mrp]}")
        mrpR.config(command = lambda: website(mrp), text = "Add link", state=NORMAL)
    elif functions[mrp] == "paste":
        mrpV.set("paste")
        mrpE.config(text="ctrl+v")
    elif type(functions[mrp]) != type(functions) and functions[mrp].find("text:") != -1:
        mrpV.set("Custom text")
        mrpE.config(text=f"{functions[mrp]}")
        mrpR.config(command = lambda: text(mrp), text = "Add text", state=NORMAL)
    elif type(functions[mrp]) != type(functions) and functions[mrp].find("app:") != -1:
        mrpV.set("Open file/application")
        mrpE.config(state=NORMAL)
        app_name = functions[mrp].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        mrpE.config(text=f"{appname}")
        mrpR.config(command = lambda:openApp(mrp), text = "Select file/application", state=NORMAL)
    elif functions[mrp] == "None":
        mrpE.config(text="None")
        mrpV.set("None")
    else:
        if len(functions[mrp]) > 0:
            a = ""
            b = 0
            for i in functions[mrp]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            mrpE.config(text=a)
        mrpV.set("Custom keys")
        mrpR.config(state=NORMAL, text = "Add key", command = lambda: start_record(mrp))

    #tim
    if functions[tim] == "copy": 
        timV.set("copy") 
        timE.config(text="ctrl+c")
    elif functions[tim] == "Dictionary":
        timV.set("Dictionary")
        timE.config(text="Click button below for instruciton")
        timR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[tim]) != type(functions) and functions[tim].find("url:") != -1:
        timV.set("Open website")
        timE.config(text=f"{functions[tim]}")
        timR.config(command = lambda: website(tim), text = "Add link", state=NORMAL)
    elif functions[tim] == "paste":
        timV.set("paste")
        timE.config(text="ctrl+v")
    elif type(functions[tim]) != type(functions) and functions[tim].find("text:") != -1:
        timV.set("Custom text")
        timE.config(text=f"{functions[tim]}")
        timR.config(command = lambda: text(tim), text = "Add text", state=NORMAL)
    elif type(functions[tim]) != type(functions) and functions[tim].find("app:") != -1:
        timV.set("Open file/application")
        timE.config(state=NORMAL)
        app_name = functions[tim].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        timE.config(text=f"{appname}")
        timR.config(command = lambda:openApp(tim), text = "Select file/application", state=NORMAL)
    elif functions[tim] == "None":
        timE.config(text="None")
        timV.set("None")
    else:
        if len(functions[tim]) > 0:
            a = ""
            b = 0
            for i in functions[tim]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            timE.config(text=a)
        timV.set("Custom keys")
        timR.config(state=NORMAL, text = "Add key", command = lambda: start_record(tim))

    #four
    if functions[four] == "copy": 
        fourV.set("copy") 
        fourE.config(text="ctrl+c")
    elif functions[four] == "Dictionary":
        fourV.set("Dictionary")
        fourE.config(text="Click button below for instruciton")
        fourR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[four]) != type(functions) and functions[four].find("url:") != -1:
        fourV.set("Open website")
        fourE.config(text=f"{functions[four]}")
        fourR.config(command = lambda: website(four), text = "Add link", state=NORMAL)
    elif functions[four] == "paste":
        fourV.set("paste")
        fourE.config(text="ctrl+v")
    elif type(functions[four]) != type(functions) and functions[four].find("text:") != -1:
        fourV.set("Custom text")
        fourE.config(text=f"{functions[four]}")
        fourR.config(command = lambda: text(four), text = "Add text", state=NORMAL)
    elif type(functions[four]) != type(functions) and functions[four].find("app:") != -1:
        fourV.set("Open file/application")
        fourE.config(state=NORMAL)
        app_name = functions[four].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        fourE.config(text=f"{appname}")
        fourR.config(command = lambda:openApp(four), text = "Select file/application", state=NORMAL)
    elif functions[four] == "None":
        fourE.config(text="None")
        fourV.set("None")
    else:
        if len(functions[four]) > 0:
            a = ""
            b = 0
            for i in functions[four]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            fourE.config(text=a)
        fourV.set("Custom keys")
        fourR.config(state=NORMAL, text = "Add key", command = lambda: start_record(four))

    #five
    if functions[five] == "copy": 
        fiveV.set("copy") 
        fiveE.config(text="ctrl+c")
    elif functions[five] == "Dictionary":
        fiveV.set("Dictionary")
        fiveE.config(text="Click button below for instruciton")
        fiveR.config(text="Instruction", command= dicInstruction, state=NORMAL)
    elif type(functions[five]) != type(functions) and functions[five].find("url:") != -1:
        fiveV.set("Open website")
        fiveE.config(text=f"{functions[five]}")
        fiveR.config(command = lambda: website(five), text = "Add link", state=NORMAL)
    elif functions[five] == "paste":
        fiveV.set("paste")
        fiveE.config(text="ctrl+v")
    elif type(functions[five]) != type(functions) and functions[five].find("text:") != -1:
        fiveV.set("Custom text")
        fiveE.config(text=f"{functions[five]}")
        fiveR.config(command = lambda: text(five), text = "Add text", state=NORMAL)
    elif type(functions[five]) != type(functions) and functions[five].find("app:") != -1:
        fiveV.set("Open file/application")
        fiveE.config(state=NORMAL)
        app_name = functions[five].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        fiveE.config(text=f"{appname}")
        fiveR.config(command = lambda:openApp(five), text = "Select file/application", state=NORMAL)
    elif functions[five] == "None":
        fiveE.config(text="None")
        fiveV.set("None")
    else:
        if len(functions[five]) > 0:
            a = ""
            b = 0
            for i in functions[five]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            fiveE.config(text=a)
        fiveV.set("Custom keys")
        fiveR.config(state=NORMAL, text = "Add key", command = lambda: start_record(five))



#Function to load the whole user interface again when a function is changed (it's kind of similiar to the pre-control function but it's more simple and needs to be seperated out becasue of some bugs)
def control():
    #index
    if functions[0] == "Dictionary":
        indexE.config(text="Click button below for instruciton")
    elif functions[0] == "copy": 
        indexE.config(text="ctrl+c")
    elif functions[0] == "paste":
        indexE.config(text="ctrl+v")
    elif type(functions[0]) != type(functions) and functions[0].find("text:") != -1:
        indexE.config(text=f"{functions[0]}")
        indexR.config(command = lambda: text(0), text = "Add text", state=NORMAL)
    elif type(functions[0]) != type(functions) and functions[0].find("url:") != -1:
        indexE.config(text=f"{functions[0]}")
        indexR.config(command = lambda: website(0), text = "Add link", state=NORMAL)
    elif type(functions[0]) != type(functions) and functions[0].find("app:") != -1:
        indexE.config(state=NORMAL)
        app_name = functions[0].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        indexE.config(text=f"{appname}")
        indexR.config(command = lambda:openApp(0), text = "Select file/application", state=NORMAL)
    elif functions[0] == "None":
        indexE.config(text="None")
    else:
        if len(functions[0]) > 0:
            a = ""
            b = 0
            for i in functions[0]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            indexE.config(text=a)
 
    #middle
    if functions[1] == "copy":
        middleE.config(text="ctrl+c")
    elif functions[1] == "Dictionary":
        middleE.config(text="Click button below for instruciton")
    elif functions[1] == "paste":
        middleE.config(text="ctrl+v")
    elif type(functions[1]) != type(functions) and functions[1].find("text:") != -1:
        middleE.config(text=f"{functions[1]}")
        middleR.config(command = lambda: text(1), text = "Add text", state=NORMAL)
    elif type(functions[1]) != type(functions) and functions[1].find("url:") != -1:
        middleE.config(text=f"{functions[1]}")
        middleR.config(command = lambda: website(1), text = "Add link", state=NORMAL)
    elif type(functions[1]) != type(functions) and functions[1].find("app:") != -1:
        middleE.config(state=NORMAL)
        app_name = functions[1].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        middleE.config(text=f"{appname}")
        middleR.config(command = lambda:openApp(1), text = "Select file/application", state=NORMAL)
    elif functions[1] == "None":
        middleE.config(text="None")
    else:
        if len(functions[1]) > 0:
            a = ""
            b = 0
            for i in functions[1]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            middleE.config(text=a)
    
    #ring
    if functions[2] == "copy":
        ringE.config(text="ctrl+c")
    elif functions[2] == "Dictionary":
        ringE.config(text="Click button below for instruciton")
    elif type(functions[2]) != type(functions) and functions[2].find("url:") != -1:
        ringE.config(text=f"{functions[2]}")
        ringR.config(command = lambda: website(2), text = "Add link", state=NORMAL)
    elif functions[2] == "paste":
        ringE.config(text="ctrl+v")
    elif type(functions[2]) != type(functions) and functions[2].find("text:") != -1:
        ringE.config(text=f"{functions[0]}")
        ringR.config(command = lambda: text(2), text = "Add text", state=NORMAL)
    elif type(functions[2]) != type(functions) and functions[2].find("app:") != -1:
        ringE.config(state=NORMAL)
        app_name = functions[2].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        ringE.config(text=f"{appname}")
        ringR.config(command = lambda:openApp(3), text = "Select file/application", state=NORMAL)
    elif functions[2] == "None":
        ringE.config(text="None")
    else:
        if len(functions[2]) > 0:
            a = ""
            b = 0
            for i in functions[2]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            ringE.config(text=a)
    
    #pinky
    if functions[3] == "copy":
        pinkyE.config(text="ctrl+c")
    elif functions[3] == "Dictionary":
        pinkyE.config(text="Click button below for instruciton")
    elif type(functions[3]) != type(functions) and functions[3].find("url:") != -1:
        pinkyE.config(text=f"{functions[3]}")
        pinkyR.config(command = lambda: website(3), text = "Add link", state=NORMAL)
    elif functions[3] == "paste":
        pinkyE.config(text="ctrl+v")
    elif type(functions[3]) != type(functions) and functions[3].find("text:") != -1:
        pinkyE.config(text=f"{functions[3]}")
        pinkyR.config(command = lambda: text(3), text = "Add text", state=NORMAL)
    elif type(functions[3]) != type(functions) and functions[3].find("app:") != -1:
        pinkyE.config(state=NORMAL)
        app_name = functions[3].replace('app:', '').replace('\ ', ' ').split("/")
        appname = StringVar
        appname =app_name[len(app_name)-1]
        pinkyE.config(text=f"{appname}")
        pinkyR.config(command = lambda:openApp(3), text = "Select file/application", state=NORMAL)
    elif functions[3] == "None":
        pinkyE.config(text="None")
    else:
        if len(functions[3]) > 0:
            a = ""
            b = 0
            for i in functions[3]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            pinkyE.config(text=a)
    
    #im
    if functions[im] == "Dictionary":
        imE.config(text="Click button below for instruciton")
    elif functions[im] == "copy": 
        imE.config(text="ctrl+c")
    elif type(functions[im]) != type(functions) and functions[im].find("url:") != -1:
        imE.config(text=f"{functions[im]}")
        imR.config(command = lambda: website(im), text = "Add link", state=NORMAL)
    elif functions[im] == "paste":
        imE.config(text="ctrl+v")
    elif type(functions[im]) != type(functions) and functions[im].find("text:") != -1:
        imE.config(text=f"{functions[im]}")
        imR.config(command = lambda: text(im), text = "Add text", state=NORMAL)
    elif type(functions[im]) != type(functions) and functions[im].find("app:") != -1:
        imE.config(state=NORMAL)
        app_name = functions[im].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        imE.config(text=f"{appname}")
        imR.config(command = lambda:openApp(im), text = "Select file/application", state=NORMAL)
    elif functions[im] == "None":
        imE.config(text="None")
    else:
        if len(functions[im]) > 0:
            a = ""
            b = 0
            for i in functions[im]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            imE.config(text=a)
    
    #ip
    if functions[ip] == "Dictionary":
        ipE.config(text="Click button below for instruciton")
    elif functions[ip] == "copy": 
        ipE.config(text="ctrl+c")
    elif functions[ip] == "paste":
        ipE.config(text="ctrl+v")
    elif type(functions[ip]) != type(functions) and functions[ip].find("url:") != -1:
        ipE.config(text=f"{functions[ip]}")
        ipR.config(command = lambda: website(ip), text = "Add link", state=NORMAL)
    elif type(functions[ip]) != type(functions) and functions[ip].find("text:") != -1:
        ipE.config(text=f"{functions[ip]}")
        ipR.config(command = lambda: text(ip), text = "Add text", state=NORMAL)
    elif type(functions[ip]) != type(functions) and functions[ip].find("app:") != -1:
        ipE.config(state=NORMAL)
        app_name = functions[ip].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        ipE.config(text=f"{appname}")
        ipR.config(command = lambda:openApp(ip), text = "Select file/application", state=NORMAL)
    elif functions[ip] == "None":
        ipE.config(text="None")
    else:
        if len(functions[ip]) > 0:
            a = ""
            b = 0
            for i in functions[ip]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            ipE.config(text=a)

    #ti
    if functions[ti] == "Dictionary":
        tiE.config(text="Click button below for instruciton")
    elif functions[ti] == "copy": 
        tiE.config(text="ctrl+c")
    elif functions[ti] == "paste":
        tiE.config(text="ctrl+v")
    elif type(functions[ti]) != type(functions) and functions[ti].find("url:") != -1:
        tiE.config(text=f"{functions[ti]}")
        tiR.config(command = lambda: website(ti), text = "Add link", state=NORMAL)
    elif type(functions[ti]) != type(functions) and functions[ti].find("text:") != -1:
        tiE.config(text=f"{functions[ti]}")
        tiR.config(command = lambda: text(ti), text = "Add text", state=NORMAL)
    elif type(functions[ti]) != type(functions) and functions[ti].find("app:") != -1:
        tiE.config(state=NORMAL)
        app_name = functions[ti].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        tiE.config(text=f"{appname}")
        tiR.config(command = lambda:openApp(ti), text = "Select file/application", state=NORMAL)
    elif functions[ti] == "None":
        tiE.config(text="None")
    else:
        if len(functions[ti]) > 0:
            a = ""
            b = 0
            for i in functions[ti]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            tiE.config(text=a)

    #mr
    if functions[mr] == "Dictionary":
        mrE.config(text="Click button below for instruciton")
    elif functions[mr] == "copy": 
        mrE.config(text="ctrl+c")
    elif functions[mr] == "paste":
        mrE.config(text="ctrl+v")
    elif type(functions[mr]) != type(functions) and functions[mr].find("url:") != -1:
        mrE.config(text=f"{functions[mr]}")
        mrR.config(command = lambda: website(mr), text = "Add link", state=NORMAL)
    elif type(functions[mr]) != type(functions) and functions[mr].find("text:") != -1:
        mrE.config(text=f"{functions[mr]}")
        mrR.config(command = lambda: text(mr), text = "Add text", state=NORMAL)
    elif type(functions[mr]) != type(functions) and functions[mr].find("app:") != -1:
        mrE.config(state=NORMAL)
        app_name = functions[mr].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        mrE.config(text=f"{appname}")
        mrR.config(command = lambda:openApp(mr), text = "Select file/application", state=NORMAL)
    elif functions[mr] == "None":
        mrE.config(text="None")
    else:
        if len(functions[mr]) > 0:
            a = ""
            b = 0
            for i in functions[mr]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            mrE.config(text=a)
    
    #tip
    if functions[tip] == "Dictionary":
        tipE.config(text="Click button below for instruciton")
    elif functions[tip] == "copy": 
        tipE.config(text="ctrl+c")
    elif functions[tip] == "paste":
        tipE.config(text="ctrl+v")
    elif type(functions[tip]) != type(functions) and functions[tip].find("url:") != -1:
        tipE.config(text=f"{functions[tip]}")
        tipR.config(command = lambda: website(tip), text = "Add link", state=NORMAL)
    elif type(functions[tip]) != type(functions) and functions[tip].find("text:") != -1:
        tipE.config(text=f"{functions[tip]}")
        tipR.config(command = lambda: text(tip), text = "Add text", state=NORMAL)
    elif type(functions[tip]) != type(functions) and functions[tip].find("app:") != -1:
        tipE.config(state=NORMAL)
        app_name = functions[tip].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        tipE.config(text=f"{appname}")
        tipR.config(command = lambda:openApp(tip), text = "Select file/application", state=NORMAL)
    elif functions[tip] == "None":
        tipE.config(text="None")
    else:
        if len(functions[tip]) > 0:
            a = ""
            b = 0
            for i in functions[tip]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            tipE.config(text=a)

    #imr
    if functions[imr] == "Dictionary":
        imrE.config(text="Click button below for instruciton")
    elif functions[imr] == "copy": 
        imrE.config(text="ctrl+c")
    elif functions[imr] == "paste":
        imrE.config(text="ctrl+v")
    elif type(functions[imr]) != type(functions) and functions[imr].find("url:") != -1:
        imrE.config(text=f"{functions[imr]}")
        imrR.config(command = lambda: website(imr), text = "Add link", state=NORMAL)
    elif type(functions[imr]) != type(functions) and functions[imr].find("text:") != -1:
        imrE.config(text=f"{functions[imr]}")
        imrR.config(command = lambda: text(imr), text = "Add text", state=NORMAL)
    elif type(functions[imr]) != type(functions) and functions[imr].find("app:") != -1:
        imrE.config(state=NORMAL)
        app_name = functions[imr].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        imrE.config(text=f"{appname}")
        imrR.config(command = lambda:openApp(imr), text = "Select file/application", state=NORMAL)
    elif functions[imr] == "None":
        imrE.config(text="None")
    else:
        if len(functions[imr]) > 0:
            a = ""
            b = 0
            for i in functions[imr]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            imrE.config(text=a)
    
    #mrp
    if functions[mrp] == "Dictionary":
        mrpE.config(text="Click button below for instruciton")
    elif functions[mrp] == "copy": 
        mrpE.config(text="ctrl+c")
    elif functions[mrp] == "paste":
        mrpE.config(text="ctrl+v")
    elif type(functions[mrp]) != type(functions) and functions[mrp].find("url:") != -1:
        mrpE.config(text=f"{functions[mrp]}")
        mrpR.config(command = lambda: website(mrp), text = "Add link", state=NORMAL)
    elif type(functions[mrp]) != type(functions) and functions[mrp].find("text:") != -1:
        mrpE.config(text=f"{functions[mrp]}")
        mrpR.config(command = lambda: text(mrp), text = "Add text", state=NORMAL)
    elif type(functions[mrp]) != type(functions) and functions[mrp].find("app:") != -1:
        mrpE.config(state=NORMAL)
        app_name = functions[mrp].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        mrpE.config(text=f"{appname}")
        mrpR.config(command = lambda:openApp(mrp), text = "Select file/application", state=NORMAL)
    elif functions[mrp] == "None":
        mrpE.config(text="None")
    else:
        if len(functions[mrp]) > 0:
            a = ""
            b = 0
            for i in functions[mrp]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            mrpE.config(text=a)
    
    #tim
    if functions[tim] == "Dictionary":
        timE.config(text="Click button below for instruciton")
    elif functions[tim] == "copy": 
        timE.config(text="ctrl+c")
    elif functions[tim] == "paste":
        timE.config(text="ctrl+v")
    elif type(functions[tim]) != type(functions) and functions[tim].find("url:") != -1:
        timE.config(text=f"{functions[tim]}")
        timR.config(command = lambda: website(tim), text = "Add link", state=NORMAL)
    elif type(functions[tim]) != type(functions) and functions[tim].find("text:") != -1:
        timE.config(text=f"{functions[tim]}")
        timR.config(command = lambda: text(tim), text = "Add text", state=NORMAL)
    elif type(functions[tim]) != type(functions) and functions[tim].find("app:") != -1:
        timE.config(state=NORMAL)
        app_name = functions[tim].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        timE.config(text=f"{appname}")
        timR.config(command = lambda:openApp(tim), text = "Select file/application", state=NORMAL)
    elif functions[tim] == "None":
        timE.config(text="None")
    else:
        if len(functions[tim]) > 0:
            a = ""
            b = 0
            for i in functions[tim]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            timE.config(text=a)

    #four
    if functions[four] == "Dictionary":
        fourE.config(text="Click button below for instruciton")
    elif functions[four] == "copy": 
        fourE.config(text="ctrl+c")
    elif functions[four] == "paste":
        fourE.config(text="ctrl+v")
    elif type(functions[four]) != type(functions) and functions[four].find("url:") != -1:
        fourE.config(text=f"{functions[four]}")
        fourR.config(command = lambda: website(four), text = "Add link", state=NORMAL)
    elif type(functions[four]) != type(functions) and functions[four].find("text:") != -1:
        fourE.config(text=f"{functions[four]}")
        fourR.config(command = lambda: text(four), text = "Add text", state=NORMAL)
    elif type(functions[four]) != type(functions) and functions[four].find("app:") != -1:
        fourE.config(state=NORMAL)
        app_name = functions[four].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        fourE.config(text=f"{appname}")
        fourR.config(command = lambda:openApp(four), text = "Select file/application", state=NORMAL)
    elif functions[four] == "None":
        fourE.config(text="None")
    else:
        if len(functions[four]) > 0:
            a = ""
            b = 0
            for i in functions[four]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            fourE.config(text=a)

    #five
    if functions[five] == "Dictionary":
        fiveE.config(text="Click button below for instruciton")
    elif functions[five] == "copy": 
        fiveE.config(text="ctrl+c")
    elif functions[five] == "paste":
        fiveE.config(text="ctrl+v")
    elif type(functions[five]) != type(functions) and functions[five].find("url:") != -1:
        fiveE.config(text=f"{functions[five]}")
        fiveR.config(command = lambda: website(five), text = "Add link", state=NORMAL)
    elif type(functions[five]) != type(functions) and functions[five].find("text:") != -1:
        fiveE.config(text=f"{functions[five]}")
        fiveR.config(command = lambda: text(five), text = "Add text", state=NORMAL)
    elif type(functions[five]) != type(functions) and functions[five].find("app:") != -1:
        fiveE.config(state=NORMAL)
        app_name = functions[five].replace('app:', '').replace('\ ', ' ').split("/")
        appname =app_name[len(app_name)-1]
        fiveE.config(text=f"{appname}")
        fiveR.config(command = lambda:openApp(five), text = "Select file/application", state=NORMAL)
    elif functions[five] == "None":
        fiveE.config(text="None")
    else:
        if len(functions[five]) > 0:
            a = ""
            b = 0
            for i in functions[five]:
                if b == 0:
                    a+=i
                else:
                    a += "+" + i
                b += 1
            fiveE.config(text=a)
 



try:
    colors = pickle.load(open('color.dat', 'rb')) 
except:
   colors = ['#87FFD3','#A03863']

print(colors)

background_color = colors[0]
foreground_color = colors[1]
path = "body.png"

def update_color():
    global background_color, foreground_color
    #win color
    win.config(bg=background_color)
    title.config(bg=background_color)
    buttonFrame.config(bg=background_color)
    handFrame.config(bg=background_color)
    title.config(fg=foreground_color)
    tabFrame.config(bg=background_color)
    twofingerFrame.config(bg=background_color)
    threefingerFrame.config(bg=background_color)
    fourfingerFrame.config(bg=background_color)

    #index color
    indexL.config(bg=background_color)
    indexE.config(bg=background_color)
    indexR.config(highlightbackground=background_color)
    indexL.config(fg=foreground_color)
    indexE.config(fg=foreground_color)
    #Middle color
    middleL.config(bg=background_color)
    middleE.config(bg=background_color)
    middleL.config(fg=foreground_color)
    middleE.config(fg=foreground_color)
    middleR.config(highlightbackground=background_color)
    #ring
    ringL.config(bg=background_color)
    ringE.config(bg=background_color)
    ringL.config(fg=foreground_color)
    ringE.config(fg=foreground_color)
    ringR.config(highlightbackground=background_color)
    #pinky
    pinkyL.config(bg=background_color)
    pinkyE.config(bg=background_color)
    pinkyR.config(highlightbackground=background_color)
    pinkyL.config(fg=foreground_color)
    pinkyE.config(fg=foreground_color)
    #im
    imL.config(bg=background_color)
    imE.config(bg=background_color)
    imR.config(highlightbackground=background_color)
    imL.config(fg=foreground_color)
    imE.config(fg=foreground_color)
    #ip
    ipL.config(bg=background_color)
    ipE.config(bg=background_color)
    ipR.config(highlightbackground=background_color)
    ipL.config(fg=foreground_color)
    ipE.config(fg=foreground_color)
    #ti
    tiL.config(bg=background_color)
    tiE.config(bg=background_color)
    tiR.config(highlightbackground=background_color)
    tiL.config(fg=foreground_color)
    tiE.config(fg=foreground_color)
    #mr
    mrL.config(bg=background_color)
    mrE.config(bg=background_color)
    mrR.config(highlightbackground=background_color)
    mrL.config(fg=foreground_color)
    mrE.config(fg=foreground_color)
    #tip
    tipL.config(bg=background_color)
    tipE.config(bg=background_color)
    tipR.config(highlightbackground=background_color)
    tipL.config(fg=foreground_color)
    tipE.config(fg=foreground_color)
    #imr
    imrL.config(bg=background_color)
    imrE.config(bg=background_color)
    imrR.config(highlightbackground=background_color)
    imrL.config(fg=foreground_color)
    imrE.config(fg=foreground_color)
    #mrp
    mrpL.config(bg=background_color)
    mrpE.config(bg=background_color)
    mrpR.config(highlightbackground=background_color)
    mrpL.config(fg=foreground_color)
    mrpE.config(fg=foreground_color)
    #tim
    timL.config(bg=background_color)
    timE.config(bg=background_color)
    timR.config(highlightbackground=background_color)
    timL.config(fg=foreground_color)
    timE.config(fg=foreground_color)
    #four
    fourL.config(bg=background_color)
    fourE.config(bg=background_color)
    fourR.config(highlightbackground=background_color)
    fourL.config(fg=foreground_color)
    fourE.config(fg=foreground_color)
    #five
    fiveL.config(bg=background_color)
    fiveE.config(bg=background_color)
    fiveR.config(highlightbackground=background_color)
    fiveL.config(fg=foreground_color)
    fiveE.config(fg=foreground_color)

    colors = [background_color,foreground_color, path]
    pickle.dump(colors,open("color.dat", "wb"))
def primary_color():
    global background_color, colors, foreground_color
    primary_color = colorchooser.askcolor()[1]
    background_color = primary_color
    update_color()
def secondary_color():
    global foreground_color, colors, background_color
    secondary_color = colorchooser.askcolor()[1]
    foreground_color = secondary_color
    update_color()
def defaultColor():
    global background_color, colors, foreground_color
    background_color = '#87FFD3'
    foreground_color = '#A03863'
    update_color()
def red_white():
    global background_color, colors, foreground_color
    background_color = '#FAFAFA'
    foreground_color = '#FF5959'
    update_color()
def blue_white():
    global background_color, colors, foreground_color
    background_color = '#FAFAFA'
    foreground_color = '#00848B'
    update_color()


win = Tk()#Main user interface window

changeTextV = StringVar()
 
win.geometry("720x550")
win.title("Handcut")
win.config(bg=background_color)

title = Label(win, text="Handcut", font=('Times', 60), fg=foreground_color, bg=background_color) 
title.pack()

tabFrame = Frame(win, width=300, height=450, bg=background_color)
tabFrame.pack_propagate(0) 
tabFrame.pack(side=LEFT) 

style = ttk.Style()

style.theme_create( "yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": "#FFFFFF"},
            "map":       {"background": [("selected", "#DADDE2")],
                          "expand": [("selected", [1, 1, 1, 0])], } } } )

style.theme_use("yummy")

tabControl = ttk.Notebook(tabFrame, style="TNotebook")
tabControl.pack(expand=1, fill='both', padx=5, pady=5)

buttonFrame = Frame(tabControl, width=300, height=450, bg=background_color) 
buttonFrame.pack(fill="both")
twofingerFrame = Frame(tabControl, width=300, height=450, bg=background_color) 
twofingerFrame.pack(expand=1, fill="both")
threefingerFrame = Frame(tabControl, width=300, height=450, bg=background_color) 
threefingerFrame.pack(expand=1, fill="both")
fourfingerFrame = Frame(tabControl, width=300, height=450, bg=background_color) 
fourfingerFrame.pack(expand=1, fill="both")

tabControl.add(buttonFrame, text="1 finger")
tabControl.add(twofingerFrame, text="2 fingers")
tabControl.add(threefingerFrame, text="3 fingers")
tabControl.add(fourfingerFrame, text="4+5 fingers")

#Functions related to the drop box button to run different functions depend on the chosen options
def indexF(event):
    global functions
    if indexV.get() == "custom keys":
        indexV.set("custom keys")
        indexR.config(command =lambda: start_record(0), text = "Add key", state=NORMAL)
        indexE.config(text="Click below to custom your shortcut")
        functions[0] = []
        saveF()
    elif indexV.get() == 'Dictionary':
        indexE.config(text="Click button below for instruction")
        indexR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[0] = "Dictionary"
        saveF()
    elif indexV.get() == "custom text":
        print("work")
        indexE.config(text="Click below to enter text")
        indexV.set("custom text")
        indexR.config(command = lambda: text(0), text = "Add text", state=NORMAL)
    elif indexV.get() == "Open website":
        indexE.config(text="Click below to enter url")
        indexV.set("Open website")
        indexR.config(command = lambda: website(0), text = "Add link", state=NORMAL)
    elif indexV.get() == 'Open file/application':
        indexV.set("Open file/application")
        indexE.config(text="Click below to choose file")
        indexR.config(command = lambda:openApp(0), text = "Select file/application", state=NORMAL)
    else:
        indexR.pack()
        indexR.config(command = lambda: start_record(0), text = "Record",state=DISABLED)
        print(indexV.get())
        functions[0] = indexV.get()
        saveF()
 
def middleF(event):
    global functions
    if middleV.get() == "custom keys":
        middleV.set("custom keys")
        middleR.config(command =lambda: start_record(1), text = "Add key", state=NORMAL)
        middleE.config(text="Click below to custom your shortcut")
        functions[1] = []
        saveF()
    elif middleV.get() == 'Dictionary':
        middleE.config(text="Click button below for instruction")
        middleR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[1] = "Dictionary"
        saveF()
    elif middleV.get() == "custom text":
        print("work")
        middleE.config(text="Click below to enter text")
        middleV.set("custom text")
        middleR.config(command = lambda: text(1), text = "Add text", state=NORMAL)
    elif middleV.get() == "Open website":
        middleE.config(text="Click below to enter url")
        middleV.set("Open website")
        middleR.config(command = lambda: website(1), text = "Add link", state=NORMAL)
    elif middleV.get() == 'Open file/application':
        middleV.set("Open file/application")
        middleE.config(text="Click below to choose file")
        middleR.config(command = lambda:openApp(1), text = "Select file/application", state=NORMAL)
    else:
        middleR.pack()
        middleR.config(command = lambda: start_record(1), text = "Record",state=DISABLED)
        functions[1] = middleV.get()
        saveF()
def ringF(event):
    global functions
    if ringV.get() == "custom keys":
        ringV.set("custom keys")
        ringR.config(command =lambda: start_record(2), text = "Add key", state=NORMAL)
        ringE.config(text="Click below to custom your shortcut")
        functions[2] = []
        saveF() 
    elif indexV.get() == "Open website":
        ringE.config(text="Click below to enter url")
        ringV.set("Open website")
        ringR.config(command = lambda: website(2), text = "Add link", state=NORMAL)
    elif ringV.get() == 'Dictionary':
        ringE.config(text="Click button below for instruction")
        ringR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[2] = "Dictionary"
        saveF()
    elif ringV.get() == "custom text":
        print("work")
        ringE.config(text="Click below to enter text")
        ringV.set("custom text")
        ringR.config(command = lambda: text(2), text = "Add text", state=NORMAL)
    elif ringV.get() == 'Open file/application':
        ringV.set("Open file/application")
        ringE.config(text="Click below to choose file")
        ringR.config(command = lambda:openApp(2), text = "Select file/application", state=NORMAL)
    else:
        ringR.pack()
        ringR.config(command = lambda: start_record(2), text = "Record",state=DISABLED)
        functions[2] = ringV.get()
        saveF()
def pinkyF(event):
    global functions
    if pinkyV.get() == "custom keys":
        pinkyV.set("custom keys")
        pinkyR.config(command =lambda: start_record(3), text = "Add key", state=NORMAL)
        pinkyE.config(text="Click below to custom your shortcut")
        functions[3] = []
        saveF()
    elif pinkyV.get() == "Open website":
        pinkyE.config(text="Click below to enter url")
        pinkyV.set("Open website")
        pinkyR.config(command = lambda: website(3), text = "Add link", state=NORMAL)
    elif pinkyV.get() == 'Dictionary':
        pinkyE.config(text="Click button below for instruction")
        pinkyR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[3] = "Dictionary"
        saveF()
    elif pinkyV.get() == "custom text":
        print("work")
        pinkyE.config(text="Click below to enter text")
        pinkyV.set("custom text")
        pinkyR.config(command = lambda: text(3), text = "Add text", state=NORMAL)
    elif pinkyV.get() == 'Open file/application':
        pinkyV.set("Open file/application")
        pinkyE.config(text="Click below to choose file")
        pinkyR.config(command = lambda:openApp(3), text = "Select file/application", state=NORMAL)
    else:
        pinkyR.pack()
        pinkyR.config(command = lambda: start_record(3), text = "Record",state=DISABLED)
        functions[3] = pinkyV.get()
        saveF()
 
def imF(event):
    global functions
    if imV.get() == "custom keys":
        imV.set("custom keys")
        imR.config(command =lambda: start_record(im), text = "Add key", state=NORMAL)
        imE.config(text="Click below to custom your shortcut")
        functions[im] = []
        saveF() 
    elif imV.get() == "Open website":
        imE.config(text="Click below to enter url")
        imV.set("Open website")
        imR.config(command = lambda: website(im), text = "Add link", state=NORMAL)
    elif imV.get() == 'Dictionary':
        imE.config(text="Click button below for instruction")
        imR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[im] = "Dictionary"
        saveF()
    elif imV.get() == "custom text":
        print("work")
        imE.config(text="Click below to enter text")
        imV.set("custom text")
        imR.config(command = lambda: text(im), text = "Add text", state=NORMAL)
    elif imV.get() == 'Open file/application':
        imV.set("Open file/application")
        imE.config(text="Click below to choose file")
        imR.config(command = lambda:openApp(im), text = "Select file/application", state=NORMAL)
    else:
        imR.pack()
        imR.config(command = lambda: start_record(im), text = "Record",state=DISABLED)
        print(imV.get())
        functions[im] = imV.get()
        saveF()

def ipF(event):
    global functions
    if ipV.get() == "custom keys":
        ipV.set("custom keys")
        ipR.config(command =lambda: start_record(ip), text = "Add key", state=NORMAL)
        ipE.config(text="Click below to custom your shortcut")
        functions[ip] = []
        saveF()
    elif ipV.get() == "Open website":
        ipE.config(text="Click below to enter url")
        ipV.set("Open website")
        ipR.config(command = lambda: website(ip), text = "Add link", state=NORMAL)
    elif ipV.get() == 'Dictionary':
        ipE.config(text="Click button below for instruction")
        ipR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[ip] = "Dictionary"
        saveF()
    elif ipV.get() == "custom text":
        print("work")
        ipE.config(text="Click below to enter text")
        ipV.set("custom text")
        ipR.config(command = lambda: text(ip), text = "Add text", state=NORMAL)
    elif ipV.get() == 'Open file/application':
        ipV.set("Open file/application")
        ipE.config(text="Click below to choose file")
        ipR.config(command = lambda:openApp(ip), text = "Select file/application", state=NORMAL)
    else:
        ipR.pack()
        ipR.config(command = lambda: start_record(ip), text = "Record",state=DISABLED)
        print(ipV.get())
        functions[ip] = ipV.get()
        saveF()

def tiF(event):
    global functions
    if tiV.get() == "custom keys":
        tiV.set("custom keys")
        tiR.config(command =lambda: start_record(ti), text = "Add key", state=NORMAL)
        tiE.config(text="Click below to custom your shortcut")
        functions[ti] = []
        saveF()
    elif tiV.get() == "Open website":
        tiE.config(text="Click below to enter url")
        tiV.set("Open website")
        tiR.config(command = lambda: website(ti), text = "Add link", state=NORMAL)
    elif tiV.get() == 'Dictionary':
        tiE.config(text="Click button below for instruction")
        tiR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[ti] = "Dictionary"
        saveF()
    elif tiV.get() == "custom text":
        print("work")
        tiE.config(text="Click below to enter text")
        tiV.set("custom text")
        tiR.config(command = lambda: text(ti), text = "Add text", state=NORMAL)
    elif tiV.get() == 'Open file/application':
        tiV.set("Open file/application")
        tiE.config(text="Click below to choose file")
        tiR.config(command = lambda:openApp(ti), text = "Select file/application", state=NORMAL)
    else:
        tiR.pack()
        tiR.config(command = lambda: start_record(ti), text = "Record",state=DISABLED)
        print(tiV.get())
        functions[ti] = tiV.get()
        saveF()

def mrF(event):
    global functions
    if mrV.get() == "custom keys":
        mrV.set("custom keys")
        mrR.config(command =lambda: start_record(mr), text = "Add key", state=NORMAL)
        mrE.config(text="Click below to custom your shortcut")
        functions[mr] = []
        saveF()
    elif mrV.get() == "Open website":
        mrE.config(text="Click below to enter url")
        mrV.set("Open website")
        mrR.config(command = lambda: website(mr), text = "Add link", state=NORMAL)
    elif mrV.get() == 'Dictionary':
        mrE.config(text="Click button below for instruction")
        mrR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[mr] = "Dictionary"
        saveF()
    elif mrV.get() == "custom text":
        print("work")
        mrE.config(text="Click below to enter text")
        mrV.set("custom text")
        mrR.config(command = lambda: text(mr), text = "Add text", state=NORMAL)
    elif mrV.get() == 'Open file/application':
        mrV.set("Open file/application")
        mrE.config(text="Click below to choose file")
        mrR.config(command = lambda:openApp(mr), text = "Select file/application", state=NORMAL)
    else:
        mrR.pack()
        mrR.config(command = lambda: start_record(mr), text = "Record",state=DISABLED)
        print(mrV.get())
        functions[mr] = mrV.get()
        saveF()

def tipF(event):
    global functions
    if tipV.get() == "custom keys":
        tipV.set("custom keys")
        tipR.config(command =lambda: start_record(tip), text = "Add key", state=NORMAL)
        tipE.config(text="Click below to custom your shortcut")
        functions[tip] = []
        saveF()
    elif tipV.get() == "Open website":
        tipE.config(text="Click below to enter url")
        tipV.set("Open website")
        tipR.config(command = lambda: website(im), text = "Add link", state=NORMAL)
    elif tipV.get() == 'Dictionary':
        tipE.config(text="Click button below for instruction")
        tipR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[tip] = "Dictionary"
        saveF()
    elif tipV.get() == "custom text":
        print("work")
        tipE.config(text="Click below to enter text")
        tipV.set("custom text")
        tipR.config(command = lambda: text(tip), text = "Add text", state=NORMAL)
    elif tipV.get() == 'Open file/application':
        tipV.set("Open file/application")
        tipE.config(text="Click below to choose file")
        tipR.config(command = lambda:openApp(tip), text = "Select file/application", state=NORMAL)
    else:
        tipR.pack()
        tipR.config(command = lambda: start_record(tip), text = "Record",state=DISABLED)
        print(tipV.get())
        functions[tip] = tipV.get()
        saveF()

def imrF(event):
    global functions
    if imrV.get() == "custom keys":
        imrV.set("custom keys")
        imrR.config(command =lambda: start_record(imr), text = "Add key", state=NORMAL)
        imrE.config(text="Click below to custom your shortcut")
        functions[imr] = []
        saveF()
    elif imrV.get() == "Open website":
        imrE.config(text="Click below to enter url")
        imrV.set("Open website")
        imrR.config(command = lambda: website(imr), text = "Add link", state=NORMAL)
    elif imrV.get() == 'Dictionary':
        imrE.config(text="Click button below for instruction")
        imrR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[imr] = "Dictionary"
        saveF()
    elif imrV.get() == "custom text":
        print("work")
        imrE.config(text="Click below to enter text")
        imrV.set("custom text")
        imrR.config(command = lambda: text(imr), text = "Add text", state=NORMAL)
    elif imrV.get() == 'Open file/application':
        imrV.set("Open file/application")
        imrE.config(text="Click below to choose file")
        imrR.config(command = lambda:openApp(imr), text = "Select file/application", state=NORMAL)
    else:
        imrR.pack()
        imrR.config(command = lambda: start_record(imr), text = "Record",state=DISABLED)
        print(imrV.get())
        functions[imr] = imrV.get()
        saveF()

def mrpF(event):
    global functions
    if mrpV.get() == "custom keys":
        mrpV.set("custom keys")
        mrpR.config(command =lambda: start_record(mrp), text = "Add key", state=NORMAL)
        mrpE.config(text="Click below to custom your shortcut")
        functions[mrp] = []
        saveF()
    elif mrpV.get() == "Open website":
        mrpE.config(text="Click below to enter url")
        mrpV.set("Open website")
        mrpR.config(command = lambda: website(mrp), text = "Add link", state=NORMAL)
    elif mrpV.get() == 'Dictionary':
        mrpE.config(text="Click button below for instruction")
        mrpR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[mrp] = "Dictionary"
        saveF()
    elif mrpV.get() == "custom text":
        print("work")
        mrpE.config(text="Click below to enter text")
        mrpV.set("custom text")
        mrpR.config(command = lambda: text(mrp), text = "Add text", state=NORMAL)
    elif mrpV.get() == 'Open file/application':
        mrpV.set("Open file/application")
        mrpE.config(text="Click below to choose file")
        mrpR.config(command = lambda:openApp(mrp), text = "Select file/application", state=NORMAL)
    else:
        mrpR.pack()
        mrpR.config(command = lambda: start_record(mrp), text = "Record",state=DISABLED)
        print(mrpV.get())
        functions[mrp] = mrpV.get()
        saveF()

def timF(event):
    global functions
    if timV.get() == "custom keys":
        timV.set("custom keys")
        timR.config(command =lambda: start_record(tim), text = "Add key", state=NORMAL)
        timE.config(text="Click below to custom your shortcut")
        functions[tim] = []
        saveF()
    elif timV.get() == "Open website":
        timE.config(text="Click below to enter url")
        timV.set("Open website")
        timR.config(command = lambda: website(tim), text = "Add link", state=NORMAL)
    elif timV.get() == 'Dictionary':
        timE.config(text="Click button below for instruction")
        timR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[tim] = "Dictionary"
        saveF()
    elif timV.get() == "custom text":
        print("work")
        timE.config(text="Click below to enter text")
        timV.set("custom text")
        timR.config(command = lambda: text(tim), text = "Add text", state=NORMAL)
    elif timV.get() == 'Open file/application':
        timV.set("Open file/application")
        timE.config(text="Click below to choose file")
        timR.config(command = lambda:openApp(tim), text = "Select file/application", state=NORMAL)
    else:
        timR.pack()
        timR.config(command = lambda: start_record(tim), text = "Record",state=DISABLED)
        print(timV.get())
        functions[tim] = timV.get()
        saveF()

def fourF(event):
    global functions
    if fourV.get() == "custom keys":
        fourV.set("custom keys")
        fourR.config(command =lambda: start_record(four), text = "Add key", state=NORMAL)
        fourE.config(text="Click below to custom your shortcut")
        functions[four] = []
        saveF()
    elif fourV.get() == "Open website":
        fourE.config(text="Click below to enter url")
        fourV.set("Open website")
        fourR.config(command = lambda: website(four), text = "Add link", state=NORMAL)
    elif fourV.get() == 'Dictionary':
        fourE.config(text="Click button below for instruction")
        fourR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[four] = "Dictionary"
        saveF()
    elif fourV.get() == "custom text":
        print("work")
        fourE.config(text="Click below to enter text")
        fourV.set("custom text")
        fourR.config(command = lambda: text(four), text = "Add text", state=NORMAL)
    elif fourV.get() == 'Open file/application':
        fourV.set("Open file/application")
        fourE.config(text="Click below to choose file")
        fourR.config(command = lambda:openApp(four), text = "Select file/application", state=NORMAL)
    else:
        fourR.pack()
        fourR.config(command = lambda: start_record(four), text = "Record",state=DISABLED)
        print(fourV.get())
        functions[four] = fourV.get()
        saveF()

def fiveF(event):
    global functions
    if fiveV.get() == "custom keys":
        fiveV.set("custom keys")
        fiveR.config(command =lambda: start_record(five), text = "Add key", state=NORMAL)
        fiveE.config(text="Click below to custom your shortcut")
        functions[five] = []
        saveF()
    elif fiveV.get() == "Open website":
        fiveE.config(text="Click below to enter url")
        fiveV.set("Open website")
        fiveR.config(command = lambda: website(five), text = "Add link", state=NORMAL)
    elif fiveV.get() == 'Dictionary':
        fiveE.config(text="Click button below for instruction")
        fiveR.config(command = dicInstruction, text = "Instruction", state = NORMAL)
        functions[five] = "Dictionary"
        saveF()
    elif fiveV.get() == "custom text":
        print("work")
        fiveE.config(text="Click below to enter text")
        fiveV.set("custom text")
        fiveR.config(command = lambda: text(five), text = "Add text", state=NORMAL)
    elif fiveV.get() == 'Open file/application':
        fiveV.set("Open file/application")
        fiveE.config(text="Click below to choose file")
        fiveR.config(command = lambda:openApp(five), text = "Select file/application", state=NORMAL)
    else:
        fiveR.pack()
        fiveR.config(command = lambda: start_record(five), text = "Record",state=DISABLED)
        print(fiveV.get())
        functions[five] = fiveV.get()
        saveF()


 
# Index
indexV = StringVar() 
indexL = Label(buttonFrame, text="Index finger's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
indexL.pack()
indexB = ttk.OptionMenu(buttonFrame, indexV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= indexF, style="TMenubutton") 
indexB.pack()
indexE = Label(buttonFrame,bg=background_color,fg=foreground_color) 
indexE.pack()
indexR = Button(buttonFrame, text="record", command= lambda: start_record(0), state=DISABLED, highlightbackground=background_color)
indexR.pack()
 
# Middle
middleV = StringVar()
middleL = Label(buttonFrame, text="Middle finger's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
middleL.pack()
middleB = ttk.OptionMenu(buttonFrame, middleV, "choose a function", "None", "copy", "paste", "custom keys", "custom text", "Open file/application", "Dictionary", "Open website", command=middleF)
middleB.pack()
middleE = Label(buttonFrame,bg=background_color, fg=foreground_color)
middleE.pack()
middleR = Button(buttonFrame, text="record", command= lambda: start_record(1), state = DISABLED, highlightbackground=background_color)
middleR.pack()
 
# Ring
ringV = StringVar()
ringL = Label(buttonFrame, text="Thumb finger's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
ringL.pack()
ringB = ttk.OptionMenu(buttonFrame, ringV, "choose a function", "None", "copy", "paste", "custom keys","custom text", "Open file/application", "Dictionary", "Open website", command=ringF)
ringB.pack()
ringE = Label(buttonFrame,bg=background_color, fg=foreground_color)
ringE.pack()
ringR = Button(buttonFrame, text="record", command= lambda: start_record(2), state=DISABLED, highlightbackground=background_color)
ringR.pack()
# Pinky
pinkyV = StringVar()
pinkyL = Label(buttonFrame, text="Pinky finger's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
pinkyL.pack()
pinkyB = ttk.OptionMenu(buttonFrame, pinkyV, "choose a function", "None", "copy", "paste", "custom keys","custom text", "Open file/application", "Dictionary", "Open website", command=pinkyF)
pinkyB.pack()
pinkyE = Label(buttonFrame,bg=background_color, fg=foreground_color)
pinkyE.pack()
pinkyR = Button(buttonFrame, text="record", command= lambda: start_record(3), state=DISABLED, highlightbackground=background_color)
pinkyR.pack()

# Index + middle
imV = StringVar() #
imL = Label(twofingerFrame, text="Index + middle fingers's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
imL.pack()
imB = ttk.OptionMenu(twofingerFrame, imV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= imF, style="TMenubutton")
imB.pack()
imE = Label(twofingerFrame,bg=background_color,fg=foreground_color) 
imE.pack() 
imR = Button(twofingerFrame, text="record", command= lambda: start_record(im), state=DISABLED, highlightbackground=background_color)
imR.pack()

#Index + pinky
ipV = StringVar() #
ipL = Label(twofingerFrame, text="Index + pinky finger's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
ipL.pack()
ipB = ttk.OptionMenu(twofingerFrame, ipV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= ipF, style="TMenubutton")
ipB.pack()
ipE = Label(twofingerFrame,bg=background_color,fg=foreground_color) 
ipE.pack()  
ipR = Button(twofingerFrame, text="record", command= lambda: start_record(ip), state=DISABLED, highlightbackground=background_color) 
ipR.pack()

#Thumb + index
tiV = StringVar() #
tiL = Label(twofingerFrame, text="Thumb + index finger's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
tiL.pack()
tiB = ttk.OptionMenu(twofingerFrame, tiV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= tiF, style="TMenubutton")
tiB.pack()
tiE = Label(twofingerFrame,bg=background_color,fg=foreground_color) 
tiE.pack() 
tiR = Button(twofingerFrame, text="record", command= lambda: start_record(ti), state=DISABLED, highlightbackground=background_color) 
tiR.pack()

#Middle + ring
mrV = StringVar() 
mrL = Label(twofingerFrame, text="Middle + ring finger's funciton:", font=('Arial', 18),bg=background_color, fg=foreground_color)
mrL.pack()
mrB = ttk.OptionMenu(twofingerFrame, mrV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= mrF, style="TMenubutton")
mrB.pack()
mrE = Label(twofingerFrame,bg=background_color,fg=foreground_color) 
mrE.pack() 
mrR = Button(twofingerFrame, text="record", command= lambda: start_record(mr), state=DISABLED, highlightbackground=background_color) 
mrR.pack()

#Thumb + index + pinky
tipV = StringVar() #
tipL = Label(threefingerFrame, text="Thumb + index + pinky finger's funciton:", font=('Arial', 15),bg=background_color, fg=foreground_color)
tipL.pack()
tipB = ttk.OptionMenu(threefingerFrame, tipV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= tipF, style="TMenubutton")
tipB.pack()
tipE = Label(threefingerFrame,bg=background_color,fg=foreground_color) 
tipE.pack() 
tipR = Button(threefingerFrame, text="record", command= lambda: start_record(0), state=DISABLED, highlightbackground=background_color) 
tipR.pack()

#Index + middle + ring
imrV = StringVar() #
imrL = Label(threefingerFrame, text="Index + middle + ring finger's funciton:", font=('Arial', 15),bg=background_color, fg=foreground_color)
imrL.pack()
imrB = ttk.OptionMenu(threefingerFrame, imrV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= imrF, style="TMenubutton")
imrB.pack()
imrE = Label(threefingerFrame,bg=background_color,fg=foreground_color) 
imrE.pack() 
imrR = Button(threefingerFrame, text="record", command= lambda: start_record(0), state=DISABLED, highlightbackground=background_color) 
imrR.pack()

#Middle + ring + pinky
mrpV = StringVar() #
mrpL = Label(threefingerFrame, text="Middle + ring + pinky finger's funciton:", font=('Arial', 15),bg=background_color, fg=foreground_color)
mrpL.pack()
mrpB = ttk.OptionMenu(threefingerFrame, mrpV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= mrpF, style="TMenubutton")
mrpB.pack()
mrpE = Label(threefingerFrame,bg=background_color,fg=foreground_color) 
mrpE.pack() 
mrpR = Button(threefingerFrame, text="record", command= lambda: start_record(0), state=DISABLED, highlightbackground=background_color) 
mrpR.pack()

#Thumb + index + middle
timV = StringVar() #
timL = Label(threefingerFrame, text="Thumb + index + middle finger's funciton:", font=('Arial', 15),bg=background_color, fg=foreground_color)
timL.pack()
timB = ttk.OptionMenu(threefingerFrame, timV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= timF, style="TMenubutton")
timB.pack()
timE = Label(threefingerFrame,bg=background_color,fg=foreground_color) 
timE.pack() 
timR = Button(threefingerFrame, text="record", command= lambda: start_record(0), state=DISABLED, highlightbackground=background_color) 
timR.pack()
#Index + middle + ring + pinky
fourV = StringVar() #
fourL = Label(fourfingerFrame, text="Index + middle + ring + pinky finger's funciton:", font=('Arial', 13),bg=background_color, fg=foreground_color)
fourL.pack()
fourB = ttk.OptionMenu(fourfingerFrame, fourV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= fourF, style="TMenubutton")
fourB.pack()
fourE = Label(fourfingerFrame,bg=background_color,fg=foreground_color) 
fourE.pack() 
fourR = Button(fourfingerFrame, text="record", command= lambda: start_record(0), state=DISABLED, highlightbackground=background_color) 
fourR.pack()

#5 fingers
fiveV = StringVar() #
fiveL = Label(fourfingerFrame, text="5 fingers' funciton:", font=('Arial', 17),bg=background_color, fg=foreground_color)
fiveL.pack()
fiveB = ttk.OptionMenu(fourfingerFrame, fiveV, "choose a function", "None", "copy", "paste", "custom keys","custom text","Open file/application", "Dictionary", "Open website", command= fiveF, style="TMenubutton")
fiveB.pack()
fiveE = Label(fourfingerFrame,bg=background_color,fg=foreground_color) 
fiveE.pack() 
fiveR = Button(fourfingerFrame, text="record", command= lambda: start_record(0), state=DISABLED, highlightbackground=background_color) 
fiveR.pack()

 
pre_control() 
 
handFrame = Frame(win, width=420, height=400, bg=background_color) 
handFrame.pack_propagate(0)
handFrame.pack(side=RIGHT)

try:
    img = Image.open(path) 
except:
    messagebox.showerror("Error in collecting image", "Wrong file type or the files have been moved, please try again")

handimg = Image.open(r"C:\Users\huy24\Documents\Handgesture\hand.png")
img = img.resize((340,360), Image.ANTIALIAS) 
photoImg =  ImageTk.PhotoImage(img) #

img2 = img.crop([340-140, 0, 340, 152])
click_btn = ImageTk.PhotoImage(img2)

bodyB = Button(handFrame, image=photoImg, command= instruction, highlightthickness = 0, pady=0, padx=0)
bodyB.place(x=20,y=0) 

startB = Button(handFrame, image=click_btn, command= startSTOP, highlightthickness = 0, pady=0, padx=0)
startB.place(x=220,y=0) 

mainMenu = Menu(win)
mainMenu2 = Menu(win)
win.config(menu=mainMenu)

def select_file():
    global path
    try:
        path= filedialog.askopenfilename(title="Select an Image")

        img= Image.open(path)
        img = img.resize((340,360), Image.ANTIALIAS) 
        img2 = img.crop([340-140, 0, 340, 152])
        img=ImageTk.PhotoImage(img)
        bodyB.config(image= img)
        bodyB.image= img

        click_btn = ImageTk.PhotoImage(img2)
        startB.config(image= click_btn)
        startB.image= click_btn

        colors[2] = path
        pickle.dump(colors,open("color.dat", "wb"))

    except: 
        messagebox.showerror("Error in collecting image", "Wrong file type or the files have been moved, please try again")



option_menu = Menu(mainMenu, tearoff=0)
image_menu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(labe="Color options", menu=option_menu)
mainMenu.add_cascade(labe="Change background image", menu=image_menu)
option_menu.add_command(label="Change background color", command=primary_color)
option_menu.add_command(label="Change foreground color", command = secondary_color)
option_menu.add_separator()
option_menu.add_command(label='Default color', command=defaultColor)
option_menu.add_command(label = 'Red-white', command = red_white)
option_menu.add_command(label = 'Blue-white', command = blue_white)
image_menu.add_command(label="Select image file", command = select_file) 



win.mainloop()
 
 
 
 
 

