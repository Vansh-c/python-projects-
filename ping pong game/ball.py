from turtle import Turtle 

class Ball(Turtle):
    def __init__(self):
        super().__init__() 
        self.shape("circle") 
        self.color("black")
        self.x = 10 
        self.y = 10 
        self.penup()
        self.speed(2)
        self.goto(self.x , self.y)
        self.movement_incremeter = 0.15  


    def move_x(self):
        newx = self.xcor() +  self.x
        newy = self.ycor() + self.y 
        self.goto(newx , newy)


    def bounce_y(self):
        self.y = -self.y 

    def bounce_x(self):
        self.x = -self.x 
        


    def move_to_start(self):
        self.goto(0,0) 
        self.bounce_x() 
        self.movement_incremeter = 0.2


    def speed_increase(self):
       if self.movement_incremeter>0:
            self.movement_incremeter *=0.90




