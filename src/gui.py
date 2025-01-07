from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
import os
from photo_collage import create_collage


class PhotoCollageApp:
    def __init__(self, master):
        self.master = master
        master.title("Photo Collage Creator")

        self.label = Label(master, text="Select Image Folder:")
        self.label.pack()

        self.folder_path = Entry(master, width=50)
        self.folder_path.pack()

        self.browse_button = Button(
            master, text="Browse", command=self.browse_folder)
        self.browse_button.pack()

        self.output_label = Label(master, text="Output Path:")
        self.output_label.pack()

        self.output_path = Entry(master, width=50)
        self.output_path.pack()
        self.output_path.insert(0, './output/collage.jpg')

        self.create_button = Button(
            master, text="Create Collage", command=self.create_collage)
        self.create_button.pack()

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.delete(0, 'end')
            self.folder_path.insert(0, folder_selected)

    def create_collage(self):
        image_folder = self.folder_path.get()
        output_path = self.output_path.get()

        if not os.path.exists(image_folder):
            messagebox.showerror(
                "Error", "The selected folder does not exist.")
            return

        try:
            create_collage(image_folder, output_path, (2800, 2800), 7)
            messagebox.showinfo("Success", "Collage created successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = Tk()
    app = PhotoCollageApp(root)
    root.mainloop()
