from turtle import Turtle 

class Score(Turtle):
    def __init__(self , position):
        super().__init__()
        self.score = 0 
        self.color('white')
        self.hideturtle()
        self.penup()
        self.goto(position) 
        self.write(f"Score= {self.score}", font= ("Arial" , 14))
    
        
        


    def scoreIncrement(self , position):
        self.score +=1 
        self.clear() 
        self.goto(position) 
        self.write(f"Score = {self.score}" , font = ("Arial" , 14)) 


    def playerWinning(self, text , position):
        a = self.score 
        self.clear() 
        self.goto(position) 
        self.write(text , font= ("Arial" , 24)) 

    def erasetext(self):
        self.clear()