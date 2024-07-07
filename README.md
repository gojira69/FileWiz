# File Operations Application

This is a graphical user interface (GUI) application built using `PyQt5` in Python. It allows users to perform various file operations conveniently through a user-friendly interface.

## Features

- **Compress Files:** Select multiple files and compress them into a ZIP archive.
- **Encrypt PDF:** Encrypt PDF files with a password for security.
- **Convert Images to PDF:** Convert multiple image files (PNG, JPEG, BMP) into a single PDF file.
- **Merge Multiple PDFs:** Combine multiple PDF files into a single PDF document.
- **Convert Text File to PDF:** Convert a text file (TXT) into a PDF document.

## Requirements

- Python 3.x
- PyQt5
- fpdf
- Pillow (PIL)
- PyPDF2

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-repo/file-operations-app.git
   cd file-operations-app
   ```

2. **Create a virtual environment (optional but recommended):**

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install PyQt5 fpdf pillow PyPDF2
   ```

## Usage

1. **Run the application:**

   ```sh
   python app.py
   ```

2. **Interface Overview:**

   - The main window displays radio buttons to select different operations.
   - Clicking the `"Open File"` button will open a file dialog specific to the selected operation.

3. **Performing File Operations:**

   - **Compress Files:** Select files to `compress` and specify the output `ZIP file`.
   - **Encrypt PDF:** Choose a PDF file to `encrypt` and set a `password` for encryption.
   - **Convert Images to PDF:** Select `images` to convert into a `single PDF file`.
   - **Merge Multiple PDFs:** Choose `multiple PDF files` to merge into a `single PDF`.
   - **Convert Text File to PDF:** Select a `text file` to convert it into a `PDF document`.
