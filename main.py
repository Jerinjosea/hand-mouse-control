import HandTrackingModule as HTM
from collections import deque
import cv2
import mouse
import pyautogui
import time
#Programed by jerin jose a https://github.com/Jerinjosea

w, h = pyautogui.size()[0], pyautogui.size()[1] #find size of screen
cap = cv2.VideoCapture(0)
detector = HTM.handDetector(detectionCon=0.5, trackCon=0.3, maxHands=1) #initialize handDetector class fom handTrackingModule

_, frame = cap.read()
frame_h,frame_w, c = frame.shape #find width and hight of camera image
prev_x, prev_y = h//2, w//2
smoothen = 3 # increase this to smoothen movement or vice versa
sensitivity = 1.5 # increase cursot speed

prev_T = time.time();
move = True # should we move pointer flag

while(cap.isOpened()):
    _, frame = cap.read() #capture a frame
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame, draw=True) # find hands
    Imlist = detector.findPosition(frame, draw=False) # find locations of each finger

    if(len(Imlist)!=0):
        x1, y1 = Imlist[8][1:] # location of index finger
        x2, y2 = Imlist[12][1:] # location of middle finger (not used yet)
        cur_T = time.time() #get current time in seconds
        dynamic_smooth = smoothen-abs(((x1 - prev_x)/(cur_T-prev_T))/1000) # smoothening movement
        mov_x1, mov_y1 = (x1 - prev_x)/dynamic_smooth, (y1 - prev_y)/dynamic_smooth # smoothening movement and getting howmuch pixels finger has moved
        mov_x1, mov_y1 = mov_x1 * sensitivity, mov_y1*sensitivity # adding sensitivity
        #print("speed", (x1 - prev_x)/(cur_T-prev_T)/1000)
        prev_T = cur_T
        prev_x, prev_y = x1, y1
        cur_pos = pyautogui.position() #get current position of mouse pointer
        fingers = detector.fingersUp() #get a matrix with whether a finger is up or down
                                       #for example if index finger is up the array will be [0,1,0,0,0]
        move = True
        
        if fingers[1] and not fingers[2] and move: #check if index finger is up
            #if mov_x1>10 or mov_x1<-10 and mov_y1 >10 or mov_y1<-10:
            if mouse.is_pressed(button='left'): # release button if it is pressed
                mouse.release(button='left')
                print("released left")
            if mouse.is_pressed(button='right'): # same here
                mouse.release(button='right')
                print("released right")
            mouse.move(cur_pos[0]+mov_x1, cur_pos[1]+mov_y1) #move cursor
        #print(mov_x1,mov_y1)

        # left click
        if fingers[1] and fingers[2] and not fingers[3]: 
            if not mouse.is_pressed(button='left'):
                mouse.press(button='left')
                print("pressed left")
                time.sleep(0.2) #give some time for user to pull finger
            mouse.move(cur_pos[0]+mov_x1, cur_pos[1]+mov_y1)
        
        # right click
        if all (x >= 1 for x in fingers):
            if not mouse.is_pressed(button='right'):
                mouse.press(button='right')
                print("pressed right")
                time.sleep(0.2)
            mouse.move(cur_pos[0]+mov_x1, cur_pos[1]+mov_y1)
    else:
        move = False #this is done so that pointer won't freakout when hand disapears and apears again
    
    #print(Imlist)
    cv2.imshow("frame",frame)

    k = cv2.waitKey(10)
    if k == 27:
        break