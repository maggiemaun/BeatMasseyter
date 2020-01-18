#BEAT MASSEYTER
'''
Welcome to Beat Masseyter: the ultimate rhythm-based game! Think you can match all the beats?
Well, we challenge you to. Power through our meme-filled levels and get the highest score to
become the one and only Beat Masseyter. Beat Masseyter is a rhythm-based game where users can
choose one of 10 levels to match specific beats to keys on the keyboard. Points are gained for
correctly-hit beats, and points are deducted for hitting the wrong beat, missing notes, and key-smashing.
'''
from pygame import *
from random import *
from math import *

#==================================

init() #initializes pygame

width, height = 1000,800
screen = display.set_mode((width, height)) #sets parameters for the screen

page = "Start Screen" #page determines what to display on screen, which is start screen at beginning
    
#images --------------
startBackground = image.load("images/startBack.jpg")    #start screen background
start_start = image.load("images/start-start.png")  #highlight for "start" 
start_leaderboard = image.load("images/start-leaderboard.png")  #highlight for "leaderboard" 
start_credits = image.load("images/start-credits.png")  #highlight for "credits"

finalScore = image.load("images/final_score.png")   #end of game
pausePic = image.load("images/pause.png")   #paused game image

scare = image.load("images/jumpscare.jpg") #jumpscare for boss level
jumpscare = transform.scale(scare,(1000,800))
mckenzieAlternate = image.load("images/backgrounds/mckenzie_alternate.jpg") #alternately coloured photo for boss level
mckenzieAv = image.load("images/avatars/mckenzie av.png") #mr.mckenzie's avatar

#bomb explosion for boss level------
boomPics = []  
for i in range(28):
    boomPics += [image.load("images\\bomb\\Explode-05_frame_"+str(i)+".gif")]
    
#buttons ---------------
startB = Rect(422,506,154,51)   
leaderboardB = Rect(320,592,359,51)
creditsB = Rect(395,683,209,51)
backRect = Rect(766,723,234,77)

#variables and images for Selection Screen--------------
up = False #up and down used to determine when up and down arrows have been pressed
down = False
gameLevels=["maggie","henning","tiger","mckenzie","jenny","keith","reem","henry","rahma","tailai"] #order of levels on Song Selection Screen
backgrounds = []
backgroundPics=["Maggie Back.png","Henning Back.png","Tiger Back.png","Mckenzie Back.png","Jenny Back.png","Keith Back.png","Reem Back.png",
                "Henry Back.png","Rahma Back.png","Tailai Back.png"] #the backdrops for each character

for pic in backgroundPics:#loading backgrounds, scaling them, and appending them to levels list so that they can later be used in the selection screen
    background=image.load("images/Selection Screen Backgrounds//"+pic)
    background=transform.scale(background,(1000,800))
    backgrounds.append(background)
    
#messages displayed at end of song, arranged from low score, to average score, to high score
comments = [[("Not even good."),("If you try really hard…"),("Meh.")],  #henning
            [("Well, you see…"),("Oh…Oh…Oh…Ok"),("The Rahmish Empire would accept you")],   #henry
            [("NOOOOOOOOOOOOOOOOOO"),("Oh, nice…!"),("“Jay Chou would be proud”")],  #jenny
            [("Git gud l0l"),("…I’m not going to say anything"),("*Nod*")],     #keith
            [("BOI"),("I mean I guess you have a point"),("Are you an avid player of Beat Masseyter")],  #maggie
            [("Come on, this is supposed to be easy."),("I didn’t think you’d get this far"),("Did you really think I wouldn’t catch you cheating? 0%")],  #mr.mckenzie
            [("It’s fine, it was a bad song anyways"),("Whaaaat? You actually passed?"),("Sssssssssssssssuper job!")],  #rahma
            [("Beep beep delete the program"),("*Whips unenthusiastically*"),("*Dabs furiously*")],  #reem
            [("Bro, you suck."),("Tsk, Tsk, *sharp intake of breath*"),("Awesome score xD")],   #tailai
            [("You have no talent"),("You did pretty good, but remember to always stay modest."),("You may be good, but are you second (*fourth) best in Canada?")]]  #tiger


songLengths = [225,166,73,141,160,148,142,135,174,168] #length of each song in seconds corresponding to players list
players = ["henning","henry","jenny","keith","maggie","mckenzie","rahma","reem","tailai","tiger"] #players in alaphabetical order
scorePos = [(31,495),(778,713),(783,718),(783,746),(42,720),(39,679),(26,686),(31,731),(32,732),(775,749)]  #where the score will be blited

#drawing Start Screen -----------------
def startScreen():
    "function that draws start screen"
    screen.blit(startBackground,(0,0))
    
#drawing Selection Screen--------------------------------------------
def selectScreen():
    "function that draws the selection screen"
    global up,down,backgrounds,gameLevels
    
    if down == True:    #if down arrow is pressed
        first = backgrounds[0]  #rearranging order of levels list so that fourth element changes
        del backgrounds[0]  #fourth element is blitted on screen, so changing it makes selection screen change
        backgrounds = backgrounds+[first]

        firstLevel=gameLevels[0]    #rearranging gameLevels so that
        del gameLevels[0]
        gameLevels=gameLevels+[firstLevel]
        down = False    #making down = False so that the event only occurs once and not several times with one click

    elif up == True:#if up arrow is pressed
        last = backgrounds[-1]
        backgrounds = [last]+backgrounds
        del backgrounds[-1]

        lastLevel=gameLevels[-1]
        gameLevels=[lastLevel]+gameLevels
        del gameLevels[-1]
        up = False  #making up=False for same reason as making down=False
        
    screen.blit(backgrounds[4],(0,0))   #blitting fourth element because it's in middle of screen
    
#Functions for Leaderboard -------------------
def createLeaderboard():
    "function sorts the users scores in case a new user was added to the leaderboard"
    global highscores
    highscores = []
    for name in open ("leaderboard.txt","r"):   #appending username and score to highscores list
        name = name.strip()
        username,scores = name.split(",")[0], int(name.split(",")[1])
        highscores.append([username,scores])
    #sorting highscores list from lowest to highest
    highscores.sort(key=lambda highscores:highscores[1]) #https://stackoverflow.com/questions/17632428/sorting-names-by-their-high-scores

def showLeaderboard():
    "function that draws leaderboard"
    init()
    fnt = font.Font("font/Adidas Half Block 2016.otf",80) #imports fonts to be used within leaderboard
    firstfnt = font.Font("font/Adidas Half Block 2016.otf",120)
    leaderboardPic = image.load("images/leaderboard.jpg")
    screen.blit(leaderboardPic,(0,0))
    createLeaderboard() #creates highscores list 

    firstplace = firstfnt.render("%-8s %7s"%(highscores[-1][0],highscores[-1][1]),True,(0,0,0)) #first place
    secondplace = fnt.render("%-8s %8s"%(highscores[-2][0],highscores[-2][1]),True,(0,0,0))   #second place
    thirdplace = fnt.render("%-8s %8s"%(highscores[-3][0],highscores[-3][1]),True,(0,0,0))  #third place
    screen.blit(firstplace,(200,280))
    screen.blit(secondplace,(200,450))
    screen.blit(thirdplace,(200,580))
    
#For Credits -----------------
def credit():
    "function that draws the creditscreen"
    creditsPic = image.load("images/credits.jpg")
    screen.blit(creditsPic,(0,0))
 
#For Game Screen ------------------
tim = 0  #timer
myClock = time.Clock() #creates an object to help track time


#creating the beats
def fixWrongCombos(letters):
    "rearranging letters in note combos so that they're all in this order: qw,qe,qr,we,wr,er,qwe,qer,qwr,wer,qwer (useful for drawing notes later)"
    wrongCombos=['wq','eq','rq','ew','rw','re','qew','weq','wqe','eqw','ewq','qre','req','rqe','eqr','erq','qrw','rwq','rqw','wrq','wqr','wre','erw','ewr',
            'rew','rwe','qwre','qewr','qerw','qewr','qrwe','qrew','wqer','wqre','weqr','werq','wreq','wrqe','eqwr','eqrw','ewqr','ewrq','erqw','erwq',
            'rqwe','rqew','rweq','rwqe','reqw','rewq']
    
    if letters in wrongCombos[:5]:  #going through the beats list, and if 2-note/3-note combos have wrong order of letters, they're rearranged
        letters=letters[::-1]   #Adam Mehdi-reverses the letters for 2-note combos (wq becomes qw)
    elif letters in wrongCombos[5:10]:  #this part of the list contains all variations of qwe
        letters="qwe"
    elif letters in wrongCombos[10:15]: #this part of the list contains all variations of qer
        letters="qer"
    elif letters in wrongCombos[15:20]: #this part of the list contains all variations of qwr
        letters="qwr"
    elif letters in wrongCombos[20:25]: #this part of the list contains all variations of wer
        letters="wer"
    elif letters in wrongCombos[25:]:
        letters="qwer"
    return letters


beats=[] #2d list containing x position of note, letter, colour, and timestamp
timeStamps=[] #times when the beat hits keyline
letters=[] #letters of the notes

def setUp(character,index):
    'prepares notes, background, and music; character is the level, index is used for the note colours of that level'
    global background,startTime,timeStamps,letters,beats
    beats=[] #resets the beats every time a new level is selected
    letters=[]
    timeStamps=[]
                 #character, note colour for q,w,e,r
    noteColours=[["henning",(255,255,255),(200,220,50),(255,200,50),(50,55,55)],
                 ["henry",(255,0,0),(233,217,22),(121,61,0),(128,0,0)],
                 ["jenny",(255,223,255),(216,191,255),(198,255,255),(221,255,187)],
                 ["keith",(0,0,0),(128,128,128),(192,192,192),(255,255,255)],
                 ["maggie",(80,0,159),(9,151,119),(236,0,118),(0,0,147)],
                 ["mckenzie",(0,0,0),(0,0,0),(0,0,0),(0,0,0)],
                 ["rahma",(255,255,255),(216,55,55),(198,255,255),(221,255,187)],
                 ["reem",(255,0,0),(0,255,0),(255,255,0),(255,128,0)],
                 ["tailai",(128,0,0),(35,0,70),(0,83,41),(168,84,0)],
                 ["tiger",(255,128,0),(0,0,0),(255,255,255),(128,0,0)]]

    for beat in open("beats/%s_beatz.txt"%(character),"r").read().split("\n"): #opens character's beatz file
        beat = beat.strip(" ")
        lett,timeStamp = beat.split(":")
    
        lett=fixWrongCombos(lett)#fixing any incorrect order of letters
        
        if "q" in lett: #q,qw,qe,qr,qwe,qwr,qer
            colour1 =noteColours[index][1]
            x1=440
            colour2=colour3=colour4=x2=x3=x4=0 #setting values to 0 just as placeholders and also to prevent error when appending them to noteBeats

        if "w" in lett: #w,qw,we,wr,qwe,qwr,wer,qwer
            if lett[0]=="w" or lett=="w":   #w,we,wr,wer
                colour1 = noteColours[index][2]
                x1=480
                colour2=colour3=colour4=x2=x3=x4=0
            else:   #if w is second letter
                colour2=noteColours[index][2]
                x2=480
                x3=colour3=x4=colour4=0

        if "e" in lett:#qe,we,er,qwe,qer,wer,qwer
            if lett[0]=="e" or lett=="e":#if first letter is e or letter is e
                colour1=noteColours[index][3]
                x1=520
                x2=x3=x4=colour2=colour3=colour4=0
            elif lett[1]=="e":#if second letter is e
                colour2=noteColours[index][3]
                x2=520
                x3=x4=colour3=colour4=0
            else:#if third letter is e
                colour3=noteColours[index][3]
                x3=520
                x4=colour4=0
                
        if "r" in lett:#r,qr,wr,er,qer,qwr,wer,qwer
            if lett=="r":#if letter is r: no combos have r as first letter
                colour1=noteColours[index][4]
                x1=560
                x2=x3=x4=colour2=colour3=colour4=0
            elif lett[1]=="r":#if second letter is r
                colour2=noteColours[index][4]
                x2=560
                x3=x4=colour3=colour4=0
            elif lett[2]=="r":#if third letter is r
                colour3=noteColours[index][4]
                x3=560
                x4=colour4=0
            else:#if fourth letter is r
                x4=560
                colour4=noteColours[index][4]

        beats.append([x1,x2,x3,x4,lett,colour1,colour2,colour3,colour4,int(timeStamp)])#if there's only 1 note, x2,x3,x4,colour2,colour3,colour4 will all be 0
        timeStamps.append(int(timeStamp))                                           #if there's only 2 notes, x3,x4,colour3,colour4 will equal 0
        letters.append(lett)
    background = image.load("images/backgrounds/%s_background.jpg"%(character))
    mixer.music.load("beats/music/%s.mp3"%(character))
    mixer.music.play()#plays music 
    startTime = time.get_ticks() #records time music starts incase playing is delayed
            
def bossSetUp():
    'setting up notes, background, and music for level 10'
    global background,startTime,timeStamps,letters,beats
    for beat in open("beats/mckenzie_beatz.txt","r").read().split("\n"): #opens mckenzie's file
        beat = beat.strip()
        lett,x,colour,timeStamp = beat.split(":")
        colour= colour.strip("[").strip("]") #colour in text file appears as "[0,0,0]"
        col1,col2,col3 = colour.split(",") #isolates each number so they can be converted into integers
        beats.append([lett,x,(int(col1),int(col2),int(col3)),timeStamp])
        timeStamps.append(int(timeStamp))
        letters.append(lett)
            
    background = image.load("images/backgrounds/mckenzie_background.jpg") #blits the image
    mixer.music.load("beats/music/mckenzie.mp3") #plays the music
    mixer.music.play()  #plays music 
    startTime = time.get_ticks() #records time music starts
    
SONG_END = USEREVENT + 1 #http://www.nerdparadise.com/programming/pygame/part3 
mixer.music.set_endevent(SONG_END)  #sets event for when song ends

def move():
    'drawing notes during gameplay'
    global beats
    
    screen.blit(background,(0,0))
    for b in beats:
        y = 650-(b[9]-tim)*1//4 #5 pixels per 20 ms 5/20 -> 1/4
        move = 0
        move2=0 #move variable for second note
        move3=0 #move variable for third note
        move4=0 #move variable for fourth note
        radius = 25
        if y>=650:
            #brings notes to center
            if 'q' in b[4]:#q always first note in combos it shows up in
                move+=60
            if 'w' in b[4]:#w is either first or second letter
                if b[4]=='w' or b[4][0]=='w':
                    move+=20
                elif b[4][1]=='w':
                    move2+=20
            if 'e' in b[4]:#e is either first, second, or third letter
                if b[4]=='e' or b[4][0]=='e':
                    move-=20
                elif b[4][1]=='e':
                    move2-=20
                else:
                    move3-=20
            if 'r' in b[4]:#r is either first, second, third letter, or fourth letter
                if b[4]=='r':
                    move-=60
                elif b[4][1]=='r':
                    move2-=60
                elif b[4][2]=='r':
                    move3-=60
                else:
                    move4-=60
            radius = (1000-y)//16 #shrinks radius
            if radius <=1:
                radius=1            

        #drawing one circle by default
        draw.circle(screen,b[5],(b[0]+move,y),radius)#b[5] is colour1 and b[0] is x1
        draw.circle(screen,(0,0,0),(b[0]+move,y),radius+1,2)#draws second circle as outline in case circle colour is white
        if len(b[4])>=2:#if there's a combo with 2 or more notes, draw a second note
            draw.circle(screen,b[6],(b[1]+move2,y),radius)#b[6] is colour2 and b[1] is x2
            draw.circle(screen,(0,0,0),(b[1]+move2,y),radius+1,2)
        if len(b[4])>=3:#if there's a combo with 3 or more notes, draw a third note
            draw.circle(screen,b[7],(b[2]+move3,y),radius)#b[7] is colour3 and b[2] is x3
            draw.circle(screen,(0,0,0),(b[2]+move3,y),radius+1,2)
        if len(b[4])==4:#if there's a 4-note combo, draw fourth note
            draw.circle(screen,b[8],(b[3]+move4,y),radius)
            draw.circle(screen,(0,0,0),(b[3]+move4,y),radius+1,2)

def bossMove():
    'moving notes during level 10'
    for b in beats:
         y = 650-(int(b[3])-tim)*1//4 # 5 pixels per 20 ms 5/20 -> 1/4
         radius = 25
         if y>=650:  #past the keyline
             radius = (1000-y)//16 #shrinks radius
             if radius <=1:
                 radius=1 #ensures that the radius will not go into the negatives
         draw.circle(screen,(0,0,0),(int(b[1]),y),radius+1) #black outline
         draw.circle(screen,b[2],(int(b[1]),y),radius)  #actual circle

         #effects
         if tim>120000:
             if 402>randint(0,1300)>400:
                 screen.blit(jumpscare,(0,0)) #the jumpscare to randomly happen any time past 120000
                 
         if tim >60000:
             if randint(0,1300)==400:
                 screen.blit(mckenzieAlternate,(0,0)) #changes the boss level background any time past 60000
                 
         if tim > 30000:
             randomize=randint(0,600)
             randomPos=(randint(0,width),randint(0,height))
             if 53>randomize>50 :
                 for boo in boomPics:
                     screen.blit(boo, randomPos) #sets up a bunch of explosions
             if tim in timeStamps: #transforms and scales the image of McKenzie's avatar
                 mckenzieAvatar = transform.scale(mckenzieAv,(randint(1,300),randint(1,200)))  
                 screen.blit(mckenzieAvatar,randomPos) 
                 if randomize%9==0:
                    mckenzieAvatarTurn = transform.rotate(mckenzieAvatar,randint(1,359))
                    screen.blit(mckenzieAvatarTurn,randomPos)      
            
def timeRem(songLength):
    global tim
    'a function that creates a bar that denotes how long the song is'
    #[(position of message), (colour of messages)]
    markerpos = [[(661,153),(0,0,0)],
                 [(30,172),(255,255,255)],
                 [(650,288),(0,0,0)],
                 [(38,174),(0,0,0)],
                 [(643,144),(255,255,255)],
                 [(28,198),(0,0,0)],
                 [(32,302),(0,0,0)],
                 [(36,260),(255,255,255)],
                 [(638,157),(255,255,255)],
                 [(31,164),(0,0,0)]]
                 
    full = 242  #distance of timebar
    halfway=(songLength*1000/2) #halfway point of song in millisecs
    perFin = mixer.music.get_pos()/(songLength*1000) #current point in song (millisecs)/song's length (secs into millisecs)
    draw.rect(screen,(255,255,255),(125,52,(perFin*full),28)) 
    marker1 = scorefnt.render("30 secs in!",True,markerpos[character][1])
    marker2 = scorefnt.render("1/2 way in!",True,markerpos[character][1])
    marker3 = scorefnt.render("30 secs left!",True,markerpos[character][1])

    if 28000<tim<33000: #30 sec mark
        screen.blit(marker1,markerpos[character][0])
        
    elif halfway-2000<tim<halfway+3000: #halfway mark
        screen.blit(marker2,markerpos[character][0])
        
    elif ((songLength*1000)-32000)<tim < ((songLength*1000)-27000): #30 sec left mark
        screen.blit(marker3,markerpos[character][0])

#init font--------
init()
fnt = font.Font("font/BebasNeue.otf",50)
scorefnt = font.Font("font/BebasNeue.otf",80 )

#End Screen----------------------------------
continueRect = Rect(314,584,370,100)
enterNamePic = image.load("images/enterName.jpg")

#buttons -- 
pauseButtonRect = Rect(17,12,86,86)
resumeButtonRect = Rect(92,528,335,101)
quitButtonRect = Rect(575,528,335,101)

#==================================
PLAYING, PAUSE = 0, 1
state = PLAYING
score = 0
showTimRem = True#used to draw time remaining bar
correctKey = False#used to deliver feedback during gameplay, such as "hit" or "miss" a note
pos = 0

#Game Loop ------------------------
running = True

while running:
    clickUp = False
    keyDown = False
    if page =="Game" or page=="Boss" or page=="Final Score":
        screen.blit(background,(0,0)) #blit gameplay if in gamemode
        
    for evnt in event.get(): 
        if evnt.type == QUIT:
            running = False
            break
        if evnt.type==KEYDOWN:#if a key has been pressed
            keyDown = True

            if page=="Boss":
                score+=randint(-500,500) #randomizes the score
                
            if evnt.key==K_ESCAPE: #if escape key is pressed, close the program
                running=False
                
            elif evnt.key==K_DOWN: #if down arrow pressed
                down = True
                up = False
                
            elif evnt.key==K_UP: #if up arrow is pressed
                up = True
                down = False
                
            elif evnt.key==K_RETURN and page == "Select Screen": #if enter is pressed, the page changes meaning selection screen no longer displayed
                score = 0 #set score and pos to 0 for when you finish a level and select another one
                pos = 0
                character = players.index(gameLevels[4]) #finds player in the alphabetized list
                if character == 5: #"mckenzie"
                    page = "Boss"
                    bossSetUp()
                else:
                    page="Game"
                    setUp(players[character],character)
                showTimRem = True#setting this to True so that time remaining bar drawn whenever player finishes level and starts new one
                
            elif evnt.key==K_LEFT and page =="Select Screen": #if left arrow is pressed in song selection, screen returns to start
                page = "Start Screen"
                
            elif evnt.key==K_LEFT and page =="Leaderboard": #if left arrow is pressed in leaderboard, screen returns to start
                page = "Start Screen"
                
            elif evnt.key==K_LEFT and page =="Credits": #if left arrow is pressed in credits, screen returns to start
                page = "Start Screen"
                
            elif evnt.key==K_LEFT and (page == "Game" or page=="Boss"):#if left arrow pressed during gameplay, page returns to selection screen
                page="Select Screen"
                mixer.music.pause()#music is stopped
                
            if page=="Final Score":
                if score>int(highscores[-3][1]):#if score > than 3rd place            
                    #typing in username
                    if evnt.key == K_BACKSPACE:
                        inputUser = inputUser[:-1]
                    else:
                        inputUser+=evnt.unicode  
                    keyDown = False #making keyDown False so that a letter is only typed once               

        if evnt.type == MOUSEBUTTONUP:
            clickUp = True

        if page=="Game" or page=="Boss":
            showTimRem = True #if you don't set this to true, time remaning bar won't be drawn when finishing a level and starting new one
                                                          
        if keyDown:
            keysClicked=''#Adam Mehdi
            keys=key.get_pressed()#getting state of all keys on keyboard
            if pos<len(timeStamps)-1:
                if abs(timeStamps[pos]-tim)<= 150: #focuses on notes in range
                    if keys[K_q]:
                        keysClicked+='q'

                    if keys[K_w]:
                        keysClicked+='w'

                    if keys[K_e]:
                        keysClicked+='e'

                    if keys[K_r]:
                        keysClicked+='r'

                    keysClicked=fixWrongCombos(keysClicked)#keysClicked is a string containing the keys that have been pressed
                    
                    if keysClicked==letters[pos]:  #if correct keys are hit
                        score+=105*len(letters[pos])  #score*number of notes
                        correctKey=True
                    else:
                        if score>20:#making sure score isn't negative in levels 1-9
                            score-=20
                        correctKey=False
                    pos+=1
                     
                elif abs(timeStamps[pos]-tim) > 150: #notes out of range
                    if keys[K_q] or keys[K_w] or keys[K_e] or keys[K_r]:#player loses points if they buttonmash
                        if score>20:
                            score-= 20
                        
    if evnt.type == SONG_END:  #level is finished
                page = "Final Score"
                inputUser=""
                inputName=""

    #finds the position of the mouse and when it's pressed
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed() 
#===================================
    
    if page == "Start Screen":
        startScreen()#drawing start screen
        #change the pages depending on the button clicked
        if startB.collidepoint(mx,my) and clickUp == True:
            page = "Select Screen"
        if leaderboardB.collidepoint(mx,my) and clickUp == True:
            page = "Leaderboard"
        if creditsB.collidepoint(mx,my) and clickUp == True:
            page = "Credits"
            
        #highlights text in start screen if user hovers over text
        elif startB.collidepoint(mx,my):
            screen.blit(start_start,(0,0)) 
        elif leaderboardB.collidepoint(mx,my):
            screen.blit(start_leaderboard,(0,0))
        elif creditsB.collidepoint(mx,my):
            screen.blit(start_credits,(0,0))
            
    elif page == "Select Screen":
        selectScreen() #draws selection screen
        showTimRem = False #closes off time remainder

    elif page == "Leaderboard":
        showLeaderboard() #draws leaderboard
        if backRect.collidepoint(mx,my) and clickUp == True:
            page = "Start Screen" 

    elif page == "Credits":
        credit()
        if backRect.collidepoint(mx,my) and clickUp == True:
            page = "Start Screen"

    elif page == "Game":
        #pause
        if pauseButtonRect.collidepoint((mx,my))and mb[0]==1:
            state = PAUSE  
            mixer.music.pause() #pauses music
            pauseClickTime = time.get_ticks() #records time music is paused at

        #playing - will only do all the game things if the game is playing
        if state == PLAYING: 
            mixer.music.unpause()
            
            if pos<len(timeStamps)-1: #making sure pos isn't out of range of timeStamps list
                if tim >= int(timeStamps[pos])+100: # kill all notes that are 200ms past due; miss a note
                    pos+=1
                    correctKey=False
                    if score>20:
                        score-=20
                            
            #timer
            tim = time.get_ticks() - startTime #takes away the amount of time it took to navigate through pages, lag, etc.

            #moves notes
            move()

            #draws timebar
            if showTimRem:
                timeRem(songLengths[character])

            #tells user if they got the note or not
            if correctKey and tim>timeStamps[0]:
                feedback=scorefnt.render("Hit",True,(255,255,255))
                screen.blit(feedback,(580,700))
                
            elif correctKey==False and tim>timeStamps[0]:
                feedback=scorefnt.render("Miss",True,(255,255,255))
                screen.blit(feedback,(580,700))

            #blits score
            scorePic = fnt.render(str(score),True,(0,0,0))
            screen.blit(scorePic,(scorePos[character]))
           
        elif state == PAUSE:   #nothing happens if game is paused         
            screen.blit(pausePic,(0,0))
            if resumeButtonRect.collidepoint((mx,my))and mb[0]==1:
                state = PLAYING
                pausedTime = time.get_ticks()-pauseClickTime  #time that game was paused for
                startTime+= pausedTime  #subtract this time from the current time 
            elif quitButtonRect.collidepoint((mx,my)) and mb[0]==1:
                running = False   #closes game
                
    elif page == "Boss":
        #pause
        if pauseButtonRect.collidepoint((mx,my))and mb[0]==1:
            state = PAUSE
            mixer.music.pause() #pauses music
            pauseClickTime = time.get_ticks() #records time music is paused at
            
        if state == PLAYING: 
            mixer.music.unpause() #unpauses the music
            
            #timer
            tim = time.get_ticks() - startTime #takes away the amount of time it took to navigate through pages, lag, etc.

            #moves notes
            bossMove() #mckenzie's special movements

            #draws timebar
            if showTimRem:
                timeRem(songLengths[5]) 

            #blits score
            scorePic = fnt.render(str(score),True,(0,0,0)) 
            screen.blit(scorePic,(scorePos[character]))

            
        elif state == PAUSE:   #nothing happens if game is paused         
            screen.blit(pausePic,(0,0))
            if resumeButtonRect.collidepoint((mx,my))and mb[0]==1:
                state = PLAYING
                pausedTime = time.get_ticks()-pauseClickTime  #time game was paused for
                startTime+= pausedTime  #subtract this time from the current time 
            elif quitButtonRect.collidepoint((mx,my)) and mb[0]==1:
                running = False   #closes game
                
    elif page=="Final Score":
        background = finalScore 
        showTimRem = False #don't show timebar if song is finished

        #showing unique messages based on low,average,or high score
        if score > 14000 :
            if character==5:
                score = 0
            comment = comments[character][2]
            message = fnt.render(comment,True,(255,255,255)) #higher score
            
        elif score > 9500:
            comment = comments[character][1]
            message = fnt.render(comment,True,(255,255,255)) #average score

        else:
            comment = comments[character][0]
            message = fnt.render(comment,True,(255,255,255)) #low score
            
        finalScorePic = fnt.render(str(score),True,(255,255,255))
        screen.blit(finalScorePic,(470,390))
        screen.blit(message,(125,500))
        createLeaderboard() #allows a leaderboard entry
        
        if score>int(highscores[-3][1]):#if score > than 3rd place
            screen.blit(enterNamePic,(0,0))
            inputName =  scorefnt.render("%-8s"%(inputUser),True,(255,255,255))  #name size is maximum 8 characters
            if inputName!="": 
                screen.blit(inputName,(300,400)) 
            if continueRect.collidepoint(mx,my) and clickUp == True:
                leaderboardFile = open("leaderboard.txt","a") 
                leaderboardFile.write("%s,%i\n" %(inputUser,score)) #adds name and score to textFile
                page = "Select Screen" 
                leaderboardFile.close() #closes the file
        else:
            if continueRect.collidepoint(mx,my) and clickUp == True:#returns player to selection screen when clicking continue
                page = "Select Screen"
        
#===================================
    display.flip()  
quit()
