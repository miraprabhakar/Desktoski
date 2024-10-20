import tkinter as tk
from PIL import Image, ImageTk
import random

class DesktopPet:
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

    def on_mouse_leave(self, event):
        self.stop_walk = False
        if self.walk_after_id is None:
            self.pet_walk()

    def run(self):
        self.pet_walk()
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root, "pngs/oski_bear.png")
    # pet2 = DesktopPet(root, "pngs/oski_image.png")
    pet.run()