import sys
import os
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QFrame
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from photo_collage import create_collage


class PhotoCollageApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Collage Creator")

        # Main widget
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Folder selection
        folder_layout = QHBoxLayout()
        self.layout.addLayout(folder_layout)
        self.folder_label = QLabel("Select Image Folder:")
        folder_layout.addWidget(self.folder_label)
        self.folder_path = QLineEdit('./src/images')
        folder_layout.addWidget(self.folder_path)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_button)

        # Output path
        output_layout = QHBoxLayout()
        self.layout.addLayout(output_layout)
        self.output_label = QLabel("Output Path:")
        output_layout.addWidget(self.output_label)
        self.output_path = QLineEdit('./collage.jpg')
        output_layout.addWidget(self.output_path)
        self.output_browse_button = QPushButton("Browse")
        self.output_browse_button.clicked.connect(self.browse_output_path)
        output_layout.addWidget(self.output_browse_button)

        # Resolution
        resolution_layout = QHBoxLayout()
        self.layout.addLayout(resolution_layout)
        self.size_label = QLabel("Resolution of each small picture:")
        resolution_layout.addWidget(self.size_label)
        self.size_entry = QLineEdit('400')
        self.size_entry.textChanged.connect(self.update_final_size_label)
        resolution_layout.addWidget(self.size_entry)

        # Dimension label
        self.dimension_label = QLabel("No valid directory selected yet.")
        self.layout.addWidget(self.dimension_label)

        # Final collage size label
        self.final_size_label = QLabel("Final collage size: Unknown")
        self.layout.addWidget(self.final_size_label)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.layout.addLayout(buttons_layout)
        self.create_button = QPushButton("Generate Preview")
        self.create_button.clicked.connect(self.preview_collage)
        buttons_layout.addWidget(self.create_button)
        self.save_button = QPushButton("Save Collage")
        self.save_button.clicked.connect(self.save_collage)
        buttons_layout.addWidget(self.save_button)

        # Preview frame
        self.preview_label = QLabel()
        self.layout.addWidget(self.preview_label)
        self.preview_label.setVisible(False)

        self.generated_collage = None

        # Check default folder path on startup
        default_folder = self.folder_path.text()
        if os.path.isdir(default_folder):
            self.update_dimension_label(default_folder)

    def browse_folder(self):
        folder_selected = QFileDialog.getExistingDirectory(
            self, "Select Folder")
        if folder_selected:
            self.folder_path.setText(folder_selected)
            self.update_dimension_label(folder_selected)

    def browse_output_path(self):
        file_selected, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "JPEG files (*.jpg);;All files (*)")
        if file_selected:
            self.output_path.setText(file_selected)

    def update_dimension_label(self, folder_path):
        valid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
        images = [f for f in os.listdir(
            folder_path) if f.lower().endswith(valid_extensions)]
        num_images = len(images)

        if num_images == 0:
            self.dimension_label.setText(
                "No images found in this folder. Please select a different folder.")
            self.dimension = None
            self.final_size_label.setText("Final collage size: Unknown")
            return

        dim = int(math.isqrt(num_images))
        if dim * dim == num_images:
            self.dimension = dim
            self.dimension_label.setText(
                f"{dim} x {dim} collage ({num_images} images)")
            self.update_final_size_label()
        else:
            self.dimension = None
            self.dimension_label.setText(f"Cannot use this folder. {
                                         num_images} images found, which is not a perfect square.")
            self.final_size_label.setText("Final collage size: Unknown")

    def update_final_size_label(self):
        if self.dimension is not None:
            try:
                size_value = int(self.size_entry.text())
                final_size = size_value * self.dimension
                self.final_size_label.setText(
                    f"Final collage size: {final_size} x {final_size}")
            except ValueError:
                self.final_size_label.setText("Invalid resolution entry.")

    def preview_collage(self):
        folder_path = self.folder_path.text()
        if not os.path.exists(folder_path):
            QMessageBox.critical(
                self, "Error", "The selected folder does not exist.")
            return
        if self.dimension is None:
            QMessageBox.critical(
                self, "Error", "Please select a valid folder with a perfect square number of images.")
            return

        try:
            size_value = int(self.size_entry.text())
            collage = create_collage(folder_path, size_value, self.dimension)
            self.generated_collage = collage

            # Show smaller preview
            collage_preview = collage.copy()
            collage_preview.thumbnail((400, 400))
            preview_image = QPixmap.fromImage(collage_preview.toqimage())
            self.preview_label.setPixmap(preview_image)

            # Show preview frame
            self.preview_label.setVisible(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def save_collage(self):
        if self.generated_collage is None:
            QMessageBox.critical(
                self, "Error", "No collage to save. Generate a preview first.")
            return
        try:
            self.generated_collage.save(self.output_path.text())
            QMessageBox.information(self, "Success", f"Collage saved to {
                                    self.output_path.text()}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoCollageApp()
    window.show()
    sys.exit(app.exec())
