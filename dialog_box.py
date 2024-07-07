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


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(50, 50, 400, 300)
        self.setWindowTitle("File Operations")
        self.setWindowIcon(QIcon("logo.jpeg"))

        centralWidget = QWidget(self)
        mainLayout = QVBoxLayout(centralWidget)

        self.selected_operation_label = QLabel("Selected Operation: None", self)
        mainLayout.addWidget(self.selected_operation_label)


        self.radioCompress = QRadioButton("Compress Files", self)
        self.radioEncryptPDF = QRadioButton("Encrypt PDF", self)
        self.radioIMGtoPDF = QRadioButton("Convert Images to PDF", self)
        self.radioMergePDFs = QRadioButton("Merge Multiple PDFs", self)
        self.radioTexttoPDF = QRadioButton("Convert Text File to PDF", self)

        radioLayout = QVBoxLayout()
        radioLayout.addWidget(self.radioCompress)
        radioLayout.addWidget(self.radioEncryptPDF)
        radioLayout.addWidget(self.radioIMGtoPDF)
        radioLayout.addWidget(self.radioMergePDFs)
        radioLayout.addWidget(self.radioTexttoPDF)

        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.radioCompress)
        self.buttonGroup.addButton(self.radioEncryptPDF)
        self.buttonGroup.addButton(self.radioIMGtoPDF)
        self.buttonGroup.addButton(self.radioMergePDFs)
        self.buttonGroup.addButton(self.radioTexttoPDF)

        self.buttonGroup.buttonClicked.connect(self.onRadioButtonClicked)

        mainLayout.addLayout(radioLayout)

        self.button = QPushButton("Open File", self)
        self.button.clicked.connect(self.openFile)

        mainLayout.addWidget(self.button)

        self.setCentralWidget(centralWidget)

        self.show()

    def onRadioButtonClicked(self, button):
        selectedOperation = button.text()
        print(f"Selected operation: {selectedOperation}")
        self.selected_operation_label.setText(
            f"Selected Operation: {selectedOperation}"
        )

    def openFile(self):
        selectedOperation = self.buttonGroup.checkedButton().text()

        if selectedOperation == "Compress Files":
            files, _ = QFileDialog.getOpenFileNames(
                self, "Select Files to Compress", "", "All Files (*)"
            )
            if files:
                output_file, _ = QFileDialog.getSaveFileName(
                    self, "Save Compressed File As", "", "ZIP Files (*.zip)"
                )
                if output_file:
                    self.compressFiles(files, output_file)

        elif selectedOperation == "Encrypt PDF":
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
                    self.encryptPDF(file, password)

        elif selectedOperation == "Convert Images to PDF":
            files, _ = QFileDialog.getOpenFileNames(
                self, "Select Images to Convert", "", "Image Files (*.png *.jpg *.bmp)"
            )
            if files:
                output_file, _ = QFileDialog.getSaveFileName(
                    self, "Save PDF As", "", "PDF Files (*.pdf)"
                )
                if output_file:
                    self.imgToPDF(files, output_file)

        elif selectedOperation == "Merge Multiple PDFs":
            files, _ = QFileDialog.getOpenFileNames(
                self, "Select PDFs to Merge", "", "PDF Files (*.pdf)"
            )
            if files:
                output_file, _ = QFileDialog.getSaveFileName(
                    self, "Save Merged PDF As", "", "PDF Files (*.pdf)"
                )
                if output_file:
                    self.mergePDFs(files, output_file)

        elif selectedOperation == "Convert Text File to PDF":
            file, _ = QFileDialog.getOpenFileName(
                self, "Select Text File to Convert", "", "Text Files (*.txt)"
            )
            if file:
                self.textToPDF(file)

    # The core functions for file operations

    def compressFiles(self, filePaths, outputFileName):
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

    def textToPDF(self, fileName):
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

    def mergePDFs(self, pdfFiles, outputFileName):
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

    def imgToPDF(self, imgFiles, outputFileName):
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

    def encryptPDF(self, fileName, pwd):
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
