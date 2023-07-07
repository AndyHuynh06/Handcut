import keyboard
from tkinter import *
from tkinter import ttk
from turtle import back
import requests, pyautogui, pyperclip, os, sys
import pynput
from bs4 import BeautifulSoup
import lxml
import pickle
import time

#Chosing color for the app (this section link with my Handtracking application, if you are planning to use this app individually then ignore this section and just define the color that you want)
try:
   colors = pickle.load(open('color.dat', 'rb'))
except:
  colors = ['#87FFD3','#A03863']

#Again this link to my handtracking application. Ignore it!
try:
   text = pickle.load(open('dictionary.dat', 'rb'))
except:
   text = "error"

#setting the color
background_color = colors[0]
foreground_color = colors[1]


#Main dictionary method
def Dictionary(input):
    background_color = colors[0]
    foreground_color = colors[1]

    #replace the "space" in case the user mishighlight it
    text = input.replace(" ","")

    #Example method
    def Example(input):
        #Using beautifulsoup for web srabbing
        url = f"https://sentence.yourdictionary.com/{input}" 
        html_text1 = requests.get(url).text
        soup1 = BeautifulSoup(html_text1, 'lxml')
        examples = soup1.find_all('p', class_ = "sentence-item__text")
        #Write the title for the example sections in the text widget
        def_region.insert(END, "----------------------------------------------------" + "\n", "seperate")
        def_region.insert(END, "Examples sentences:" + "\n", "title")
        examples_list = []
        #Clearing the example strings and write them in the text widget
        for example in examples:
            a =str(example).replace('<p class="sentence-item__text" data-v-ea7db9ee="">', "").replace("</p>", "").replace(f'<strong>{input.lower()}</strong>', f"{input.upper()}").replace(f'<strong>{input.title()}</strong>', f"{input.upper()}")
            print(a)
            print("\n")
            def_region.insert(END, "-" + a + "\n\n", "example")

    #Using beautifulsoup for web srabbing
    url = f"https://www.merriam-webster.com/dictionary/{text}"

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    all_def = soup.find_all('span', class_ = "dt")

    win = Tk()
    win.configure(bg=background_color)

    #Title
    title = Label(win,text="Dictionary", font=('Arial', 50), bg=background_color, fg=foreground_color)
    title.pack()

    #Display definition
    def_frame = Frame(win)
    def_frame.pack()

    #Some style for the user interplace
    style=ttk.Style()
    style.theme_use('classic')
    style.configure("Vertical.TScrollbar", background=foreground_color, bordercolor="red", arrowcolor=foreground_color, troughcolor=background_color)

    scroll_y = ttk.Scrollbar(def_frame, orient="vertical")
    scroll_y.pack(side=RIGHT,fill=Y)
    def_region = Text(def_frame, width=42, height=13, bd=5, relief='groove', wrap='word',bg="#EEE2E2", fg = "black",
                    font=('Arial', 15),
                    yscrollcommand=scroll_y.set)
    def_region.pack()
    scroll_y.config(command= def_region.yview)
    def_region.tag_configure("def", font=('Arial', 15), background="#EEE2E2")
    def_region.tag_configure("example", font=('Arial',15),background="#EEE2E2")
    def_region.tag_configure("title", font=('Arial',25),background="#EEE2E2")
    def_region.tag_configure("seperate", font=('Arial',15),background="#EEE2E2")

    win.geometry(f"300x300")
    win.title(f"Definition of {text}")

    def_region.insert(END, "Definition" + "\n", "title")

    #Write all the definition after scrabbing into the text widget
    for a_def in all_def:
        try:
            a = a_def.find('span', class_ = 'dtText').text
            def_region.insert(END, a +"." + "\n", "def")
        except:
            pass

    Example(input)
    win.attributes('-topmost', True)
    win.update()
    win.mainloop()




if __name__ == "__main__":
   Dictionary(text)