import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import Tk, Button, PhotoImage
from PIL import Image, ImageTk
import random
import json
import os
balance = 0

class DesktopPetWithPopup:
    def __init__(self, root, window_size=(1200, 800)):
        self.root = root
        self.root.title("Desktop Pet")
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")

        self.stationary_image_path = "pngs/oski front facing.png"
        self.right_animation = ["pngs/right1.png", "pngs/right2.png"]
        self.left_animation = ["pngs/left1.png", "pngs/left2.png"]

        self.pet_image, self.pet_width, self.pet_height = self.resize(self.stationary_image_path, 200, 200)
        self.pet_label = tk.Label(self.root, image=self.pet_image)
        self.pet_label.place(x=800, y=640)

        self.stop_walk = False
        self.walk_after_id = None
        self.current_animation = None
        self.animation_frame = 0

        self.pet_label.bind("<Enter>", self.on_mouse_enter)
        self.pet_label.bind("<Leave>", self.on_mouse_leave)

        # Load and create small images
        self.small_images = []
        self.small_labels = []
        for i in range(5):
            img, _, _ = self.resize("pngs/blank_bubble.png", 30, 30)
            self.small_images.append(img)
            label = tk.Label(self.root, image=img)
            label.bind("<Button-1>", self.on_small_image_click)
            self.small_labels.append(label)

        # Load todo list from file
        self.todo_list = self.load_todo_list()

    @staticmethod
    def resize(image_path, width, height):
        img = Image.open(image_path)
        img_resized = img.resize((width, height))
        return ImageTk.PhotoImage(img_resized), width, height

    def pet_walk(self):
        if not self.stop_walk:
            current_x, current_y = self.pet_label.winfo_x(), self.pet_label.winfo_y()
            target_lower = max(current_x - 300, 0)
            target_upper = min(current_x + 300, 1200)
            target_x = random.randint(target_lower, target_upper)
            
            step_size = 2

            def move_step():
                nonlocal current_x
                if current_x > target_x:
                    current_x -= step_size
                    self.current_animation = self.left_animation
                elif current_x < target_x:
                    current_x += step_size
                    self.current_animation = self.right_animation
                else:
                    self.current_animation = None

                self.pet_label.place(x=current_x, y=640)
                
                if self.current_animation:
                    self.animate_pet()
                
                if abs(current_x - target_x) > step_size:
                    self.walk_after_id = self.root.after(100, move_step)
                else:
                    self.current_animation = None
                    self.update_pet_image(self.stationary_image_path)
                    self.walk_after_id = self.root.after(random.randint(1000, 4000), self.pet_walk)

            move_step()

    def animate_pet(self):
        if self.current_animation:
            self.animation_frame = (self.animation_frame + 1) % len(self.current_animation)
            self.update_pet_image(self.current_animation[self.animation_frame])

    def update_pet_image(self, image_path):
        new_image, _, _ = self.resize(image_path, 200, 200)
        self.pet_label.configure(image=new_image)
        self.pet_label.image = new_image

    def on_mouse_enter(self, event):
        self.stop_walk = True
        if self.walk_after_id is not None:
            self.root.after_cancel(self.walk_after_id)
            self.walk_after_id = None
        self.show_small_images()

    def on_mouse_leave(self, event):
        self.stop_walk = False
        if self.walk_after_id is None:
            self.pet_walk()
        self.hide_small_images()

    def show_small_images(self):
        pet_x = self.pet_label.winfo_x()
        pet_y = self.pet_label.winfo_y()
        center_x = pet_x + self.pet_width // 2
        center_y = pet_y

        num_images = len(self.small_labels)
        radius = 55  # Adjust this value to change the size of the arc
        start_angle = -math.pi  # Start from the top
        angle_step = math.pi / (num_images - 1)  # Distribute evenly across the top half

        for i, label in enumerate(self.small_labels):
            angle = start_angle + i * angle_step
            x = center_x + int(radius * math.cos(angle)) - 20  # 20 is half the width of small images
            y = center_y + int(radius * math.sin(angle)) + 50
            label.place(x=x, y=y)

    def hide_small_images(self):
        for label in self.small_labels:
            label.place_forget()

    def on_small_image_click(self, event):
        if event.widget == self.small_labels[0]:  # Middle right image
            self.pop_up_todo()
        if event.widget == self.small_labels[1]:  # Image 2
            self.pop_up_shop()

    

    def pop_up_shop(self):
        shop_window = tk.Toplevel(self.root)
        shop_window.title("Oski's Shop")
        shop_window.geometry("800x600")
        shop_window.configure(bg='#F0F0F0')

        entry_frame = tk.Frame(shop_window, bg='#F0F0F0')
        entry_frame.place(x=20, y=50, width=800, height=600)

        self.coin_label = tk.Label(shop_window, text=f"Coins: {balance}", font=("Arial", 14), bg='#F0F0F0', fg='black',borderwidth=2)
        self.coin_label.place(x=640, y=50)
        
        pil_image1 = Image.open("/Users/theman1483/Documents/GitHub/Desktoski/pngs/oski_image.png")
        resized_image1 = pil_image1.resize((100, 100))  # Resize to 100x100 pixels
        button_image1 = ImageTk.PhotoImage(resized_image1)

        add_button = tk.Button(entry_frame, image=button_image1, command=self.open_clothing,borderwidth=0)
        add_button.place(x=100, y=100)
        add_button.image = button_image1

        add_button = tk.Button(entry_frame, text="Testing2", command=self.add_task)
        add_button.place(x=200, y=100)

        add_button = tk.Button(entry_frame, text="Testing3", command=self.add_task)
        add_button.place(x=300, y=100)

    def open_clothing(self):
        clothing_window = tk.Toplevel(self.root)
        clothing_window.title("Clothing!")
        clothing_window.geometry("600x400")
        clothing_window.configure(bg='#F0F0F0')
        
        entry_frame = tk.Frame(clothing_window, bg='#F0F0F0')
        entry_frame.place(x=20, y=50, width=600, height=400)


    def pop_up_todo(self):
        todo_window = tk.Toplevel(self.root)
        todo_window.title("Oski's Todo")
        todo_window.geometry("400x500")
        todo_window.configure(bg='#F0F0F0')

        # Create a frame for the todo list
        frame = tk.Frame(todo_window, bg='#F0F0F0')
        frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Create a canvas for scrolling
        canvas = tk.Canvas(frame, bg='#F0F0F0')
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#F0F0F0')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add tasks to the scrollable frame
        for i, task in enumerate(self.todo_list):
            task_frame = tk.Frame(scrollable_frame, bg='#F0F0F0')
            task_frame.pack(fill=tk.X, padx=5, pady=2)

            task_text = tk.Label(task_frame, text=task, bg='#F0F0F0', font=("Helvetica", 12))
            task_text.pack(side=tk.LEFT)

            delete_button = tk.Button(task_frame, text="Delete", command=lambda i=i: self.delete_task(i))
            delete_button.pack(side=tk.RIGHT)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add new task entry and button
        entry_frame = tk.Frame(todo_window, bg='#F0F0F0')
        entry_frame.pack(pady=10, padx=20, fill=tk.X)

        self.new_task_entry = tk.Entry(entry_frame, font=("Helvetica", 12))
        self.new_task_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

        add_button = tk.Button(entry_frame, text="Add Task", command=self.add_task)
        add_button.pack(side=tk.RIGHT)

    def add_task(self):
        new_task = self.new_task_entry.get()
        if new_task:
            self.todo_list.append(new_task)
            self.new_task_entry.delete(0, tk.END)
            self.save_todo_list()
            self.pop_up_todo()  # Refresh the todo list window

    def delete_task(self, index):
        del self.todo_list[index]
        self.save_todo_list()
        self.pop_up_todo()  # Refresh the todo list window

    def load_todo_list(self):
        try:
            with open('todo_list.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_todo_list(self):
        with open('todo_list.json', 'w') as f:
            json.dump(self.todo_list, f)

    def run(self):
        self.pet_walk()
        self.root.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPetWithPopup(root)
    pet.run()