# Photo Collage GUI

This project is a Python application that allows users to create photo collages from images in a specified folder. It features a graphical user interface (GUI) for easy interaction.

## Project Structure

```
photo-collage-gui
├── src
│   ├── photo_collage.py  # Core functionality for creating photo collages
│   ├── gui.py            # GUI implementation for user interaction
│   └── assets            # Directory for additional assets
│       └── .gitkeep      # Keeps the assets directory tracked by Git
├── requirements.txt       # Lists project dependencies
└── README.md              # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd photo-collage-gui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python src/gui.py
   ```

2. Use the GUI to select an image folder, specify output options, and create your collage.

## Dependencies

- Pillow: For image processing
- Tkinter or PyQt: For the graphical user interface

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.