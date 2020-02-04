from PyPDF2 import PdfFileWriter,PdfFileReader,PdfFileMerger
import glob
import os

PATH = r"L:\01 Site Tools\02 Operational Tools\62 DSV\**" + os.sep
OUTPUT_PATH = r"L:\01 Site Tools\02 Operational Tools\62 DSV" + os.sep

FILE_EXTENSION = "*.pdf"

def get_files():
    files = glob.glob(PATH + FILE_EXTENSION,recursive=True)
    #print(files)
    get_dimensions(files)

def get_dimensions(files):
    count = 0
    for file in files:
        print("FILENAME IS", file)
        pdf_file = PdfFileReader(open(file,"rb"))
        page = pdf_file.getPage(0)
        print("lower left",page.cropBox.getLowerLeft())
        print("lower right",page.cropBox.getLowerRight())
        print("upper left",page.cropBox.getUpperLeft())
        print("upper right",page.cropBox.getUpperRight())
        print("Mid point",page.cropBox.getUpperRight())
        print(pdf_file.getDocumentInfo())


        crop(pdf_file, count)
        count += 1

def crop(pdf, count):
    output = PdfFileWriter()
    pagecount = pdf.getNumPages()
    print(f"The document has {pagecount} pages ")    

    for i in range(pagecount):
        page = pdf.getPage(i)
        upper_right = page.mediaBox.getUpperRight_x(),page.mediaBox.getUpperRight_y()
        #upper_left = page.mediaBox.getUpperLeft_x(), page.mediaBox.getUpperLeft_y()
        mid_point_left = 0, page.mediaBox.getUpperLeft_y()/2
        #mid_point_right = page.mediaBox.getLowerRight_x(), page.mediaBox.getUpperRight_y()/2
        
        page.cropBox.lowerLeft = mid_point_left
        page.cropBox.upperRight = upper_right

        #print("Media box upper right ",upper_right)
        #print("Media box upper left ",upper_left)
        #print(mid_point_left)
        #print(mid_point_right)
        page.rotateCounterClockwise(90)
        output.addPage(page)

    with open(OUTPUT_PATH + str(count) + "_resized.pdf","wb") as out_file:
        output.write(out_file)


if __name__ == "__main__":
    get_files()