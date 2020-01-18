#beatz.py
#Reem Boudali, Maggie Maun, KETH WONG

from pygame import *
from math import *
from datetime import datetime

screen = display.set_mode((800,600))
init()

begin = 0
myClock = time.Clock()
beatzFile = open("keith_beatz.txt","w")
mixer.music.load("music/keith.mp3")
mixer.music.play()
startTime = time.get_ticks()
        
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.unicode == "q":
                beatzFile.write(("q:%i \n") %(timer))
            if e.unicode == "w":
                beatzFile.write(("w:%i \n") %(timer))
            if e.unicode == "e":
                beatzFile.write(("e:%i \n") %(timer))
            if e.unicode == "r":
                beatzFile.write(("r:%i \n") %(timer))
            
#================================
    screen.fill((0,0,0))

    
    timer = time.get_ticks()-startTime
    keys = key.get_pressed()

        
#================================

    display.flip()
    myClock.tick(60)
beatzFile.close()
quit()




