from tkinter import *
import time
from random import randint

global lives

tk = Tk()



winHeight = 1000
winWidth = 1200

win = Canvas(tk, bg = "white", height=winHeight, width=winWidth)
win.pack()
tk.title("Pang")

global gameMode
gameMode = "player"


def main():
    global lives
    global gameMode
    global gamemodeSwitchTimer
    global gameWinStatus
    global livesNotification
    global BrickHitNotification
    lives = 50
    livesNotification = False
    BrickHitNotification = False
    gameWinStatus = "Loading"
    gamemodeSwitchTimer = 0
    speedMultiplier = 6
    currentBrickCoords = [0,0]

    def rgb_to_hex(r, g, b):
        return ('{:02X}' * 3).format(r, g, b)

    class Ball:
        def __init__(self):
            self.x = winWidth/2 + randint(-150, 150)
            self.y = winHeight/2 + randint(-20, 20)
            self.width = 25
            self.height = 25
            startingDirection = randint(1,2)
            if startingDirection == 1:
                self.xv = 0.7 * speedMultiplier
            elif startingDirection == 2:
                self.xv = -0.7 * speedMultiplier
            self.yv = 0.8 * speedMultiplier
            
        def draw(self):
            return win.create_oval(Ball.x,Ball.y,Ball.x+Ball.width,Ball.y+Ball.height,fill="blue",outline="blue")
        
        def check_collision(self, other):
            return (self.x < other.x + other.width and self.x + self.width > other.x and self.y < other.y + other.height and self.y + self.height > other.y)
            
    Balls = [Ball() for _ in range(1)]

    class Paddle:
        def __init__(self, x, y, width):
            self.x = x
            self.y = y
            self.width = width
            
        def draw(self):
            return win.create_rectangle(paddle1.x, paddle1.y, paddle1.x+paddle1.width, paddle1.y+20, fill = "red")
            
    paddle1 = Paddle(winWidth/2, winHeight - 30, 200)

    class Brick:
        def __init__(self):
            self.x = currentBrickCoords[0]
            self.y = currentBrickCoords[1]
            self.width = 75
            self.height = 45
            if currentBrickCoords[0] < (winWidth - self.width):
                currentBrickCoords[0] += self.width
            else:
                currentBrickCoords[0] = 0
                currentBrickCoords[1] += self.height
            
            self.redValue = randint(0, 255)
            self.greenValue = randint(0, 255)
            self.blueValue = randint(0, 255)
            
        def draw(self):
            self.brickColour = rgb_to_hex(self.redValue, self.greenValue, self.blueValue)
            self.brickColour = "#" + self.brickColour
            return win.create_rectangle(Brick.x, Brick.y, Brick.x+Brick.width, Brick.y+Brick.height, fill = self.brickColour)
        
    Bricks = [Brick() for _ in range(96)]

    class Barrier:
        def __init__(self):
            self.x = winWidth/2 - randint (-400, 400)
            self.y = winHeight/2 - randint(-30, 30)
            self.width = 200
            self.xv = (randint(70, 130) / 100) * speedMultiplier
            
        def draw(self):
            return win.create_rectangle(Barrier.x, Barrier.y, Barrier.x+Barrier.width, Barrier.y+20, fill = "#DC143C")

    Barriers = [Barrier() for _ in range(2)]

    # class PowerUp:
    #     def __init__(self):
    #         self.x = location


    def keyPressed(direction):
        global Ball
        global Paddle
        global gameWinStatus
        global lives
        global gameMode

        if gameMode == "player":
            if direction.keysym == "Left" or direction.keysym == "a":
                paddle1.x = paddle1.x - (6 * speedMultiplier)
                if gameWinStatus == "Loading":
                    gameWinStatus = "ongoing"
            if direction.keysym == "Right" or direction.keysym == "d":
                paddle1.x = paddle1.x + (6 * speedMultiplier)
                if gameWinStatus == "Loading":
                    gameWinStatus = "ongoing"
            if direction.keysym == "w" and paddle1.width <= winWidth - 5:
                paddle1.width = paddle1.width + 5
            if direction.keysym == "s" and paddle1.width >= 10:
                paddle1.width = paddle1.width - 5
            if direction.keysym == "5":
                lives = 1000000000000000
        
        if direction.keysym == "p":
            if gameMode == "player":
                gameMode = "ai"
                print("gamemode is now ai", gameMode)
            elif gameMode == "ai":
                gameMode = "player"
                print("gamemode is now player", gameMode)
            gamemodeSwitchTimer = 500
            

        for Ball in Balls:
            if direction.keysym == "Up":
                Ball.yv = Ball.yv * -1
            if direction.keysym == "Down":
                Ball.xv = Ball.xv * -1
            if direction.keysym == "b":
                Ball.width = Ball.width + 2
                Ball.height = Ball.height + 2
                Ball.x = Ball.x - 1
                Ball.y = Ball.y - 1
            if direction.keysym == "t":
                if Ball.width > 1 and Ball.height > 1:
                    Ball.width = Ball.width - 2
                    Ball.height = Ball.height - 2
                    Ball.x = Ball.x + 1
                    Ball.y = Ball.y + 1

    win.bind("<KeyPress>", keyPressed)
    win.focus_set()
    win.pack()

    restartCounter = 0
    



    while True:
        #print("ballX dimensions are", ballX, "and", ballX + ballWidth, ", ballY dimensions are", ballY, "and", ballY + ballHeight, ", paddle1.x dimensions are", paddle1.x, "and", paddle1.x +paddle1.width, ", paddle1.y is", paddle1.y, "Ball x movement is", xv, ", Ball y movement is", Ball.yv) 
        if gamemodeSwitchTimer > 0:
            gamemodeSwitchTimer -= 1

        if gameMode == "ai" and gameWinStatus == "Loading":
            gameWinStatus = "ongoing"
        
        if gameWinStatus == "ongoing":
            restartCounter = 0
            for Ball in Balls:
                if gameMode == "ai":
                    if paddle1.x + (paddle1.width/2) < Ball.x:
                        paddle1.x += 5
                    elif paddle1.x + (paddle1.width/2) > Ball.x + Ball.width:
                        paddle1.x -= 5
                Ball.x = Ball.x+Ball.xv
                Ball.y = Ball.y+Ball.yv
                
                if Ball.x<0 or Ball.x>winWidth-Ball.width:
                    Ball.xv=Ball.xv*-1
                    #print("------------------------------\nBall hit X barrier\n------------------------------")
                    
                if Ball.y<0:
                    Ball.yv = Ball.yv*-1
                    #print("------------------------------\nBall hit upper Y barrier\n------------------------------")
                    
                if Ball.y >winHeight-Ball.height:
                    #print("------------------------------\nBall hit lower Y barrier, life lost\n------------------------------")
                    lives = lives - 1
                    Ball.x = winWidth/2 + randint(-10,10)
                    Ball.y = winHeight/2
                    
                if paddle1.x < Ball.x< paddle1.x+ paddle1.width and Ball.y+Ball.height>paddle1.y and Ball.y+Ball.height < paddle1.y+10:
                    Ball.yv = Ball.yv * -1
                    #print("------------------------------\nBall has hit paddle\n------------------------------")
                
                for Barrier in Barriers:
                    if ((Ball.x + Ball.width >= Barrier.x) and (Ball.x <= Barrier.x + Barrier.width)) and ((Barrier.y <= Ball.y <= Barrier.y+10) and (not(Barrier.y <= Ball.y+Ball.height <= Barrier.y+10)) or (Barrier.y <= Ball.y+Ball.height <= Barrier.y+10 and(not(Barrier.y <= Ball.y <= Barrier.y+10)))):
                        Ball.yv = Ball.yv * -1
                        #print("------------------------------\nBall has hit Barrier Block on x\n------------------------------")
                    
                    elif ((Ball.y + Ball.height >= Barrier.y) and (Ball.y <= Barrier.y + 10)) and ((Barrier.x <= Ball.x <= Barrier.x+Barrier.width) and (not(Barrier.x <= Ball.x+Ball.width <= Barrier.x+Barrier.width)) or (Barrier.x <= Ball.x+Ball.width <= Barrier.x+Barrier.width and(not(Barrier.x <= Ball.x <= Barrier.x+Barrier.width)))):
                        Ball.xv = Ball.xv * -1
                        #print("------------------------------\nBall has hit Barrier Block on y\n------------------------------")
                    
                    
                for Brick in Bricks:
                    if ((Ball.x + Ball.width >= Brick.x) and (Ball.x <= Brick.x + Brick.width)) and ((Brick.y <= Ball.y+Ball.height <= Brick.y+Brick.height) or (Brick.y <= Ball.y <= Brick.y+Brick.height)):
                        Ball.xv = Ball.xv * -1
                        #print("------------------------------\nBall has hit Brick on x, point gained\n------------------------------")
                        Bricks.remove(Brick)
                    elif ((Ball.y + Ball.height >= Brick.y) and (Ball.y <= Brick.y + Brick.height)) and ((Brick.x <= Ball.x+Ball.width <= Brick.x+Brick.width) or (Brick.x <= Ball.x <= Brick.x+Brick.width)):
                        Ball.yv = Ball.yv * -1
                        #print("------------------------------\nBall has hit Brick on y, point gained\n------------------------------")
                        Bricks.remove(Brick)
            for Barrier in Barriers:
                Barrier.x = Barrier.x+Barrier.xv
                if Barrier.x < 0 or Barrier.x > winWidth - Barrier.width:
                    Barrier.xv = Barrier.xv * -1
                    
        for i in range(len(Balls)):
            for j in range(i+1, len(Balls)):
                if Balls[i].check_collision(Balls[j]):
                    Balls[i].xv, Balls[j].xv = Balls[j].xv, Balls[i].xv
                    Balls[i].yv, Balls[j].yv = Balls[j].yv, Balls[i].yv
                
        if paddle1.x<0:
            paddle1.x = 0
        if paddle1.x>winWidth-paddle1.width:  
            paddle1.x = winWidth-paddle1.width
        for Ball in Balls:
            if Ball.y > winHeight:
                Ball.yv = Ball.yv*-1
            
        win.delete("all")
        
        # livesCount = Label(win, text=f"Lives: {lives}", font = ("Helvetica") )
        # livesCount.place(x=1100,y=50)
        
        # brickCount = Label(win, text=f"Bricks: {len(Bricks)}", font = ("Helvetica") )
        # brickCount.place(x=1100,y=74)
        
        if lives > 0:
            for Ball in Balls:
                Ball.draw()
        elif  lives <= 0:
            if livesNotification == False:
                print("Womp Womp you lost your lives")
                gameWinStatus = "loss"
                livesNotification = True
            gameStatusLabel = Label(win, text = "You win!", font = ("helvetica", 30))
            gameStatusLabel.place(x = 500, y = 75)
            gameStatusLabel.pack()
        paddle1.draw()
        
        for Brick in Bricks:
            Brick.draw()
        if len(Bricks) <= 0:
            if BrickHitNotification == False:
                print("Good job! You hit all the Bricks")
                gameWinStatus = "win"
                BrickHitNotification = True
            gameStatusLabel = Label(win, text = "You win!", font = ("helvetica", 30))
            gameStatusLabel.place(x = 500, y = 75)
            
        for Barrier in Barriers:
            Barrier.draw()
            
        if gameWinStatus == "win":
            for Ball in Balls:
                Ball.width = Ball.width + 3
                Ball.height = Ball.height + 3
                Ball.x = Ball.x - 1.5
                Ball.y = Ball.y - 1.5
        
        if gameWinStatus != "ongoing" and gameWinStatus != "Loading":
            restartCounter += 1
            print(f"Restarting commencing, {restartCounter} out of 1000")
        
        if restartCounter >= 1000:
            print("program restarting")
            main()
        tk.update()
        time.sleep(0.01)


main()

tk.mainloop() 