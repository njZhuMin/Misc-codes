#Be careful with [[0]*m]*n!
#Congratulations to ver 1.1! It's the first usable version(with out lines yet)
#Congratulations to ver 2.0! It's a integrated version
route = "C:\\Users\\Administrator.LOQP9MWIGKQIWNY\\Desktop\\pokelink_v2.0\\"
#Some computers fail to use the local source without giving route

import pygame
from pygame.locals import *
from sys import exit
from random import randint
from math import sin
global screen

pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
#The size of the window is 800*600

BLUE     = (  0,   0, 255)
ORANGE   = (255, 128,   0)

picfile=route + "p"
img=[""]*20
for i in range(0,17):
    img[i]=picfile+str(i)+".png"
#import images of squares

pb=pygame.image.load(route + "pb.png").convert_alpha()
#import a frame

start_background_filename = route + "llk.jpg"
sprite_image_filename = route + "p20.png"
pausepic=pygame.image.load(route + "pause.jpg").convert()
sprite=pygame.image.load(sprite_image_filename).convert_alpha()
back=pygame.image.load(route+"p30.png").convert_alpha()
#use images

global  a,b
bg_img=route + "bg.jpg"
w=800;h=600
a=60.0;b=50.0
size=(w,h)
#set basic parameters

def win():#called when win
    winpic=pygame.image.load(route+"win.jpg").convert()
    screen.blit(winpic,(0,0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
                #exit when the player clicks cross at the top right corner
            if event.type == MOUSEBUTTONDOWN:
                return -1 
                break
            #when the player clicks the mouse,break win() and return -1
            
def lose(con):#called when lose
    losepic=pygame.image.load(route+"lose.jpg").convert()
    screen.blit(losepic,(0,0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit
            if event.type == MOUSEBUTTONDOWN:
                x,y = event.pos
                if x>=51 and x<=261 and y>=482 and y<=553:
                    return -1
                    break
                if x>=539 and x<=749 and y>=482 and y<=553:
                    return con
                    break
                #play the same game again


class square:
    #a class of small squares
    def __init__(self,kind):
        self.kind=kind
        #the parameter "kind" corresponding to a square 
        self.visible=0
        #make squares invisible
        self.image=pygame.image.load(img[kind]).convert_alpha()
        self.location=(0,0)
        #set the initial location of squares
    def remove(self):
        self.visible=0
        self.kind=0
        self.image=pygame.image.load(img[0]).convert_alpha()
        #make it invisible (how)
    def changekind(self,kindb):
        #may be used when we create a stronger one =_=
        self.kind=kindb
        self.image=pygame.image.load(img[kindb]).convert_alpha()


def getp(n,m):
    #get the position of square[n][m]  
    global x0,y0,a
    return(x0+n*a,y0+m*a)

def getp2(n,m):
    global x0,y0,a,b
    return(x0+n*a+0.5*b,y0+m*a+0.5*b)

def antp(x,y):
    #return the row and colum according to the position the mouse clicks
    global x0,y0,a,b
    x1=int((x-x0)/a)
    y1=int((y-y0)/a)
    if (x-x0)-a*x1<=b and (y-y0)-a*y1<=b:
        return x1,y1
    else: return 0,0

def order(a,b):
    #compare a,b and return them in order
    if a<=b: return a,b
    else: return b,a

def link(n1,m1,n2,m2,n,m):
    #this function is used to judge whether two squares can match
    global sq ,p0 ,p1 ,p2 ,p3
    #lazy arithmatic
    p=0

    ra=range(n1,n1-n-2,-1)
    rb=range(n1+1,n+2)
    ra[n1+1:n+2]=rb
    #define the order for searching
    for i in ra:
        q=0
        #search in row
        x,y=order(i,n1)
        for j in range(x,y+1):
            if sq[j][m1].visible==1 and (j,m1)!=(n1,m1) and (j,m1)!=(n2,m2):
            #the link is successful
                q=1;break
        x,y=order(i,n2)
        for j in range(x,y+1):
            if sq[j][m2].visible==1 and (j,m2)!=(n1,m1) and (j,m2)!=(n2,m2):
                q=1;break
        x,y=order(m1,m2)
        for j in range(x,y+1):
            if sq[i][j].visible==1 and (i,j)!=(n1,m1) and (i,j)!=(n2,m2):
                q=1;break
        if q==0:
        #no successful links
            p=1;break
            
    if p==0:
        #search in column
        ra=range(m1,m1-m-2,-1)
        rb=range(m1+1,m+2)
        ra[m1+1:m+2]=rb
        for i in ra:
            q=0
            x,y=order(i,m1)
            for j in range(x,y+1):
                if sq[n1][j].visible==1 and (n1,j)!=(n1,m1) and (n1,j)!=(n2,m2):
                    q=1;break
            x,y=order(i,m2)
            for j in range(x,y+1):
                if sq[n2][j].visible==1 and (n2,j)!=(n1,m1) and (n2,j)!=(n2,m2):
                    q=1;break
            x,y=order(n1,n2)
            for j in range(x,y+1):
                if sq[j][i].visible==1 and (j,i)!=(n1,m1) and (j,i)!=(n2,m2):
                    q=1;break
            if q==0:
                p=2;break

    if p == 0:
        return False
    else:
        if p == 1:
            p1=getp2(i,m1)
            p2=getp2(i,m2)
            #get the central coordinate
        if p == 2:
            p1=getp2(n1,i)
            p2=getp2(n2,i)
        p0=getp2(n1,m1)
        p3=getp2(n2,m2)
        
        return True
  
def click(i,j):
    #used to draw frame
    global screen
    x,y=sq[i][j].location
    x-=(a-b)/2.0
    y-=(a-b)/2.0
    screen.blit(pb,(x,y))

def findlink(n,m):
    #used to help the player find a possible link
    ff=0
    for i1 in range(0,n+2):
        for j1 in range(0, m+2):
            if sq[i1][j1].visible == 1:
                for i2 in range(i1,n+2):
                    for j2 in range(0,m+2):
                        if sq[i2][j2].visible == 1:
                            if sq[i1][j1].kind==sq[i2][j2].kind and (i1,j1)!=(i2,j2) :
                                if link(i1,j1,i2,j2,n,m):
                                    ff=1
                                    break
    if ff == 1:
        return True
    else:
        return False

def draw_links(color):
    #used to draw the link line
    pygame.draw.line(screen,color,p0,p1,5)
    pygame.draw.line(screen,color,p1,p2,5)
    pygame.draw.line(screen,color,p2,p3,5)

def draw_item(i1,i2):
    #draw the buttom of "help" and "reset"
    font = pygame.font.SysFont("arial",28)
    text1 = font.render(str(i1), True, (255,80,80))
    text2 = font.render(str(i2), True, (255,80,80))
    screen.blit(text1,(60,90))
    screen.blit(text2,(60,210))

    item1= pygame.image.load(route+"item1.png").convert_alpha()
    item2= pygame.image.load(route+"item2.png").convert_alpha()

    screen.blit(item1,(15,80))
    screen.blit(item2,(15,200))

    return i1,i2

def llkpause():
    #called when the player wants to pause
    screen.blit(pausepic,(0,0))
    pygame.display.update()

    pp=0
    while pp == 0:
        clock.tick()
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    pp=1
                    break

def resetlink(n,m):
    #called when the player asks to reset the squares randomly
    global sq
    for i in range(1,100*m*n):
        i1=randint(1,n)
        j1=randint(1,m)
        i2=randint(1,n)
        j2=randint(1,m)
        if sq[i1][j1].visible==1 and sq[i2][j2].visible==1 and sq[i1][j1].kind!=sq[i2][j2].kind:
            kind=sq[i1][j1].kind
            sq[i1][j1].kind=sq[i2][j2].kind
            sq[i2][j2].kind=kind
            image=sq[i1][j1].image
            sq[i1][j1].image=sq[i2][j2].image
            sq[i2][j2].image=image

def timer(timelim, elist):
    #a timer
    global time, game 
    time+=clock.tick()/1000.0
    
    pygame.draw.line(screen,(0,100,255),(100,580),(750,580),5)
    #draw the time line
    speed = 600.0/timelim
    #set the speed of a moving subject to time
 
    xsprite = 100 + speed * time
    #make the subject move from the left to the right
    ysprite = 530-abs(10*sin(4*time))
    #make the subject "jump"
    screen.blit(sprite, (xsprite , ysprite))
    
    font1 = pygame.font.SysFont("arial",24)
    text1 = font1.render("Time Left", True, (0,0,0))
    screen.blit(text1,(10,520))

    font2 = pygame.font.SysFont("arial",28)
    text2 = font2.render("%0.2f"%(timelim-time), True, (255,80,80))
    screen.blit(text2,(10,540))
    #show the time left

    for e in elist:
        if e.type ==KEYDOWN:
            if e.key == K_SPACE:
                llkpause()
                
    if time>=timelim:
        game=-1
        #lose when time's up
        
def main(n,m,k,timelim):  # m*n should be even number/m is number of lines and n is number of rows
    global  x0 ,y0 ,sq ,clock ,time, screen ,game 
    clock = pygame.time.Clock()
    #clock is used in the time bar 
    screen=pygame.display.set_mode(size,0,32)

        
    sum=m*n/2
    #total pairs
    k0=[0]*(m*n+99)
    #a list to store all square kinds, 99 is a number to avoid bug

    for i in range(1,sum+1):
        k0[i]=i%k+1;
        k0[i+sum]=i%k+1
    #decide the kinds of squares in pairs according to k

    for i in range(1,100*sum):
        i1=randint(1,m*n)
        i2=randint(1,m*n)
        t=k0[i1]
        k0[i1]=k0[i2]
        k0[i2]=t
    #change the kinds randomly

 
    mid=(w/2.0,h/2.0)
    x0=mid[0]-(n+2)/2.0*a+20
    y0=mid[1]-(m+2)/2.0*a-30
    #set the center of the whole combination of all squares

    sq=[]
    for i in range(0,n+2):
        sqe=[]
        for j in range(0,m+2):
            sqe.append(square(0))
            sqe[j].location=getp(i,j)
        sq.append(sqe)
    #sq[i][j] colum i,row j

    for i in range(1,n+1):
        for j in range(1,m+1):
            sq[i][j]=square(k0[(i-1)*m+j])
            sq[i][j].location=getp(i,j)
            #decide the location of squares
            sq[i][j].visible=1
            #make squares visible

    screen=pygame.display.set_mode(size,0,32)
    bg=pygame.image.load(bg_img).convert()

    p=0
    game=0
    pause = 1
    time = 0.0
    flink =False
    it1=2; it2=2
    #set the tolerant values of these variables

#The most important circulation
    while True:
        event_list=pygame.event.get()
        dec=0
        #a variable to record whether a link is successful
        
        screen.blit(bg,(0,0))
        if p == 1:
            click(np,mp)
            #show frame
        for i in range(1,n+1):
            for j in range(1,m+1):
                if sq[i][j].visible==1:
                    screen.blit(sq[i][j].image,sq[i][j].location)
        #show squares in right location

        for event in event_list:
        #do relevant command
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pause=-pause
            #pause when SPACE is knocked 


            if event.type == MOUSEBUTTONUP:
                x,y=event.pos
                n0,m0=antp(x,y)
                #get the row and colum
                if 1<=n0<=n and 1<=m0<=m and sq[n0][m0].visible==1:
                    if p==0:
                    #no other squares are chosen
                        p=1
                        np=n0;mp=m0
                        
                    else:
                        p=0
                        #cancel the choice if link fails
                        if sq[np][mp].kind==sq[n0][m0].kind and (n0,m0)!=(np,mp):
                            if link(np,mp,n0,m0,n,m):
                            #if the link succeeds
                                sum-=1
                                dec=1
                                sq[np][mp].visible=0
                                sq[n0][m0].visible=0
                                #eliminate the two squares if link succeeds
                                
                if x>=30 and x<=70 and y>=80 and y<=120 and it1>0:
                #get help
                    flink=findlink(n,m)
                    it1-=1
                else:
                    flink=0


                if x>=30 and x<=70 and y>=200 and y<=240 and it2>0:
                #reset the squares randomly
                    resetlink(n,m)
                    it2-=1

                if x>=750 and x<=780  and y>=20 and y<=70:
                    game=-2
                    break
                        
        if dec == 1:
            #show the link and frames
            draw_links(BLUE)
            click(n0,m0)
            click(np,mp)
            screen.blit(sq[n0][m0].image,sq[n0][m0].location)
            screen.blit(sq[np][mp].image,sq[np][mp].location)


        timer(timelim, event_list)

        screen.blit(back,(750,20))
        #show a bottom to return to the beginning screen
        font = pygame.font.SysFont("black",14)
        #set the system font
        text = font.render("return", True, (255,80,80))
        screen.blit(text,(750,50))
        #show the text"return"

        it1,it2= draw_item(it1,it2)
        #it1,it2 are two numbers to store the rest times to get help and reset randomly

        if flink == 1:
            #if there are possible links remain
            draw_links(ORANGE)
            #show one
    
        pygame.display.update()
        if dec == 1:
            time += clock.tick(12)/1000.0
            #remain the link on the screen for a few seconds

        if game<0:
            #lose
            break
        if sum==0:
            #succeed
            game=1;break

    return game


def start():
    level=[]
    level.append((8,6,10,60))
    level.append((10,8,12,80))
    level.append((11,8,15,90))
    level.append((13,13,0,0))
    #four different levels

    start_background = pygame.image.load(start_background_filename).convert()
    x, y = pygame.mouse.get_pos()

    w=0
    con=-1 #a variable means the level
    while True:
        w=0
        if con == -1:
            screen.blit(start_background,(0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    #choose a level 
                    x, y = pygame.mouse.get_pos()
                    if x>=93 and x<=250 and y>=253 and y<=300:
                        con=0
                        n,m,k,t=level[0]
                        w=main(n,m,k,t)
                    if x>=93 and x<=250 and y>=336 and y<=385:
                        con=1
                        n,m,k,t=level[1]
                        w=main(n,m,k,t)
                    if x>=93 and x<=250 and y>=415 and y<=470:
                        con=2
                        n,m,k,t=level[2]
                        w=main(n,m,k,t)
                    if x>=93 and x<=250 and y>=500 and y<=550:
                    #ask the player to input the numbers of rows,columns,kinds of squares and time
                        con=3 
                        n,m,k,t=(13,13,0,0)
                        while (m*n)%2==1:
                            n=13
                            m=13
                            while n<1 or n>12:
                                n=input("Please input the number of lines (1 <= n <= 12)")
                            while m<1 or m>8:
                                m=input("Please input the number of rows (1 <= m <= 8)\n and m*n should be even")
                                
                        while k<1 or k>16:
                            k=input("Please input the number of kinds (1 <= k <= 16)")
                        while t<1 or k>200:
                            t=input("Please input the length of time(seconds)(1 <= t <= 200)")

                        level[3]=n,m,k,t
                        w=main(n,m,k,t)
                    if x>=690 and x<=780 and y>=570 and y<=590:
                        pygame.quit()
                        exit()
                        
        else:
            n,m,k,t=level[con]
            w=main(n,m,k,t)
            #play the same game again
            
        if w==1:
            #win
            con=win()
        elif w==-1:
            #lose
            con=lose(con)
        else:
            con=-1
        pygame.display.update()

start()