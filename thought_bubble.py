import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import random
import json
import os

class DesktopPetWithPopup:
    def __init__(self, root, image_path, window_size=(1200, 800)):
        self.root = root
        self.root.title("Desktop Pet")
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")

        self.pet_image, self.pet_width, self.pet_height = self.resize(image_path, 200, 200)
        self.pet_label = tk.Label(self.root, image=self.pet_image)
        self.pet_label.place(x=800, y=640)

        self.stop_walk = False
        self.walk_after_id = None

        self.pet_label.bind("<Enter>", self.on_mouse_enter)
        self.pet_label.bind("<Leave>", self.on_mouse_leave)

        # Load and create small images
        self.small_images = []
        self.small_labels = []
        for i in range(5):
            img, _, _ = self.resize("pngs/full_bubble.png", 30, 30)
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
                elif current_x < target_x:
                    current_x += step_size

                self.pet_label.place(x=current_x, y=640)
                
                if abs(current_x - target_x) > step_size:
                    self.walk_after_id = self.root.after(100, move_step)
                else:
                    self.walk_after_id = self.root.after(random.randint(1000, 4000), self.pet_walk)

            move_step()

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
        positions = [
            (pet_x - 20, pet_y - 20),
            (pet_x + 50, pet_y - 30),
            (pet_x + 120, pet_y - 20),
            (pet_x + 190, pet_y + 50),
            (pet_x + 210, pet_y + 120)
        ]
        for label, pos in zip(self.small_labels, positions):
            label.place(x=pos[0], y=pos[1])

    def hide_small_images(self):
        for label in self.small_labels:
            label.place_forget()

    def on_small_image_click(self, event):
        if event.widget == self.small_labels[2]:  # Middle right image
            self.pop_up_todo()

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
    pet = DesktopPetWithPopup(root, "pngs/oski_bear.png")
    pet.run()