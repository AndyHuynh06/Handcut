
import subprocess
import cv2 
import time 
import numpy as np 
import handtrackingmodule as htm 
import pyautogui 
import pickle 
import keyboard 
import os 
import pyperclip
import webbrowser


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

try:
    functions = pickle.load(open('function.dat', 'rb'))
except:
    functions = ['copy','paste','copy','paste']

print(functions)

def gestureF(n):
    if functions[n] == "copy":
        pyautogui.hotkey('command', 'c')
    elif functions[n] == "None":
        pass
    elif functions[n] == "Dictionary":
        pyautogui.hotkey('command','c') 
        text = pyperclip.paste()
        print("---------")
        print(text)
        print("---------")
        pickle.dump(text,open("dictionary.dat", "wb"))
        p = subprocess.Popen(['python3', 'dictionary.py'])
    elif functions[n] == "paste":
        pyautogui.hotkey('command', 'v') 
    elif type(functions[n]) != type(functions) and functions[n].find("text:") != -1:
        text = functions[n].replace('text:',"") 
        pyautogui.write(text)
    elif type(functions[n]) != type(functions) and functions[n].find("url:") != -1:
        link = functions[n].replace('url:',"") 
        webbrowser.open(link, new=2)
    elif type(functions[n]) != type(functions) and functions[n].find('app:') != 1:
        app = functions[n].replace('app:','') 
        os.system(f"open {app}") 
    else:
        keys = ""
        for i,ele in enumerate(functions[n]):
            if i < len(functions[n])-1:
                keys += ele + "+"
            else:
                keys += ele
        print(keys)
        keyboard.press_and_release(keys) 

cap = cv2.VideoCapture(0) 
 
ptime = 0 
ctime = 0 
 
detector = htm.handDetector() 
 
reload = 0
 
text = ""
 
while True:
    #1 finger
    thumb_up = False
    index_up = False
    middle_up = False
    thumb_up = False
    pinky_up = False
    sth_up = False

    #2finger
    im_up = False
    ti_up = False
    ip_up =False
    mr_up = False

    #3 fingers
    imr_up = False
    tim_up = False
    tip_up = False
    mrp_up = False

    #5 and 4 fingers
    five_up = False
    four_up = False
 
    index = 8
    middle = 12
    thumb = 4
    pinky = 20
    ring = 16
 
    if reload > 0:
        reload -= 1

    success, image = cap.read()

    pre_img = cv2.flip(image, 1) 

    img = detector.findHands(pre_img)
 
    lmList = detector.findPos(pre_img,draw=False) 
    
    if len(lmList) != 0:
        if lmList[6][3] <= -15:
            #5 fingers
            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[2][1] > lmList[4][1] and abs(lmList[2][2] - lmList[4][2]) <= 95 and abs(lmList[8][1] - lmList[12][1]) <= 95  and lmList[20][2] < lmList[18][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and abs(lmList[16][1] - lmList[12][1]) <= 125 and abs(lmList[16][1] - lmList[20][1]) <= 125 and abs(lmList[12][1] - lmList[10][1]) <= 70 and reload == 0:
                five_up = True
                sth_up = True
            #4 fingers
            elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and abs(lmList[8][1] - lmList[12][1]) <= 95 and lmList[20][2] < lmList[18][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and abs(lmList[16][1] - lmList[12][1]) <= 125 and abs(lmList[16][1] - lmList[20][1]) <= 125 and abs(lmList[12][1] - lmList[10][1]) <= 65 and reload == 0:
                four_up = True
                sth_up = True
            #index+middle+ring up
            elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and abs(lmList[8][1] - lmList[12][1]) <= 85 and abs(lmList[16][1] - lmList[12][1]) <= 85 and abs(lmList[12][1] - lmList[10][1]) <= 40 and reload == 0:
                imr_up = True
                sth_up = True
            #thumb+index+middle up
            elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and abs(lmList[8][1] - lmList[12][1]) <= 80 and lmList[2][1] > lmList[4][1] and abs(lmList[2][2] - lmList[4][2]) <= 80 and abs(lmList[12][1] - lmList[10][1]) <= 60 and reload == 0:
                tim_up = True
                sth_up = True
            #thumb+index+pinky up 
            elif lmList[8][2] < lmList[6][2] and lmList[20][2] < lmList[18][2] and lmList[2][1] > lmList[4][1] and reload == 0:
                tip_up = True
                sth_up = True
            #middle+ring+pinky up
            elif lmList[20][2] < lmList[18][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and abs(lmList[16][1] - lmList[12][1]) <= 115 and abs(lmList[16][1] - lmList[20][1]) <= 115 and abs(lmList[12][1] - lmList[10][1]) <= 60 and reload == 0:
                mrp_up = True
                sth_up = True
            #index + thumb up
            elif lmList[8][2] < lmList[6][2] and abs(lmList[8][1] - lmList[6][1]) <= 40 and lmList[2][1] > lmList[4][1] and abs(lmList[2][2] - lmList[4][2]) <= 80 and  reload == 0:
                ti_up = True
                sth_up = True
            #index + middle up
            elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and abs(lmList[8][1] - lmList[12][1]) <= 80 and abs(lmList[4][1] - lmList[12][1]) <= 100 and abs(lmList[12][1] - lmList[10][1]) <= 60 and reload == 0:
                im_up = True
                sth_up = True
            #index + pinky up
            elif lmList[8][2] < lmList[6][2] and lmList[20][2] < lmList[18][2] and reload == 0:
                ip_up = True
                sth_up = True
            #middle + ring up
            elif lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][2] and abs(lmList[16][1] - lmList[12][1]) <= 80 and abs(lmList[12][1] - lmList[10][1]) <= 60 and reload == 0:
                mr_up = True
                sth_up = True
            #index up
            elif lmList[8][2] < lmList[6][2] and abs(lmList[8][1] - lmList[6][1]) <= 50 and lmList[2][1] < lmList[4][1] and reload == 0:
                index_up = True
                sth_up = True
            #middle up
            elif lmList[12][2] < lmList[10][2] and abs(lmList[12][1] - lmList[10][1]) <= 50 and reload == 0:
                middle_up = True
                sth_up = True
            #thumb up
            elif lmList[4][2] < lmList[2][2] and abs(lmList[4][1] - lmList[2][1]) <= 95 and abs(lmList[8][1] - lmList[5][1]) <= 60 and abs(lmList[12][1] - lmList[9][1]) <= 60 and  abs(lmList[16][1] - lmList[13][1]) <= 65  and abs(lmList[20][1] - lmList[17][1]) <= 75 and reload == 0:
                thumb_up = True 
                sth_up = True
            #pinky up
            elif lmList[20][2] < lmList[18][2] and abs(lmList[20][1] - lmList[18][1]) <= 65 and reload == 0:
                pinky_up = True  
                sth_up = True

            if five_up:
                text = "5 fingers"
                gestureF(five)
            elif four_up:
                text = "4 fingers"
                gestureF(four)
            elif imr_up and lmList[6][2] < lmList[pinky][2]:
                text = "Index + middle + ring up"
                gestureF(imr)
            elif tim_up and lmList[6][2] < lmList[ring][2]  and lmList[6][2] < lmList[pinky][2]:
                text = "Thumb + index+ middle up"
                gestureF(tim)
            elif tip_up and lmList[6][2] < lmList[ring][2]  and lmList[6][2] < lmList[middle][2]:
                text = "Thumb + index+ pinky up"
                gestureF(tip)
            elif mrp_up and lmList[14][2] < lmList[index][2]:
                text = "Middle + ring + pinky up"
                gestureF(mrp)
            elif ti_up  and lmList[6][2] < lmList[middle][2]  and lmList[6][2] < lmList[pinky][2]:
                text = "Thumb + index"
                gestureF(ti)
            elif im_up  and lmList[6][2] < lmList[ring][2]  and lmList[6][2] < lmList[pinky][2]:
                text = "Index + middle"
                gestureF(im)
            elif ip_up  and lmList[6][2] < lmList[ring][2]  and lmList[6][2] < lmList[middle][2]:
                text = "Index + pinky"
                gestureF(ip)
            elif mr_up  and lmList[14][2] < lmList[index][2]  and lmList[14][2] < lmList[pinky][2]:
                text = "middle + ring"
                gestureF(mr)
            elif index_up and lmList[6][2] < lmList[middle][2] and lmList[6][2] < lmList[thumb][2]:
                text = "Index"
                gestureF(0)
            elif middle_up and lmList[10][2] < lmList[index][2] and lmList[10][2] < lmList[thumb][2] and lmList[10][2] < lmList[pinky][2]:
                text = "Middle"
                gestureF(1)
            elif thumb_up  and lmList[4][2] < lmList[middle][2] and lmList[4][2] < lmList[index][2] and lmList[4][2] < lmList[pinky][2]:
                text ="thumb"
                gestureF(2)
            elif pinky_up  and lmList[20][2] < lmList[middle][2]  and lmList[20][2] < lmList[index][2]:
                text = "Pinky"
                gestureF(3)
            if sth_up:
                reload = 30
            
    else:
        text = "none"
 
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    scale_percent = 100 # percent of original size
    width = int(pre_img.shape[1] * scale_percent / 100)
    height = int(pre_img.shape[0] * scale_percent / 100)
    dim = (width, height)
  
# resize image
    resized = cv2.resize(pre_img, dim, interpolation = cv2.INTER_AREA)

    cv2.putText(resized, f"FPS: {str(int(fps))}", (10,70), cv2.FONT_HERSHEY_PLAIN, 5, (36,255,12), 2)
    cv2.putText(resized, f"Detected finger: {text}", (10,250), cv2.FONT_HERSHEY_PLAIN, 5, (36,255,12), 2)

    cv2.imshow("Recognitor", resized)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:  # close on ESC key
        cv2.destroyAllWindows()
        break

