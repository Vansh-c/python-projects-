from tkinter import * 
from PIL import Image , ImageTk 
import time 
import math 



# defining counting function 
t = 0 

def countingTime(sec):
    minute = math.floor(sec/60) 
    second = int(sec%60) 

    if second < 10:
        second = f"0{second}" 

    if minute<10:
        minute = f'0{minute}'

    showing_time.config(text = f'{minute}:{second}')

    if sec>0:
        global t
        t = window.after(1000 , countingTime , sec-1) 
    else:
        Timer()




# defining how the countdown works .

work_minute = 0.1
break_time = 0.05
long_break = 0.1

s = 0 

def Timer():
    global s
    s = s+1 
    working_seconds = work_minute*60        # here working seconds is working
    shorty_break = break_time*60 
    longy_break = long_break*60   

    if(s%8==0):
        countingTime(longy_break)
        title_label.config(text='BREAK' , fg= 'black')
        stop_spinning()

    elif(s%2==0):
        countingTime(shorty_break) 
        title_label.config(text= 'BREAK' , fg= 'black')
        stop_spinning()



    else:
        countingTime(working_seconds) 
        start_spin()
        title_label.config(text= 'WORK' , fg= 'green')

        marking = '' 
        for i in range(math.floor(s/2)):
            marking  = marking + 'O'

        tickmark.config(text=marking)



# defining resetting function . 
def resetting():
    global t
    if t:
        window.after_cancel(t)
    showing_time.config(text =  "00:00")
    tickmark.config(text = '') 
    title_label.config(text= "Timer") 
    global s 
    s = 0 
    stop_spinning()






    


# this is creating a rough layout for project . 
window = Tk() 
window.title('pomodoro technique') 
window.config(bg = 'pink', padx=30 , pady= 40)

title_label = Label(text = "TIMER" , fg = 'green' , font= ("Arial" , 30) ,bg = 'pink') 
title_label.grid(column=1 , row= 0) 

canvas = Canvas(width = 600 , height= 430 ,bg = 'pink' , highlightthickness=0)
beyblade_img = Image.open("dragoon.png")           # here, Image.open reads our png file . 
beyblade_img = beyblade_img.resize((300,300))              # Image is Pil class pil is pillow which has several methods so we used pil for resizing . 
zoro_photo = ImageTk.PhotoImage(beyblade_img)          # since our image is pillow image that image gets converted to canvas compatible image. 
canvas.image = zoro_photo


storing_img = canvas.create_image(300, 250, image = zoro_photo) 
canvas.grid(column= 1 , row= 1)


# creating our beyblade spinning function 


angle = 0 
isspinning = False 

def animate():
    global angle 
    if isspinning:
        rotation = beyblade_img.rotate(angle , resample= Image.BICUBIC)     # without resample out  animation will look of poor quality . 

        new_image = ImageTk.PhotoImage(rotation) 
        canvas.image = new_image 

        canvas.itemconfig(storing_img, image = new_image)
        angle = (angle+24)%360

    window.after(1, animate)   # using recursion so our beyblade spins . 



# defining starting spin and stop spinning 

def start_spin():
    global isspinning 
    isspinning = True 

def stop_spinning():
    global isspinning 
    isspinning = False 


# creating buttons 

starting_button = Button(text= 'START', highlightthickness=0 , command= Timer) 
starting_button.grid(column= 0 , row= 1) 

reset_button = Button(text = 'END' , highlightthickness= 0 , command= resetting) 
reset_button.grid(column= 2,  row=1)

tickmark =Label(text=' O ' , fg='green' , bg = 'pink' , font=(50))
tickmark.grid(row=3 , column= 1)

# text for showing time 
showing_time = Label(text= "00:00" ,font=("Arial" , 50 , 'bold') , bg= 'pink')
showing_time.grid(row=2,  column=1)



animate()
window.mainloop()
