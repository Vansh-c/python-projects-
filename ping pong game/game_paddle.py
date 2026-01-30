from turtle import * 


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__() 
        self.shape('square') 
        self.color("red") 
        self.shapesize(stretch_len=1 , stretch_wid=6) 
        self.penup() 
        self.goto(position) 

    def go_up(self):
        y_cor = self.ycor() + 20 
        self.goto(self.xcor() , y_cor) 

    def come_down(self):
        y_cor = self.ycor() -20 
        self.goto(self.xcor() , y_cor) 


