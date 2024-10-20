import numpy as np
import matplotlib.pyplot
import tkinter as tk
import requests
from tkinter import PhotoImage, Label
from tkinter import filedialog
from PIL import Image, ImageTk
import random
stopWalk = False

#IMAGE SETUP------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


# Create the main window
root = tk.Tk()
root.title("Desktop Pet")
root.geometry("1200x800")  # Set window size (width x height)

def resize(image_path, width, height):
    # Open the image using Pillow
    img = Image.open(image_path)
    
    # Resize the image
    img_resized = img.resize((width, height))
    
    # Convert the image to a PhotoImage that Tkinter can display
    return ImageTk.PhotoImage(img_resized),width,height


image_path = "oski_image.png"
pet_image,pet_width,pet_height = resize(image_path,200,200)
# Create a label to hold the image
pet_label = tk.Label(root, image=pet_image)
pet_label.place(x=800, y=640)


#MOVEMENT----------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


def petwalk():

    current_x, current_y = pet_label.winfo_x(), pet_label.winfo_y()
    targetLower = current_x-300
    if targetLower < 0:
        targetLower = 0
    targetUpper = current_x+300
    if targetUpper > 1200:
        targetUpper = 1200
    target_x = random.randint(targetLower, targetUpper)
    
    # Calculate the step size for smooth movement
    step_size = 1

    def move_step():
        
        nonlocal current_x
        if current_x > target_x:
            current_x -= step_size
        elif current_x < target_x:
            current_x += step_size
        #print(str(clicked))

        pet_label.place(x=current_x, y=640)

        # Continue moving if we haven't reached the target
        if abs(current_x - target_x) > step_size:
            root.after(100, move_step)  # Adjust speed of movement here
        else: 
            root.after(random.randint(1000,4000),petwalk())
    
    move_step()

#CLICKING----------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


def on_mouse_enter(event):
    print("hello")
    pet_label.config(text="Mouse is over the image",bd="blue")
    stopWalk = True
def on_mouse_leave(event):
    print("bye")
    pet_label.config(text="Mouse is not over the image",bd="red")
    stopWalk = False
    petwalk()


pet_label.bind("<Enter>", on_mouse_enter)
pet_label.bind("<Leave>", on_mouse_leave)



#MOVING----------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------


# Start the pet's walking animation




root.mainloop()

