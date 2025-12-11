from turtle import Turtle , Screen  ; 


starting_position =[(0,0)  , (-20,0) , (-40,0)]

class Snake:
    def __init__(self):
        self.partslist = [] 
        self.placingPositions() 
        self.snakespeed = 10
        
        


    def moveUp(self):
        if self.partslist[0].heading() != 270:
               self.partslist[0].setheading(90)  

    def moveDown(self):
         if self.partslist[0].heading()!=90:
              self.partslist[0].setheading(270) 

    def moveLeft(self):
         if self.partslist[0].heading() != 0:
            self.partslist[0].setheading(180) 


    def moveRight(self):
         if self.partslist[0].heading()!= 180:
              self.partslist[0].setheading(0) 


    def placingPositions(self):
         for pos in starting_position:
              self.createPart(pos)

    def move(self):
         for i in range(len(self.partslist)-1 , 0 , -1):
              pos1 = self.partslist[i-1].xcor() 
              pos2 = self.partslist[i-1].ycor() 
              self.partslist[i].goto(pos1 , pos2) 

         self.partslist[0].forward(self.snakespeed)
              
              


    def createPart(self, position):
         part = Turtle() 
         part.shape('square') 
         part.color('green') 
         part.penup() 
         part.goto(position)
         self.partslist.append(part) 

    def extend_snake(self):
         lastpart = self.partslist[-1].position() 
         self.createPart(lastpart)

         


