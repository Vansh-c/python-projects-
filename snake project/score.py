from turtle import Turtle  


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white') 
        self.score = 0 
        with open('snake project\\highscore.txt', 'r') as file:
            self.highscore  = int(file.read())
        self.penup()
        self.goto(0,320) 
        self.write(f'score = {self.score} , highscore = {self.highscore}' , align='center' , font=('Arial' , 20 , 'normal')) 
        self.hideturtle()

    def increase_score(self):
        self.score+=1 
        self.clear() 

        if self.score > self.highscore :
              with open('snake project\\highscore.txt', 'w') as file:
                  file.write(f'{self.score}')
        self.update_title()


    def update_title(self):
        self.write(f'score = {self.score} , high score = {self.highscore}' , align = 'center' , font=('Arial' , 20 , 'normal')) 

    def game_is_over(self):
        self.goto(0,0)
        self.write('Game Over' , align = "center" , font=('Arial' , 20 , 'normal'))

