from fpdf import FPDF

def text_to_pdf_Converter(fileName):

    if not fileName:
        print("Please provide a file name.")
        return

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font('Arial')

    def read_text_file(filename):
        encodings = ['utf-8', 'latin-1', 'ascii'] 
        for encoding in encodings:
            try:
                with open(filename, "r", encoding=encoding) as file:
                    return file.readlines()
            except UnicodeDecodeError:
                continue
        with open(filename, "r", encoding='utf-8', errors='ignore') as file:
            return file.readlines()

    lines = read_text_file(fileName)

    for line in lines:
        pdf.cell(200, 10, txt=line.strip(), ln=True)

    fileName = fileName.split('.')[0] + ".pdf"

    pdf.output(fileName)
    
    print(f"PDF file '{fileName}' created successfully.")

fileName = input("Enter the name of the text file: ")
text_to_pdf_Converter(fileName)