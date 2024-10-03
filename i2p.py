import os
import tkinter as tk
from tkinter import filedialog
import img2pdf

# Change the working directory to the directory where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def images_to_pdf():
    # Open file dialog to select image files
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    image_paths = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    # If no images were selected, exit the function
    if not image_paths:
        print("No images selected.")
        return

    # Open file dialog to specify the output PDF path
    output_pdf_path = filedialog.asksaveasfilename(
        title="Save PDF as",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )

    # If no output file was selected, exit the function
    if not output_pdf_path:
        print("No output path specified.")
        return

    # Convert images to PDF
    try:
        with open(output_pdf_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))
        print(f"Images converted successfully. PDF saved at '{output_pdf_path}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    images_to_pdf()
