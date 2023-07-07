import pickle
from tkinter import *
from tkinter import messagebox
from pynput.keyboard import Key, Listener
import threading
from tkinter import ttk

recordONOFF = False
keys = ""
try:
    functions = pickle.load(open('function.dat', 'rb'))
except:
    functions = ['copy','paste','copy','paste']

num = pickle.load(open('finger.dat', 'rb'))

def saveF():
    global functions
    pickle.dump(functions,open("function.dat", "wb"))
    print(functions)

def record():
    global recordONOFF
    global keys
    global functions
    global num
    if type(functions[num]) == type(functions):
        keys = functions[num]
    else:
        keys = []
    def on_press(key):
        keys.append(str(key).replace('Key.','').replace("'", "").replace('_l', '').replace('_r','').replace('_','').replace('capsock','capslock').replace("cmd", "command"))
        print(keys)
    def on_release(key):
        global keys
                
        functions[num] = keys
        saveF()
        return False

    # Collect events until released
    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


record()