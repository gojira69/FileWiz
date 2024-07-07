import zipfile

def compressFiles(filePaths, outputFileName):
    if not filePaths:
        print("Please provide a list of files to compress.")
        return
    
    if not outputFileName:
        print("Please provide an output file name for the compressed files.")
        return

    outputFileName += ".zip"
    with zipfile.ZipFile(outputFileName, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in filePaths:
            zipf.write(file, arcname=file.split("/")[-1])
    
    print(f"Files compressed successfully to {outputFileName}")

filePaths = input("Enter the list of files to compress (separated by spaces): ").split(" ")
outputFileName = input("Enter the name of the output zip file: ")

compressFiles(filePaths, outputFileName)