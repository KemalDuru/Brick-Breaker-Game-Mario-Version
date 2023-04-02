from tkinter import *
import time
import random
from PIL import Image, ImageTk


MINX = 0
MINY = 0
MAXX = 800
MAXY = 600

gameover = False
totalBricks = 24
startGame = False
brickPosX = 0
brickPosY = 0
score = 0
lose = 0
win = 0
posBallX = 400
posBallY = 450
moveYFactor = 1
moveXFactor = 0.5
directionY = -1
directionX = -1
posX = 500
posY = 550
Bricks = []


bgcolor = 'blue'
tkd = Tk()

C = Canvas(tkd, bg="blue", height=600, width=800)
tkd.resizable(width=False, height=False)
tkd.title('Brick Game')
C.pack()

texture = Image.open("resim.jpg")
texture_photo = ImageTk.PhotoImage(texture)
texture_photo = ImageTk.PhotoImage(texture.resize((50, 50)))

köstext = Image.open("mario.png")
mario1 = ImageTk.PhotoImage(köstext)
mario1 = ImageTk.PhotoImage(köstext.resize((200, 100)))
mario2 = ImageTk.PhotoImage(köstext.transpose(
    Image.FLIP_LEFT_RIGHT).resize((200, 100)))
mario3 = ImageTk.PhotoImage(köstext.transpose(
    Image.FLIP_LEFT_RIGHT).resize((500, 500)))

Bar = C.create_image(posX, posY, image=mario1)
BarTop = C.create_rectangle(
    posX-100, posY+50, posX+100, posY-30, fill='', outline='')
Ball = C.create_oval(posBallX, posBallY, posBallX +
                     20, posBallY + 20, fill="red")

score_text = C.create_text(40, 10, text="Score: 0", font=('Helvetica', 14))
# Brickleri Çizdirme

for i in range(totalBricks):
    # Her satırda 8 brick olsun

    brickPosX = 30 + (i % 8) * 100
    brickPosY = 45 + (i // 8) * 80
    brickcord = (brickPosX, brickPosY, brickPosX + 50, brickPosY + 50)
    brick_item = C.create_image(
        brickPosX, brickPosY, image=texture_photo, anchor='nw')
    Bricks.append((brick_item, brickcord))

for i in Bricks:
    print(i, "yukarı")


def move_rect(event):
    global startGame, totalBricks
    # Dikdörtgenin koordinatlarını al
    coords = C.coords(BarTop)
    # Sol tuşuna basıldıysa x koordinatlarını 10 azalt
    if (event.keysym == 'a'):
        if coords[0] - 10 >= 0:
            C.move(Bar, -10, 0)
            C.move(BarTop, -10, 0)
            C.itemconfig(Bar, image=mario1)
    # Sağ tuşuna basıldıysa x koordinatlarını 10 artır
    elif (event.keysym == 'd'):
        if coords[2] + 10 <= C.winfo_width():
            C.move(Bar, 10, 0)
            C.move(BarTop, 10, 0)
            C.itemconfig(Bar, image=mario2)
    # Space tuşuna basıldıysa StartGame i true yap
    elif (event.keysym == 'space'):

        if (startGame == True):
            startGame = False
        else:
            startGame = True
            playGame()
    elif (event.keysym == "r"):
        totalBricks = 0


def win_game():
    global startGame, Bar
    startGame = False
    C.delete("all")
    Bar = C.create_image(300, 300, image=mario3)
    C.create_text(500, 100, text="You Win!", font=('Helvetica', 40))
    C.create_text(600, 200, text="DERSİ GEÇTİNİZ :) :)",
                  font=('Helvetica', 30))


def lose_game():
    global startGame, Bar
    startGame = False
    C.delete("all")
    Bar = C.create_image(300, 300, image=mario3)
    C.create_text(400, 300, text="LOSE GAME!", font=('Helvetica', 40))


def update_score(points):
    C.itemconfig(score_text, text="Score: {}".format(points))


def move_brick_down(brick_item, brick):
    global score
    C.move(brick_item, 0, 2)
    brickCord = C.coords(brick_item)
    if brickCord[1] <= MAXY:
        C.after(10, move_brick_down, brick_item, brick)
    else:
        C.delete(brick_item)
        Bricks.remove(brick)


def playGame():
    global directionY, directionX, startGame, Ball, Bar, win, score, Bricks, totalBricks

    if (startGame):

        barCord = C.coords(BarTop)
        ballCord = C.coords(Ball)

        for brick in Bricks:
            brick_item, brickCord = brick
            if brickCord[0] <= ballCord[0] + 20 and brickCord[2] >= ballCord[2] - 20:
                if brickCord[1] <= ballCord[1] and brickCord[3] >= ballCord[3]:
                    directionY = -directionY
                    directionX = -directionX
                    C.after(10, move_brick_down, brick_item, brick)
                    totalBricks -= 1
                    score += 10

        if (ballCord[0] <= MINX or ballCord[2] >= MAXX):
            directionX = directionX * (-1)
        if (ballCord[1] <= MINY or ballCord[3] >= MAXY):
            directionY = directionY * (-1)
        if barCord[0] <= ballCord[2] and barCord[2] >= ballCord[0] and barCord[3] >= ballCord[1] and barCord[1] <= ballCord[3]:
            directionY = directionY * (-1)

        if (ballCord[3] >= MAXY):

            lose_game()
        if (totalBricks <= 0):
            win_game()
        tkd.update_idletasks()
        tkd.update()
        C.move(Ball, directionX * moveXFactor, directionY * moveYFactor)

        update_score(score)
        # 10ms sonra playGame() fonksiyonunu tekrar çağır
        tkd.after(3, playGame)


def main():

    ############## Top çizdirme ############

    C.bind_all('<KeyPress-a>', move_rect)
    C.bind_all('<KeyPress-d>', move_rect)
    C.bind_all('<space>', move_rect)
    C.bind_all('<KeyPress-r>', move_rect)
    tkd.mainloop()


main()
