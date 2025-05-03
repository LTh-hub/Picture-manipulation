# app.py


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import time


class CropApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Kvadratisk bildbeskärning")

        self.input_dir = filedialog.askdirectory(title="Välj mapp med originalbilder")
        if not self.input_dir:
            master.destroy()
            return
        self.output_dir = filedialog.askdirectory(title="Välj mapp att spara beskurna bilder")
        if not self.output_dir:
            master.destroy()
            return

        self.image_files = [f for f in os.listdir(self.input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        self.image_index = 0

        self.canvas = tk.Canvas(master, cursor="cross")
        self.canvas.pack()

        self.label_info = tk.Label(master, text="", font=("Arial", 12))
        self.label_info.pack()

        self.label_crop = tk.Label(master, text="", font=("Arial", 12))
        self.label_crop.pack()

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5)

        self.skip_button = tk.Button(self.button_frame, text="Hoppa över", command=self.skip_image)
        self.skip_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=master.quit)
        self.exit_button.pack(side=tk.LEFT, padx=10)

        master.bind("<Key>", self.handle_key)

        self.load_next_image()

    def load_next_image(self):
        if self.image_index >= len(self.image_files):
            print("Inga fler bilder.")
            self.master.quit()
            return

        image_path = os.path.join(self.input_dir, self.image_files[self.image_index])
        self.image = Image.open(image_path)
        self.original_image = self.image.copy()
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        self.image_width, self.image_height = self.image.size
        min_side = min(self.image_width, self.image_height)
        #crop_size = int(min_side * 0.9)
        crop_size = int(min_side - 40)

        self.crop_x = (self.image_width - crop_size) // 2
        self.crop_y = (self.image_height - crop_size) // 2
        self.crop_size = crop_size

        self.draw_crop_rectangle()
        self.update_labels()

    def draw_crop_rectangle(self):
        self.canvas.delete("crop")
        x1 = self.crop_x
        y1 = self.crop_y
        x2 = x1 + self.crop_size
        y2 = y1 + self.crop_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=2, tag="crop")
        self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, outline="lime", width=1, tag="crop")

    def update_labels(self):
        self.label_info.config(text=f"Bildstorlek: {self.image_width} x {self.image_height} px")
        self.label_crop.config(text=f"Maskstorlek: {self.crop_size} x {self.crop_size} px vid ({self.crop_x}, {self.crop_y})")

    def save_crop(self):
        x1 = self.crop_x
        y1 = self.crop_y
        x2 = x1 + self.crop_size
        y2 = y1 + self.crop_size
        cropped = self.original_image.crop((x1, y1, x2, y2))

        filename = self.image_files[self.image_index]
        named_tuple = time.localtime()                                  # get struct_time
        time_string = time.strftime("%Y%m%dT%H%M%S", named_tuple)       # läsbart format
        TxT_fNAME = "SQ-{}-".format(time_string)
        TxT_fNAME = TxT_fNAME + filename
        #print(f"  {TxT_fNAME  =  }")
        #print(f"{filename  =  }")
        filename = TxT_fNAME
        name, ext = os.path.splitext(filename)
        new_path = os.path.join(self.output_dir, f"{name}_crop{ext}")
        cropped.save(new_path)
        print(f"Sparade: {new_path}")

    def skip_image(self):
        self.image_index += 1
        self.load_next_image()

    def handle_key(self, event):
        key = event.keysym
        if key == 's':  # smaller
            if self.crop_size > 10:
                self.crop_size -= 10
        elif key == 'b':  # bigger
            max_crop = min(self.image_width, self.image_height)
            if self.crop_size + 10 <= max_crop:
                self.crop_size += 10
        elif key == 'Up':
            if self.crop_y > 0:
                self.crop_y -= 10
        elif key == 'Down':
            if self.crop_y + self.crop_size < self.image_height:
                self.crop_y += 10
        elif key == 'Left':
            if self.crop_x > 0:
                self.crop_x -= 10
        elif key == 'Right':
            if self.crop_x + self.crop_size < self.image_width:
                self.crop_x += 10
        elif key == 'F2':
            self.save_crop()
        elif key == 'F3':
            self.skip_image()
        elif key == 'Return':
            self.save_crop()
            self.image_index += 1
            self.load_next_image()
        elif key == 'Escape':
            self.master.quit()

        self.draw_crop_rectangle()
        self.update_labels()

if __name__ == "__main__":
    root = tk.Tk()
    app = CropApp(root)
    root.mainloop()
