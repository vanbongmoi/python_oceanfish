import pygame
import random
import time
import threading
import RPi.GPIO as GPIO
button=26
kickcoin=6
atick=19
stick=13
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(atick,GPIO.OUT)
GPIO.setup(stick,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(kickcoin,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(button,GPIO.IN,GPIO.PUD_UP)
GPIO.output(atick,False)
pygame.init()
win = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Ocean Fish")
rocketimg = pygame.image.load('/home/pi/oceanfish/rocket.png')
tamgunimg = pygame.image.load('/home/pi/oceanfish/tam.png')
bg1 = pygame.image.load('/home/pi/oceanfish/bg1.png')
bg2 = pygame.image.load('/home/pi/oceanfish/bg2.png')
gunimg = pygame.image.load('/home/pi/oceanfish/gun.png')
bg3 = pygame.image.load('/home/pi/oceanfish/bg3.png')
mau = pygame.image.load('/home/pi/oceanfish/fire.png')
khungdiem =pygame.image.load('/home/pi/oceanfish/khungdiem.png')
khungca =pygame.image.load('/home/pi/oceanfish/khungca.png')
imgc1 =pygame.image.load('/home/pi/oceanfish/c1.png')
imgc2 =pygame.image.load('/home/pi/oceanfish/c2.png')
mytamgun1 =pygame.image.load('/home/pi/oceanfish/tamgun1.png')
mynfc =pygame.image.load('/home/pi/oceanfish/nfc.png')
clock = pygame.time.Clock()
imgenemy1 =  pygame.image.load('/home/pi/oceanfish/enemy1.png')
imgenemy2 =  pygame.image.load('/home/pi/oceanfish/enemy2.png')
imgenemy3 =  pygame.image.load('/home/pi/oceanfish/enemy3.png')
imgenemy4 =  pygame.image.load('/home/pi/oceanfish/enemy4.png')
imgenemy5 =  pygame.image.load('/home/pi/oceanfish/enemy5.png')
imgenemy6 =  pygame.image.load('/home/pi/oceanfish/enemy6.png')
imgenemy7 =  pygame.image.load('/home/pi/oceanfish/enemy7.png')
imgenemy8 =  pygame.image.load('/home/pi/oceanfish/enemy8.png')
boom =pygame.mixer.Sound('/home/pi/oceanfish/boom.wav')
insertcoin=pygame.mixer.Sound('/home/pi/oceanfish/insertcoin.wav')
music = pygame.mixer.music.load('/home/pi/oceanfish/bgmusic.mp3')
bem=pygame.mixer.Sound('/home/pi/oceanfish/bem.wav')
pygame.mixer.music.play(-5)
thoigian=''
demnguoc=''
messagedemo="DEMO PLAY"
countplaytime=0
countplayday=0
starttime=30
playtime=starttime
playtimedemo=1
countdown=3
countshowticket=5
newgame=False
heso=5
credit=1
minticket=10
yourticket=False
playdemo=False
countstop=0
rockets=[]
crocolist=[]
class crocodile(object):
    def __init__(self,x,y,width,height,img,vel,tk):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.img=img
        self.stoppoint = 1355
        self.stoppoint1 = -105
        self.startpoint=x
        self.startpointy=y
        self.ticket=tk
    def draw(self, win):
        win.blit(self.img, (self.x,self.y))
    def moveup(self):
        if self.x <=self.stoppoint and self.x>=self.stoppoint1: 
            self.x+=self.vel
        else:
            self.x=self.startpoint
            self.y=self.startpointy
class tamgun(object):
    def __init__(self,x,y,width,height,img):
        self.x = x
        self.y = y
        self.width=width
        self.height=height
        self.img=img
        self.startpos=y
    def draw(self,win):
        win.blit(self.img,(self.x,self.y)) 
class rocket(object):
    def __init__(self,x,y,width,height,img,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.img=img
        self.vel=vel
    def draw(self,win):
        win.blit(self.img,(self.x,self.y))             
class blood(object):
    def __init__(self,x,y,width,height,img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height        
        self.img=img
        self.counttam=0
    def draw(self, win):
        win.blit(self.img, (self.x,self.y))
class mygun(object):
    def __init__(self,x,y,width,height,img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height        
        self.img=img
        self.startpos=y
    def draw(self, win):
        win.blit(self.img, (self.x,self.y))
class khungticket(object):
    def __init__(self,x,y,width,height,img):
        self.x = x
        self.y = y
        self.width = width
        self.height = height        
        self.img=img
    def draw(self, win):
        win.blit(self.img, (self.x,self.y))
class playerinfo(object):
    def __init__(self):
        self.coin=0
        self.playtime=0
        self.score=0
        self.returntick=0
        self.btnpress=True
        self.tradiem=False
        self.readticket=0
        self.ticket=0
        self.allowmove=True
        self.allowgun=False
def redrawGameWindow():
    win.blit(bg1, (0,0))   
    win.blit(khungdiem, (50,5))
    win.blit(khungca, (350,5))
    win.blit(mytamgun1, (380,10))
    win.blit(imgc2, (450,10))
    win.blit(imgc1, (680,10))
    win.blit(khungdiem, (50,5)) 
    win.blit(khungdiem, (930,5)) 
    txtscore = font.render('Score: ' + str(playinfo.score), 1, (255,0,0))
    txttime = font.render('Time: ' + thoigian[0:2], 1, (255,0,0))
    txtcoin = font.render('Coin: ' + str(playinfo.coin), 1, (0,120,65))
    txtcountdown = font.render(demnguoc, 1, (255,0,0))
    txtdemo = font.render(messagedemo,1,(255,0,0))
    txtenemy7 = font.render('= '+str(enemy7.ticket),1,(255,255,255))
    txtenemy8 = font.render('= '+str(enemy8.ticket),1,(255,255,255))
    txtplayday = font.render(str(countplayday),1,(0,0,0))  
    win.blit(txttime, (100, 23))
    for cro in crocolist:
            cro.draw(win)
    win.blit(bg2, (0,0))
    for r in rockets:
        r.draw(win)
    gun.draw(win)
    mytamgun.draw(win)  
    win.blit(bg3, (0,0))
    win.blit(txtscore, (980, 23))    
    mykhung.draw(win)
    nfc.draw(win)    
    win.blit(txtplayday,(10,650))
    win.blit(txtenemy7,(580,20))
    win.blit(txtenemy8,(810,20))
    win.blit(txtdemo,(500,270))
    win.blit(txtcountdown,(530,270))
    win.blit(khungdiem, (450,630)) 
    win.blit(txtcoin,(540,647))
    bl1.draw(win)
    pygame.display.update()
#mainloop

font = pygame.font.SysFont('comicsans', 50, True)
enemy1 = crocodile(0, 110, 150,100,imgenemy1,10,2)
enemy2 = crocodile(-50, 120, 150,100,imgenemy2,8,2)
enemy3 = crocodile(-100, 120, 150,100,imgenemy3,5,2)
enemy4 = crocodile(1000, 110, 150,100,imgenemy4,-10,2)
enemy5 = crocodile(1200, 120, 150,100,imgenemy5,-8,2)
enemy6 = crocodile(1350, 120, 150,100,imgenemy6,-5,2)
enemy7 = crocodile(-100, 100, 150,100,imgenemy7,10,500)
enemy8 = crocodile(-150, 100, 150,100,imgenemy8,10,750)

gun=mygun(525,450,166,224,gunimg)
bl1 = blood(570, -100, 80,80,mau)
mytamgun=tamgun(580,120,60,60,mytamgun1)
nfc = tamgun(1030,450,250,250,mynfc)
mykhung=khungticket(450,-100,300,70,khungdiem)
playinfo=playerinfo()
playinfo.playtime=starttime
run = True
def addplaying():    
    crocolist.append(enemy1)
    crocolist.append(enemy2)
    crocolist.append(enemy3)
    crocolist.append(enemy4)
    crocolist.append(enemy5)
    crocolist.append(enemy6)
def checkticket(num):   
    while True:
        if num<=0:
            if playinfo.readticket<1:
                playinfo.tradiem=False
                GPIO.output(atick,False)
            break    
        num-=1
        pygame.time.delay(1000)        
def returnticket(tk):
    playinfo.ticket=tk
    playinfo.readticket=0
    playinfo.tradiem=True
    GPIO.output(atick,True)
    threadcheckticket=threading.Thread(target=checkticket,name='checkticket',args=[5])
    threadcheckticket.start()
    while playinfo.tradiem:
        if playinfo.readticket>=playinfo.ticket:
            playinfo.tradiem=False
            GPIO.output(atick,False)
        if GPIO.input(stick)==False:
            pygame.time.delay(200)
            playinfo.readticket+=1

def tinhticket(tk):
    myticket = tk/heso
    if myticket<minticket:
        myticket=minticket
    return round(myticket)
def resetcontrol():
    for cr in crocolist:
        cr.x=cr.startpoint
        cr.y=cr.startpointy
    bl1.y=-100
def movefish():
    while True: 
        for cr in crocolist:
            cr.moveup()
        pygame.time.delay(30)
def autorocket():
    boom.play()
    if gun.y<480:
        gun.y+=30
        mytamgun.y+=30
    if len(rockets)<3:
        rockets.append(rocket(570,450,80,160,rocketimg,330))
def checkbutton():
    countstopfire=0
    while True:
        if GPIO.input(button)!=False:
            countstopfire=0
            playinfo.allowgun=True
        if playinfo.allowgun:
            if playinfo.btnpress:                
                playinfo.btnpress=False        
                if GPIO.input(button)==False:
                    countstopfire+=1
                    boom.play()
                    if gun.y<480:
                        gun.y+=30
                        mytamgun.y+=30
                    if len(rockets)<3:
                        rockets.append(rocket(570,450,80,160,rocketimg,330))                             
                pygame.time.delay(30)
                playinfo.btnpress=True
                if countstopfire>3:                    
                    playinfo.allowgun=False                    
addplaying()
def checkcointhread():
    while True:        
        if GPIO.input(kickcoin)==False:            
            playinfo.coin+=credit
            insertcoin.play()
            pygame.time.delay(200)
cointhread=threading.Thread(target=checkcointhread,name="check coin")
cointhread.start()
threadmovefish=threading.Thread(target=movefish,name='move fish')
threadmovefish.start()
btnthread=threading.Thread(target=checkbutton)
btnthread.start()
while run:
    clock.tick(27)    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False      
    if gun.y>450:
        gun.y-=30
        mytamgun.y-=30
    if bl1.y>0:
        bl1.y=-100
    for r in rockets:
        if  r.y>120:
            r.y-=r.vel
        else:
            for cro in crocolist:
                if r.x+(r.width/2)>=cro.x and r.x<=cro.x+cro.width:
                    cro.x=cro.startpoint
                    bem.play()
                    playinfo.score+=cro.ticket
                    if crocolist.index(cro)>=6:
                        crocolist.pop(crocolist.index(cro))
                    bl1.y=110
            rockets.pop(rockets.index(r))
    if newgame:
        if playinfo.playtime>0:
            thoigian=str(round(playinfo.playtime))
            playinfo.playtime-=0.15           
        else:
            playinfo.allowgun=False
            yourticket=True   
            playinfo.returntick=tinhticket(playinfo.score)
            mykhung.y=250
            messagedemo="Ticket: " + str(playinfo.returntick) 
            pygame.mixer.music.stop()
    else:
        if playinfo.coin>0:
            nfc.x=1300
            pygame.mixer.music.stop()
            messagedemo=""
            playdemo=False
            countdown-=0.15
            playinfo.score=0
            demnguoc='Ready '+ str(round(countdown))            
            if countdown<=0:
                music = pygame.mixer.music.load('/home/pi/oceanfish/playmusic.mp3')
                pygame.mixer.music.play(-10)
                countdown=3
                demnguoc=''
                newgame=True
                playinfo.allowgun=True               
                playinfo.coin-=1
                countplaytime+=1
                countplayday+=1
                if countplaytime==10:                    
                    crocolist.append(enemy7)
                if countplaytime>=20:
                    countplaytime=0
                    crocolist.append(enemy8)
        else:
            newgame=False
            playdemo=True
    if yourticket:
        resetcontrol()
        if countshowticket>0:
            countshowticket-=0.2
        else:            
            music = pygame.mixer.music.load('/home/pi/oceanfish/bgmusic.mp3')
            pygame.mixer.music.play(-10)    
            mykhung.y=-100
            newgame=False
            yourticket=False
            playinfo.playtime=starttime
            playinfo.score=0            
            countshowticket=5
            playdemo=True
            messagedemo="DEMO PLAY"
            returnticket(playinfo.returntick)
    if playdemo:
        nfc.x=1030
        if playinfo.score>100:
            playinfo.score=0
        playtimedemo-=0.1
        if playtimedemo<=0:
            playtimedemo=1
            autorocket() 
    redrawGameWindow()
pygame.quit()
