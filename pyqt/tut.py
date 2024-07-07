import sys
import zipfile
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QWidget,
    QRadioButton,
    QButtonGroup,
    QLabel,
    QInputDialog,
    QLineEdit,
)
from PyQt5.QtGui import QIcon
from fpdf import FPDF
from PIL import Image
import PyPDF2
import getpass


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(50, 50, 400, 300)
        self.setWindowTitle("File Operations Selector")
        self.setWindowIcon(QIcon("pic.png"))

        # Create central widget and layout
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Create a label to display the selected operation
        self.selected_operation_label = QLabel("Selected Operation: None", self)
        main_layout.addWidget(self.selected_operation_label)

        # Create a vertical layout for radio buttons
        radio_layout = QVBoxLayout()

        # Create radio buttons for file operations
        self.radio_compress = QRadioButton("Compress Files", self)
        self.radio_encrypt_pdf = QRadioButton("Encrypt PDF", self)
        self.radio_img_to_pdf = QRadioButton("Convert Image to PDF", self)
        self.radio_merge_pdfs = QRadioButton("Merge Multiple PDFs", self)
        self.radio_text_to_pdf = QRadioButton("Convert Text to PDF", self)

        # Add radio buttons to layout
        radio_layout.addWidget(self.radio_compress)
        radio_layout.addWidget(self.radio_encrypt_pdf)
        radio_layout.addWidget(self.radio_img_to_pdf)
        radio_layout.addWidget(self.radio_merge_pdfs)
        radio_layout.addWidget(self.radio_text_to_pdf)

        # Create a button group for the radio buttons
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.radio_compress)
        self.button_group.addButton(self.radio_encrypt_pdf)
        self.button_group.addButton(self.radio_img_to_pdf)
        self.button_group.addButton(self.radio_merge_pdfs)
        self.button_group.addButton(self.radio_text_to_pdf)

        # Connect the button group's signal to the handler method
        self.button_group.buttonClicked.connect(self.on_radio_button_clicked)

        # Add radio button layout to main layout
        main_layout.addLayout(radio_layout)

        # Create button for file selection
        self.button = QPushButton("Open File", self)
        self.button.clicked.connect(self.file_open)

        # Add button to layout
        main_layout.addWidget(self.button)

        # Set central widget
        self.setCentralWidget(central_widget)

        self.show()

    def on_radio_button_clicked(self, button):
        selected_operation = button.text()
        print(f"Selected operation: {selected_operation}")
        self.selected_operation_label.setText(
            f"Selected Operation: {selected_operation}"
        )

    def file_open(self):
        selected_operation = self.button_group.checkedButton().text()

        if selected_operation == "Compress Files":
            files, _ = QFileDialog.getOpenFileNames(
                self, "Select Files to Compress", "", "All Files (*)"
            )
            if files:
                output_file, _ = QFileDialog.getSaveFileName(
                    self, "Save Compressed File As", "", "ZIP Files (*.zip)"
                )
                if output_file:
                    self.compress_files(files, output_file)

        elif selected_operation == "Encrypt PDF":
            file, _ = QFileDialog.getOpenFileName(
                self, "Select PDF to Encrypt", "", "PDF Files (*.pdf)"
            )
            if file:
                password, ok = QInputDialog.getText(
                    self,
                    "Password",
                    "Enter Password for PDF Encryption:",
                    QLineEdit.Password,
                )
                if ok:
                    self.encrypt_pdf(file, password)

        elif selected_operation == "Convert Image to PDF":
            files, _ = QFileDialog.getOpenFileNames(
                self, "Select Images to Convert", "", "Image Files (*.png *.jpg *.bmp)"
            )
            if files:
                output_file, _ = QFileDialog.getSaveFileName(
                    self, "Save PDF As", "", "PDF Files (*.pdf)"
                )
                if output_file:
                    self.img_to_pdf(files, output_file)

        elif selected_operation == "Merge Multiple PDFs":
            files, _ = QFileDialog.getOpenFileNames(
                self, "Select PDFs to Merge", "", "PDF Files (*.pdf)"
            )
            if files:
                output_file, _ = QFileDialog.getSaveFileName(
                    self, "Save Merged PDF As", "", "PDF Files (*.pdf)"
                )
                if output_file:
                    self.merge_pdfs(files, output_file)

        elif selected_operation == "Convert Text to PDF":
            file, _ = QFileDialog.getOpenFileName(
                self, "Select Text File to Convert", "", "Text Files (*.txt)"
            )
            if file:
                self.text_to_pdf_converter(file)

    def compress_files(self, filePaths, outputFileName):
        if not filePaths:
            print("Please provide a list of files to compress.")
            return

        if not outputFileName:
            print("Please provide an output file name for the compressed files.")
            return

        outputFileName += ".zip"
        with zipfile.ZipFile(outputFileName, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in filePaths:
                zipf.write(file, arcname=file.split("/")[-1])

        print(f"Files compressed successfully to {outputFileName}")

    def text_to_pdf_converter(self, fileName):
        if not fileName:
            print("Please provide a file name.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial")

        def read_text_file(filename):
            encodings = ["utf-8", "latin-1", "ascii"]
            for encoding in encodings:
                try:
                    with open(filename, "r", encoding=encoding) as file:
                        return file.readlines()
                except UnicodeDecodeError:
                    continue
            with open(filename, "r", encoding="utf-8", errors="ignore") as file:
                return file.readlines()

        lines = read_text_file(fileName)

        for line in lines:
            pdf.cell(200, 10, txt=line.strip(), ln=True)

        fileName = fileName.split(".")[0] + ".pdf"
        pdf.output(fileName)
        print(f"PDF file '{fileName}' created successfully.")

    def merge_pdfs(self, pdfFiles, outputFileName):
        if not pdfFiles:
            print("Please provide a list of PDF files.")
            return

        if not outputFileName:
            print("Please provide an output file name.")
            return

        merger = PyPDF2.PdfMerger()
        for pdf in pdfFiles:
            merger.append(pdf)

        outputFileName = outputFileName + ".pdf"
        merger.write(outputFileName)
        merger.close()
        print(f"PDF files merged successfully to {outputFileName}")

    def img_to_pdf(self, imgFiles, outputFileName):
        if not imgFiles:
            print("Please provide a list of image files.")
            return

        if not outputFileName:
            print("Please provide an output file name.")
            return

        outputFileName = outputFileName + ".pdf"
        imgs = [Image.open(img).convert("RGB") for img in imgFiles]
        imgs[0].save(outputFileName, save_all=True, append_images=imgs[1:])

        print(f"Images converted to PDF: {outputFileName}")

    def encrypt_pdf(self, fileName, pwd):
        if not fileName:
            print("Please provide a PDF file name.")
            return

        with open(fileName, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            writer = PyPDF2.PdfWriter()

            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

            writer.encrypt(pwd)
            output_file = fileName.split(".")[0] + "_encrypted.pdf"

            with open(output_file, "wb") as output_file:
                writer.write(output_file)

            print(
                f"PDF file '{fileName}' encrypted successfully and saved as {output_file}."
            )


if __name__ == "__main__":

    def run():
        app = QApplication(sys.argv)
        gui = Window()
        sys.exit(app.exec_())

    run()
