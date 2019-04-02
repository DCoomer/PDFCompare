from PyPDF2 import PdfFileReader
import re
import os, sys
#todo
#  List reports that exist in one folder but not the other
#  Improve reporting to make it more readable

def get_pages(path):
    # returns total pdf page number
    pdf = PdfFileReader(path)
    pages = pdf.getNumPages()
    return pages


def get_text(path, page):
   # return text from pdf page
    pdf = PdfFileReader(path)
    text = pdf.getPage(page).extractText()
    return text

def remove_date(pdf_text):
    #removes date from pdf
    regex = r"(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2}) (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d) AM|PM"
    substr = "xx/xx/xxxx HH:MM:SS AM/PM"
    pdf_text_date_removed = re.sub(regex,substr,pdf_text)
    return(pdf_text_date_removed)


def report_failures(file_name1,file1_text, file2_name, file2_text, page):
    f = open("Failed_Files.Txt", "a")
    f.write("%s page %d and %s page %d are different\n_______________________________\n%s Page %d Text:\n%s\n_______________________________\n%s Page %d Text:\n%s \n"% (file_name1, page, file2_name,page,file_name1,page,file1_text,file2_name,page,file2_text))
    f.close

def compare_pdf(pdf1, pdf2):
    #prints page number
    pdf1_total_pages = get_pages(pdf1)
    pdf2_total_pages = get_pages(pdf2)

    if pdf1_total_pages != pdf2_total_pages:
        print("The PDFs have an unequal amount of pages.\nPDF1 Page Count = %d. PDF2 Page Count = %d."% (pdf1_total_pages, pdf2_total_pages))

        report_failures(SnapFile,"%s Total Page Count %d"%(SnapFile,pdf1_total_pages),RegFile,"%s Total Page Count: %d"%(RegFile,pdf2_total_pages),pdf1_total_pages)
    else:
         #prints page text
        for page in range(pdf1_total_pages):
            pdf1Text = remove_date(get_text(pdf1,page))
            pdf2Text = remove_date(get_text(pdf2,page))

            if pdf1Text == pdf2Text:
                print("%s page %d and %s page %d are the same"% (SnapFile,page,RegFile,page))
                #write to a successFile
            else:
                print("%s page %d and %s page %d are different"% (SnapFile,page,RegFile,page))
                print("\n")
                print('PDF1 Page %d Text:\n%s \nPDF2 Page %d Text:\n%s \n'% (page, pdf1Text, page, pdf2Text))
                report_failures(SnapFile, pdf1Text, RegFile, pdf2Text, page)
   


if __name__ == '__main__':
    Snapshots = 'PDFFiles\\SnapShots'
    Regression ='PDFFiles\\Regression'
    SnapShotFiles = os.listdir(Snapshots)
    RegressionFiles = os.listdir(Regression)
    for SnapFile in SnapShotFiles:
        for RegFile in RegressionFiles:
            if SnapFile == RegFile:
                SnapFile = Snapshots+"\\"+SnapFile
                RegFile = Regression+"\\"+RegFile
                compare_pdf(SnapFile,RegFile)
