from turtle import Turtle , Screen 
from game_paddle import Paddle 
from ball import Ball
from game_score import Score
import time 

screen = Screen() 
screen.bgcolor('green') 
screen.setup(width = 800 , height = 600)
screen.title("ping pong game")
screen.tracer(0)

rlock = 1 
llock= 0

# now making the paddles of our game 

rightPaddle = Paddle((350 , 0))
leftPaddle = Paddle((-350 , 0))
ball = Ball() 
lscore = Score((-50 , 270)) 
rscore = Score((50 , 270))

screen.listen() 

screen.update()
while True:
    screen.onkey(rightPaddle.go_up , "Up") 
    screen.onkey(rightPaddle.come_down , 'Down')
    screen.onkey(leftPaddle.go_up , "w") 
    screen.onkey(leftPaddle.come_down , 's')


    time.sleep(ball.movement_incremeter)
    ball.move_x()
    screen.update()

    if ball.ycor()>280 or ball.ycor() <-280 :
        ball.bounce_y()

    if (ball.distance(rightPaddle)<50 and ball.xcor()>320 and rlock==1):
        ball.bounce_x()
        ball.speed_increase()
        rlock = 0 
        llock = 1

    if (ball.distance(leftPaddle)<50 and ball.xcor()<-320 and llock==1):
        ball.bounce_x()
        ball.speed_increase()
        llock = 0 
        rlock = 1

    if ball.xcor() < -350:
        rscore.scoreIncrement((50 , 270)) 
        ball.move_to_start()

        rlock = 1 
        llock = 0 

    if(ball.xcor() >350):
        lscore.scoreIncrement((-50 , 270)) 
        ball.move_to_start()

        llock = 0 
        rlock = 1


    if ball.xcor()>400 or ball.xcor()<-400:
        ball.move_to_start()


    if lscore.score == 2:
        lscore.playerWinning(f"left Wins!, score = {lscore.score}" , (-60,0)) 
        rscore.erasetext()
        break

    if rscore.score == 2:
        rscore.playerWinning(f"right wins! score = {rscore.score}" , (-60,0))
        lscore.erasetext()
        break


   


screen.mainloop()