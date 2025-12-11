from snake import Snake
from turtle import Turtle , Screen 
import time 
from food import Roti
from score  import Score


scr = Screen() 
scr.setup(700 , 700) 
scr.bgcolor("black") 
scr.title("welcome to play snake-chappati game") 
scr.tracer(0)    


snake = Snake()
scr.listen()
roti = Roti()
score = Score()

game_is_on = True 
while(game_is_on):
    scr.update()


    time.sleep(0.1)
    
    snake.move()
    scr.onkey(snake.moveUp , "Up") 
    scr.onkey(snake.moveDown , "Down") 
    scr.onkey(snake.moveLeft , "Left") 
    scr.onkey(snake.moveRight,  "Right") 

    if snake.partslist[0].distance(roti)<15:
        roti.refresh()
        snake.extend_snake()
        score.increase_score() 



    if snake.partslist[0].xcor()<-335 or snake.partslist[0].ycor()<-335 or snake.partslist[0].ycor()>335 or snake.partslist[0].xcor()>335:
        score.game_is_over()  
        game_is_on = False

    for parts in snake.partslist[0:]:
          
          if snake.partslist[0] == parts:
              pass
          elif  snake.partslist[0].distance(parts)<10:
            score.game_is_over()
            game_is_on = False 



    


        


    
        





scr.exitonclick()

