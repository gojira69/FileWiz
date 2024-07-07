import PyPDF2

def merge_pdfs(pdfFiles,outputFileName):    
    
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
    
pdfFiles = input("Enter the names of the PDF files to merge (separated by commas): ").split(" ")
outputFileName = input("Enter the name of the output file: ")

merge_pdfs(pdfFiles, outputFileName)