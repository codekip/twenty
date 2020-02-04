import glob
import os

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

PATH = r"L:\01 Site Tools\02 Operational Tools\62 DSV\**" + os.sep
OUTPUT_PATH = r"L:\01 Site Tools\02 Operational Tools\62 DSV" + os.sep
FILE_EXTENSION = "*.pdf"
IGNORE = ("resize")

def get_files():
    all_files = glob.glob(PATH + FILE_EXTENSION,recursive=True)
    files = [file for file in all_files if not IGNORE in file]
    return files

def run():
    modify_files(get_files())
    
def modify_files(files):
    count = 0
    for file in files:
        input_file = open(file,"rb")
        pdf_file = PdfFileReader(input_file)
        crop(pdf_file, count)
        input_file.close()
        count += 1

def crop(pdf, count):
    output = PdfFileWriter()
    pagecount = pdf.getNumPages()

    for i in range(pagecount):
        page = pdf.getPage(i)
        upper_right = page.mediaBox.getUpperRight_x(),page.mediaBox.getUpperRight_y()
        mid_point_left = 0, page.mediaBox.getUpperLeft_y()/2
        
        page.cropBox.lowerLeft = mid_point_left
        page.cropBox.upperRight = upper_right
        page.rotateCounterClockwise(90)
        output.addPage(page)

    with open(OUTPUT_PATH + str(count) + "_resized.pdf","wb") as out_file:
        output.write(out_file)
    
    out_file.close()

def delete_files():
    for file in get_files():
        os.remove(file)

if __name__ == "__main__":
    run()
    delete_files()