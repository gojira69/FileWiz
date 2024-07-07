from PIL import Image

def img_to_pdf(imgFiles, outputFileName):
    
    if not imgFiles:
        print("Please provide a list of image files.")
        return
    
    if not outputFileName:
        print("Please provide an output file name.")
        return

    outputFileName = outputFileName + ".pdf"
    imgs = [Image.open(img).convert('RGB') for img in imgFiles]
    imgs[0].save(outputFileName, save_all=True, append_images=imgs[1:])
    
    print(f"Images converted to PDF: {outputFileName}")    

imgList = input("Enter the list of image files: ").split(" ")
outputFileName = input("Enter the output file name: ")

img_to_pdf(imgList, outputFileName)
