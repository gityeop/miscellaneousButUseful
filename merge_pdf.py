import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
from PyPDF2 import PdfMerger

def create_pdf_from_images(directory):
    # Get list of image files and PDF files
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

    # Sort files by natural order
    image_files = natsorted(image_files)
    pdf_files = natsorted(pdf_files)

    # List to hold images
    image_list = []

    # Open images and append to list
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        img = Image.open(image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        image_list.append(img)

    # Create an intermediate PDF from images
    if image_list:
        temp_pdf_path = os.path.join(directory, 'temp_images.pdf')
        image_list[0].save(temp_pdf_path, save_all=True, append_images=image_list[1:])
        pdf_files.insert(0, 'temp_images.pdf')

    # Merge all PDFs into one
    merger = PdfMerger()
    for pdf_file in pdf_files:
        merger.append(os.path.join(directory, pdf_file))

    # Output PDF path (using the directory name as the filename)
    directory_name = os.path.basename(directory)
    output_path = os.path.join(directory, f'{directory_name}.pdf')
    merger.write(output_path)
    merger.close()

    # Remove the intermediate PDF
    if 'temp_images.pdf' in pdf_files:
        os.remove(temp_pdf_path)

    return output_path

if __name__ == "__main__":
    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a dialog to select directory
    directory = filedialog.askdirectory(title="이미지 파일과 PDF 파일이 있는 디렉토리를 선택하세요")

    if directory:
        pdf_path = create_pdf_from_images(directory)
        print(f"PDF가 성공적으로 생성되었습니다: {pdf_path}")
    else:
        print("디렉토리가 선택되지 않았습니다")
