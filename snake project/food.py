from  turtle import Turtle 

import random


class Roti(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle') 
        self.color('red') 
        self.penup() 
        self.speed('fastest')
        self.refresh()

        
        

      
    def refresh(self ):
        roti_x = random.randint(-335 , 335) 
        roti_y = random.randint(-335 , 335) 
        self.goto(roti_x , roti_y) 
        





