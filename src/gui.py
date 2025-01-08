from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
import os
import math
from PIL import Image, ImageTk
from photo_collage import create_collage


class PhotoCollageApp:
    def __init__(self, master):
        self.master = master
        master.title("Photo Collage Creator")

        # Folder selection
        self.label = Label(master, text="Select Image Folder:")
        self.label.pack()
        self.folder_path = Entry(master, width=50)
        self.folder_path.pack()
        self.folder_path.insert(0, './src/images')
        self.browse_button = Button(
            master, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        # Resolution
        self.size_label = Label(
            master, text="Resolution of each small picture:")
        self.size_label.pack()
        self.size_entry = Entry(master, width=10)
        self.size_entry.pack()
        self.size_entry.insert(0, '400')

        # Dimension label
        self.dimension_label = Label(
            master, text="No valid directory selected yet.")
        self.dimension_label.pack()
        self.dimension = None

        # Final collage size label
        self.final_size_label = Label(
            master, text="Final collage size: Unknown")
        self.final_size_label.pack()

        # Output path
        self.output_label = Label(master, text="Output Path:")
        self.output_label.pack()
        self.output_path = Entry(master, width=50)
        self.output_path.pack()
        self.output_path.insert(0, './collage.jpg')

        # Buttons and preview
        self.create_button = Button(
            master, text="Generate Preview", command=self.preview_collage)
        self.create_button.pack()
        self.preview_label = Label(master)
        self.preview_label.pack()
        self.save_button = Button(
            master, text="Save Collage", command=self.save_collage)
        self.save_button.pack()

        self.generated_collage = None

        # Check default folder path on startup
        default_folder = self.folder_path.get()
        if os.path.isdir(default_folder):
            self.update_dimension_label(default_folder)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.delete(0, 'end')
            self.folder_path.insert(0, folder_selected)
            self.update_dimension_label(folder_selected)

    def update_dimension_label(self, folder_path):
        valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
        images = [f for f in os.listdir(
            folder_path) if f.lower().endswith(valid_extensions)]
        num_images = len(images)

        if num_images == 0:
            self.dimension_label.config(
                text="No images found in this folder. Please select a different folder."
            )
            self.dimension = None
            self.final_size_label.config(text="Final collage size: Unknown")
            return

        dim = int(math.isqrt(num_images))
        if dim * dim == num_images:
            self.dimension = dim
            self.dimension_label.config(
                text=f"It will be a {dim}x{dim} collage.")
            try:
                size_value = int(self.size_entry.get())
                final_size = size_value * dim
                self.final_size_label.config(
                    text=f"Final collage size: {final_size} x {final_size}")
            except ValueError:
                self.final_size_label.config(text="Invalid resolution entry.")
        else:
            self.dimension = None
            self.dimension_label.config(
                text=f"Cannot use this folder. {num_images} images found, which is not a perfect square."
            )
            self.final_size_label.config(text="Final collage size: Unknown")

    def preview_collage(self):
        folder_path = self.folder_path.get()
        if not os.path.exists(folder_path):
            messagebox.showerror(
                "Error", "The selected folder does not exist.")
            return
        if self.dimension is None:
            messagebox.showerror(
                "Error", "Please select a valid folder with a perfect square number of images.")
            return

        try:
            size_value = int(self.size_entry.get())
            collage = create_collage(folder_path, size_value, self.dimension)
            self.generated_collage = collage

            # Show smaller preview
            collage_preview = collage.copy()
            collage_preview.thumbnail((400, 400))
            preview_image = ImageTk.PhotoImage(collage_preview)
            self.preview_label.config(image=preview_image)
            # Keep a reference to avoid garbage collection
            self.preview_label.image = preview_image

            messagebox.showinfo("Preview", "Collage preview generated!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_collage(self):
        if self.generated_collage is None:
            messagebox.showerror(
                "Error", "No collage to save. Generate a preview first.")
            return
        try:
            self.generated_collage.save(self.output_path.get())
            messagebox.showinfo(
                "Success", f"Collage saved to {self.output_path.get()}!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = Tk()
    app = PhotoCollageApp(root)
    root.mainloop()
