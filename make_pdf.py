import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted

def create_pdf_from_images(directory):
    # Get list of image files
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Sort files by natural order
    image_files = natsorted(image_files)

    # List to hold images
    image_list = []

    # Open images and append to list
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        img = Image.open(image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        image_list.append(img)

    # Output PDF path (using the directory name as the filename)
    directory_name = os.path.basename(directory)
    output_path = os.path.join(directory, f'{directory_name}.pdf')

    # Save images as a single PDF
    if image_list:
        image_list[0].save(output_path, save_all=True, append_images=image_list[1:])

    return output_path

if __name__ == "__main__":
    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a dialog to select directory
    directory = filedialog.askdirectory(title="이미지 파일이 있는 디렉토리를 선택하세요")

    if directory:
        pdf_path = create_pdf_from_images(directory)
        print(f"PDF가 성공적으로 생성되었습니다: {pdf_path}")
    else:
        print("디렉토리가 선택되지 않았습니다")
