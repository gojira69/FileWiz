import PyPDF2
import getpass

def encryptPDF(fileName, pwd):
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
        
        print(f"PDF file '{fileName}' encrypted successfully and saved as {output_file}.")

def get_secure_password_input():
    while True:
        pwd = getpass.getpass(prompt="Enter the password for encryption: ")
        confirm_pwd = getpass.getpass(prompt="Confirm password: ")
        if pwd == confirm_pwd:
            return pwd
        else:
            print("Passwords do not match. Please try again.")

inputFile = input("Enter the name of the PDF file to encrypt: ")
password = get_secure_password_input()
encryptPDF(inputFile, password)
