import os
import img2pdf
from PIL import Image
from pdf2image import convert_from_path
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def convert_pdf_to_images(pdf_file, poppler_path):
    # Directory where the Python file is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create an output folder in the same directory as the Python file
    output_folder = os.path.join(script_dir, 'img')
    os.makedirs(output_folder, exist_ok=True)

    images = convert_from_path(pdf_file, poppler_path=poppler_path)
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f'{i + 1}.jpg')
        image.save(image_path, 'JPEG')
        print(f"Saved {image_path}")
    return output_folder

def rename_images(n, series, folder_path):
    temp_names = []
    for i in range(n):
        old_name = os.path.join(folder_path, f"{series[i]}.jpg")
        temp_name = os.path.join(folder_path, f"temp_{i + 1}.jpg")
        os.rename(old_name, temp_name)
        temp_names.append(temp_name)
        print(f"Renamed {old_name} to {temp_name}")

    for i in range(n):
        new_name = os.path.join(folder_path, f"{i + 1}.jpg")
        os.rename(temp_names[i], new_name)
        print(f"Renamed {temp_names[i]} to {new_name}")

def create_series(n):
    series = []
    smallest = 1
    largest = n
    counter = 1

    while smallest <= largest:
        if (counter % 4 == 1) or (counter % 4 == 0):
            series.append(largest)
            largest -= 1
        else:
            series.append(smallest)
            smallest += 1
        counter += 1

    return series

def convert_images_to_pdf(image_folder, pdf_file):
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group()) if match else 0

    image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(".jpg") or f.endswith(".png")]
    image_files.sort(key=lambda x: extract_number(os.path.basename(x)))

    with open(pdf_file, "wb") as f:
        f.write(img2pdf.convert(image_files))

    print(f"PDF created: {pdf_file}")

# Main Execution
def main():
    # Initialize Tkinter and hide the main window
    root = Tk()
    root.withdraw()

    # Use file dialog to select a PDF file
    pdf_file = askopenfilename(filetypes=[("PDF files", "*.pdf")], title="Choose a PDF file")

    if not pdf_file:
        print("No file selected. Exiting.")
        return

    poppler_path = 'poppler/library/bin'
    
    # Directory where the Python file is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths for images and output PDF
    image_folder = os.path.join(script_dir, 'img')
    output_pdf_file = os.path.join(script_dir, 'output.pdf')

    # Convert PDF to images
    output_folder = convert_pdf_to_images(pdf_file, poppler_path)
    if output_folder:
        # Determine the number of images
        n = len([f for f in os.listdir(output_folder) if f.endswith('.jpg')])

        # Generate the series and rename the images
        series = create_series(n)
        rename_images(n, series, output_folder)

        # Convert images to PDF
        convert_images_to_pdf(output_folder, output_pdf_file)

if __name__ == "__main__":
    main()
