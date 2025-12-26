import tkinter as tk 
from PIL import Image , ImageTk 


# creating main window 
window = tk.Tk() 
window.title("beyblade spinning") 
window.configure(bg = 'black') 
window.minsize(width = 500 , height= 400)


# loading orignal image
orignal_image = Image.open('beyblade2.png').convert('RGBA')
orignal_image = orignal_image.resize((230 , 230) ,resample= Image.LANCZOS)

# labelling to display image 

image_label = tk.Label(window , bg = 'black') 
image_label.pack() 


# control variables 
angle = 0            # current roation angle 
spinning = False   # to know whether beyblade is spinning. 



# animation function 

def animate():
    global angle 
    if spinning :
            rotated =orignal_image.rotate(angle , resample = Image.BICUBIC) 


             # convert to Tkinter image 
            tk_img = ImageTk.PhotoImage(rotated) 

             # updating label 
            image_label.config(image = tk_img) 
            image_label.image = tk_img   # preventing garbage collection . 


             # updating angle . 
            angle = (angle + 24)%360 


            # calling function animate after 50 seconds to keep loop alive . 

    window.after(1 , animate)


# start spinning function 

def start_spin():
      global spinning 
      spinning = True 


# stop spinning 

def stop_spin():
      global spinning 
      spinning = False 


# creating button 
b1 = tk.Button(text = 'START' ,command= start_spin)
b1.pack(side = 'left' , padx = 20)

b2 = tk.Button(text = 'STOP' , command= stop_spin) 
b2.pack(side = 'right' , padx = 20) 


animate() 
window.mainloop()