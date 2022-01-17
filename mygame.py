from graphics import *
import random
from math import sqrt



margin = 10
moveIncrement = 15
ballRadius = 15
BOUNCE_WAIT = 1200

BALL_COUNT = 1



class Timer:
    def __init__(self):
        self.value = 0


class Paddle:

    def __init__(self, color, width, height, coordx, win):
        self.color = color
        self.width = width
        self.height = height
        self.x = coordx
        self.shape = Rectangle(Point(self.x - int(self.width / 2), win.getHeight() - margin - self.height),
                               Point(self.x + int(self.width / 2), win.getHeight() - margin))
        self.shape.setFill(self.color)
        self.window = win
        self.shape.draw(self.window)

    def move_left(self):

        if self.x >= int(self.width/2):
            self.x -= moveIncrement
            self.shape.move(-moveIncrement, 0)


    def move_right(self):

        if self.x + int(self.width / 2) <= 300:
            self.x += moveIncrement
            self.shape.move(moveIncrement, 0)




class Bubble:

    def __init__(self,radius,color,axisx,axisy,win):
        self.radius=radius
        self.color=color
        self.axisx=axisx
        self.axisy=axisy
        self.center=Point(self.axisx,self.axisy)
        self.shape=Circle(self.center,self.radius)
        self.window=win
        self.shape.setFill(color)
        self.shape.draw(self.window)

    def explode(self):
        self.shape.undraw()

class Ball:

    def __init__(self, coordx, coordy, color, radius, x_direction, speed, win):
        self.shape = Circle(Point(coordx, coordy), radius)
        self.x = coordx
        self.y = coordy
        self.xMovement = 0  # Current x movement
        self.yMovement = 0  # Current y movement
        self.color = color
        self.window = win
        self.shape.setFill(self.color)
        self.shape.draw(self.window)
        self.radius = radius
        self.timer = 0
        self.x_direction = x_direction  # Initial x direction. This variable will be 0 or 1. 1:right 0:left
        self.speed = speed

    def is_moving(self):

        if self.xMovement != 0 and self.yMovement != 0:
            return True
        else:
            return False

    def bounce(self, gameTimer, minX, maxX, maxY):
        # Calculating x-axis ball movement and bouncing
        # minX: min x coord. of paddle
        # maxX: max x coord. of paddle
        # maxY: max y coord. at which the ball can be move. If it goes further, it falls to the ground.
        self.minx=minX
        self.maxx=maxX
        self.maxy=maxY


        global BOUNCE_WAIT
        gameOver = False

        if gameTimer >= self.timer + BOUNCE_WAIT:
            self.timer = gameTimer

            if int(self.x) <= self.maxx and int(self.x) >= self.minx and int(self.maxy - self.y) <= self.radius and int(self.y) < 600:
                if self.yMovement==1:
                    self.yMovement=-1
            elif self.y > (600 - self.radius):
                gameOver=True

            elif int(self.y) < self.radius:
                self.yMovement=1

            elif int(self.x) <= self.radius:
                self.xMovement = 1
            elif int(300 - self.x) <= self.radius:
                self.xMovement = -1
            if self.yMovement==1:
                self.y += self.speed
            elif self.yMovement==-1:
                self.y -= self.speed

            if self.xMovement == 1:
                self.x += self.speed
            elif self.xMovement == -1:
                self.x -= self.speed
            self.shape.move(self.xMovement * self.speed, self.yMovement * self.speed)



            return gameOver


def main():
    win = GraphWin("19290331 Pong Game", 300, 600)
    win.setCoords(0.0,600.0,300.0,0.0)
    lives = 2
    win.setBackground("Black")
    myPaddle = Paddle("White", 100, 15, 150, win)

    ColorsList = ["Navy", "Red", "Green", "Yellow"]
    BallList = list()
    for i in range(BALL_COUNT):
        rand_speed = random.randint(5, 20)  # random speed for ball


        rand_direction = random.randint(0, 1)  # This variable will be 0 or 1 randomly.
        ball = Ball(myPaddle.x - int(myPaddle.width / 2) + i * 30,
                    win.getHeight() - margin - myPaddle.height - ballRadius, ColorsList[i % 4], ballRadius,
                    rand_direction, rand_speed, win)
        BallList.append(ball)
    bubbleslist=[]
    counter=30
    for i in range(5):
        bubble=Bubble(30,"Red",counter,30,win)
        counter+=60
        bubbleslist.append(bubble)
    counter=30
    for i in range(5):
        bubble=Bubble(30,"Dodgerblue",counter,90,win)
        counter+=60
        bubbleslist.append(bubble)
    counter = 30
    for i in range(5):
        bubble = Bubble(30, "Lime", counter, 150, win)
        counter += 60
        bubbleslist.append(bubble)




    livesCounter = Text(Point(win.getWidth() - int(win.getWidth() / 5), 250), f'Lives -- {lives}')
    livesCounter.setTextColor("Cyan")
    livesCounter.setSize(15)
    livesCounter.draw(win)
    gameTimer = Timer()

    gameOver = False

    while lives > 0:
        while not gameOver:

            keyPress = win.checkKey()
            if keyPress == 'a':
                myPaddle.move_left()

            if keyPress == 'd':
                myPaddle.move_right()

            if keyPress == 'l':  # balls will move faster
                for item in BallList:
                    item.speed += 1

            if keyPress == 'k':  # Balls will move slower. Note that in our case min speed is 2.
                for item in BallList:
                    if item.speed > 2:
                        item.speed -= 1

            if keyPress == 's':  # Initial movement of balls
                for item in BallList:
                    if (not item.is_moving()):
                        if item.x_direction == 1:  # it means ball moves to right in x direction
                            item.xMovement = 1
                        else:  # it means ball moves to left in x direction
                            item.xMovement = -1
                        item.yMovement = -1  # at initial ball moves up in y direction

            gameTimer.value += 1

            for item in BallList:
                for i in bubbleslist:
                    if sqrt((float(item.y) - float(i.axisy)) ** 2 + (float(item.x) - float(i.axisx)) ** 2) <= (float(i.radius) + float(item.radius)):
                        i.explode()
                        bubbleslist.remove(i)
                        break
                gameOver = item.bounce(gameTimer.value, (myPaddle.x - int(myPaddle.width / 2)),
                                       (myPaddle.x + int(myPaddle.width / 2)),
                                       win.getHeight() - margin - myPaddle.height)
                if bubbleslist==[]:
                    gameOver=True

                if gameOver == True:
                    if lives==2 and bubbleslist != []:
                        lives=1
                        livesCounter.setText(f'Lives -- {lives}')
                    elif lives==2 and bubbleslist == []:
                        pass
                    elif lives==1 and bubbleslist==[]:
                        pass
                    elif lives==1 and bubbleslist != []:
                        lives=0
                        livesCounter.setText(f'Lives -- {lives}')
                    break
        while gameOver:
            if lives==2 or (lives==1 and bubbleslist==[]):
                myPaddle.shape.undraw()
                for item in BallList:
                    item.shape.undraw()
                message1=Text(Point(150.0,300.0),"GAME OVER")
                message1.setTextColor("Red")
                message1.setSize(25)
                try:
                    message1.draw(win)
                except GraphicsError:
                    win.close()
                message2 = Text(Point(150.0, 350.0), "YOU WIN!")
                message2.setTextColor("Red")
                message2.setSize(25)
                try:
                    message2.draw(win)
                except GraphicsError:
                    win.close()

                message3 = Text(Point(150.0, 400.0), "Press Any Key to Quit")
                message3.setTextColor("Red")
                message3.setSize(20)
                try:
                    message3.draw(win)
                except GraphicsError:
                    win.close()
                k=win.getKey()

                if k in ["a","q","w","e","r","t","y","u","ı","o","p","ğ","ü","s","d","f","g","h","j","k","l","ş","i","z","x","c","v","b","n","m","ö","ç"]:
                    win.close()
            elif lives==1:
                for i in bubbleslist:
                    i.shape.undraw()
                bubbleslist = []
                counter = 30
                for i in range(5):
                    bubble = Bubble(30, "Deeppink", counter, 30, win)
                    counter += 60
                    bubbleslist.append(bubble)
                counter = 30
                for i in range(5):
                    bubble = Bubble(30, "Deepskyblue", counter, 90, win)
                    counter += 60
                    bubbleslist.append(bubble)
                counter = 30
                for i in range(5):
                    bubble = Bubble(30, "Chocolate", counter, 150, win)
                    counter += 60
                    bubbleslist.append(bubble)
                for i in BallList:
                    i.shape.undraw()
                myPaddle.shape.undraw()
                myPaddle = Paddle("White", 100, 15, 150, win)
                BallList = list()
                for i in range(BALL_COUNT):
                    rand_speed = random.randint(5, 20)  #

                    rand_direction = random.randint(0, 1)  # This variable will be 0 or 1 randomly.
                    ball = Ball(myPaddle.x - int(myPaddle.width / 2) + i * 30,
                                win.getHeight() - margin - myPaddle.height - ballRadius, ColorsList[i % 4],
                                ballRadius,
                                rand_direction, rand_speed, win)
                    BallList.append(ball)


                gameOver = False
                break

            elif lives==0:
                myPaddle.shape.undraw()
                for item in BallList:
                    item.shape.undraw()
                for i in bubbleslist:
                    i.shape.undraw()
                message1 = Text(Point(150.0, 300.0), "GAME OVER")
                message1.setTextColor("Red")
                message1.setSize(25)
                message1.draw(win)
                message2 = Text(Point(150.0, 350.0), "YOU LOST!")
                message2.setTextColor("Red")
                message2.setSize(25)
                message2.draw(win)
                message3 = Text(Point(150.0, 400.0), "Press Any Key to Quit")
                message3.setTextColor("Red")
                message3.setSize(20)
                message3.draw(win)
                k = win.getKey()
                if k in ["a", "q", "w", "e", "r", "t", "y", "u", "ı", "o", "p", "ğ", "ü", "s", "d", "f", "g", "h", "j",
                         "k", "l", "ş", "i", "z", "x", "c", "v", "b", "n", "m", "ö", "ç"]:
                    win.close()


main()