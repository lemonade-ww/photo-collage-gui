from tkinter import Tk, filedialog, messagebox
from tkinter import ttk
import os
import math
from PIL import ImageTk
from photo_collage import create_collage


class PhotoCollageApp:
    def __init__(self, master):
        self.master = master
        master.title("Photo Collage Creator")

        # Main frame
        main_frame = ttk.Frame(master)
        main_frame.pack(padx=10, pady=10)

        # Folder selection
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=0, column=0, columnspan=2, pady=5)
        self.label = ttk.Label(folder_frame, text="Select Image Folder:")
        self.label.grid(row=0, column=0, padx=5)
        self.folder_path = ttk.Entry(folder_frame, width=50)
        self.folder_path.grid(row=0, column=1, padx=5)
        self.folder_path.insert(0, './src/images')
        self.browse_button = ttk.Button(
            folder_frame, text="Browse", command=self.browse_folder)
        self.browse_button.grid(row=0, column=2, padx=5)

        self.output_label = ttk.Label(folder_frame, text="Output Path:")
        self.output_label.grid(row=1, column=0, padx=5)
        self.output_path = ttk.Entry(folder_frame, width=50)
        self.output_path.grid(row=1, column=1, padx=5)
        self.output_path.insert(0, './collage.jpg')
        self.output_browse_button = ttk.Button(
            folder_frame, text="Browse", command=self.browse_output_path)
        self.output_browse_button.grid(
            row=1, column=2, padx=5)

        resolution_frame = ttk.Frame(main_frame)
        resolution_frame.grid(row=1, column=0, columnspan=2, pady=5)

        # Resolution
        self.size_label = ttk.Label(
            resolution_frame, text="Resolution of each small picture:")
        self.size_label.grid(row=0, column=0, padx=5)
        self.size_entry = ttk.Entry(resolution_frame, width=10)
        self.size_entry.grid(row=0, column=1, padx=5)
        self.size_entry.insert(0, '400')
        self.size_entry.bind("<KeyRelease>", self.update_final_size_label)

        # Dimension label
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=0, columnspan=2, pady=5)
        self.dimension_label = ttk.Label(
            info_frame, text="No valid directory selected yet.")
        self.dimension_label.grid(
            row=1, column=0, columnspan=2)
        self.dimension = None

        # Final collage size label
        self.final_size_label = ttk.Label(
            info_frame, text="Final collage size: Unknown")
        self.final_size_label.grid(
            row=2, column=0, columnspan=2)

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=5)
        self.create_button = ttk.Button(
            buttons_frame, text="Generate Preview", command=self.preview_collage)
        self.create_button.grid(row=0, column=0, padx=5)
        self.save_button = ttk.Button(
            buttons_frame, text="Save Collage", command=self.save_collage)
        self.save_button.grid(row=0, column=1, padx=5)

        # Preview frame
        self.preview_frame = ttk.Frame(main_frame)
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.grid(row=0, column=0, columnspan=2)

        self.generated_collage = None

        # Disable preview frame initially
        self.preview_frame.grid_remove()

        # Check default folder path on startup
        default_folder = self.folder_path.get()
        if os.path.isdir(default_folder):
            self.update_dimension_label(default_folder)

        # Set minimum size after window is rendered
        self.master.after(100, self.set_min_size)

    def set_min_size(self):
        self.master.update_idletasks()  # Ensure all elements are rendered
        width = self.master.winfo_reqwidth()
        height = self.master.winfo_reqheight()
        self.master.wm_minsize(width=width, height=height)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.delete(0, 'end')
            self.folder_path.insert(0, folder_selected)
            self.update_dimension_label(folder_selected)

    def browse_output_path(self):
        file_selected = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[
                                                     ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_selected:
            self.output_path.delete(0, 'end')
            self.output_path.insert(0, file_selected)

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
                text=f"{dim} x {dim} collage ({num_images} images)")
            self.update_final_size_label()
        else:
            self.dimension = None
            self.dimension_label.config(
                text=f"Cannot use this folder. {num_images} images found, which is not a perfect square."
            )
            self.final_size_label.config(
                text="Final collage size: Unknown")

    def update_final_size_label(self, event=None):
        if self.dimension is not None:
            try:
                size_value = int(self.size_entry.get())
                final_size = size_value * self.dimension
                self.final_size_label.config(
                    text=f"Final collage size: {final_size} x {final_size}")
            except ValueError:
                self.final_size_label.config(text="Invalid resolution entry.")

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

            # Show preview frame
            self.preview_frame.grid(row=4, column=0, columnspan=2, pady=5)
            self.set_min_size()

            # messagebox.showinfo("Preview", "Collage preview generated!")

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
