from PyPDF2 import PdfFileReader
import re
import os, sys
import time
#todo
#  List reports that exist in one folder but not the other
#  Improve reporting to make it more readable - mostly finished
#  Improve variable names for easier reading - mostly finished
#  Display differences on failures - probably not worth, will maybe implement later

def get_files_in_directories(Snapshots, Regression):
    SnapShotFiles = os.listdir(Snapshots)
    RegressionFiles = os.listdir(Regression)
    return SnapShotFiles,RegressionFiles

def get_pages(path):
    # returns total pdf page number
    try:
        pdf = PdfFileReader(path)
        pages = pdf.getNumPages()
    except Exception as ex:
        print(ex)
    else:
        return pages

def get_text(path, page):
   # return text from pdf page
    pdf = PdfFileReader(path)
    text = pdf.getPage(page).extractText()
    return text

def remove_date(pdf_text):
    #replaces date with xx/xx/xxxx
    regex = r"(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2}) (?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d) AM|PM"
    substr = "xx/xx/xxxx HH:MM:SS AM/PM"
    pdf_text_date_removed = re.sub(regex,substr,pdf_text)
    return(pdf_text_date_removed)

def report_failures(snapshot_name, regress_name,page,): 
    f = open("%s-%s.txt"%(re.sub(".pdf","",os.path.split(snapshot_name)[1]),time.strftime("%m%d%y")), "at")
    f.write("FAIL\nPage %d is different\n%s\n%s\n\n"% (page, snapshot_name,regress_name))
    f.close

def report_successes(snapshot_name,snapshot_page_num, regress_name, regress_page_num,page):
    f = open("%s-%s.txt"%(re.sub(".pdf","",os.path.split(snapshot_name)[1]),time.strftime("%m%d%y")), "at")
    f.write("PASS: Page %d is the same\n%s Total Pages:%d\n%s Total Pages:%d\n\n"% (page,snapshot_name,snapshot_page_num,regress_name,regress_page_num))
    f.close

def compare_pdf(pdf1, pdf2):
    #Gets page number
    pdf1_total_pages = get_pages(pdf1)
    pdf2_total_pages = get_pages(pdf2)
    if pdf1_total_pages is None:
        pdf1_total_pages = 0
    if pdf2_total_pages is None:
        pdf2_total_pages = 0
        
    if pdf1_total_pages != pdf2_total_pages:
        #print("The PDFs have an unequal amount of pages.\nPDF1 Page Count = %d. PDF2 Page Count = %d."% (pdf1_total_pages, pdf2_total_pages))
        report_failures(SnapFile+ " %s Total Page Count %d"%(SnapFile,pdf1_total_pages),RegFile + " %s Total Page Count: %d"%(RegFile,pdf2_total_pages),pdf1_total_pages)
    else:
         #Gets page text
        for page in range(pdf1_total_pages):
            pdf1Text = remove_date(get_text(pdf1,page))
            pdf2Text = remove_date(get_text(pdf2,page))

            if pdf1Text == pdf2Text:
                print("%s page %d and %s page %d are the same"% (SnapFile,page,RegFile,page))
                report_successes(SnapFile, pdf1_total_pages,RegFile,pdf2_total_pages,page)
            else:
                print("%s page %d and %s page %d are different"% (SnapFile,page,RegFile,page))
                print("\n")
                #print('PDF1 Page %d Text:\n%s \nPDF2 Page %d Text:\n%s \n'% (page, pdf1Text, page, pdf2Text))
                report_failures(SnapFile, RegFile, page)

if __name__ == '__main__':
    # path1 = 'PDFFiles\\AP Payment RegisterF.pdf'
    # path2 = 'PDFFiles\\AP Payment RegisterB.pdf'
    # path3 = 'PDFFiles\\StatementTitle1A.pdf'
    # path4 = 'PDFFiles\\exposure.pdf'
    #compare_pdf(path1, path2)
    Snapshots = 'PDFFiles\\SnapShots'
    Regression ='PDFFiles\\Regression'
    pdfs_to_compare = get_files_in_directories(Snapshots, Regression)

    for SnapFile in pdfs_to_compare[0]:
        for RegFile in pdfs_to_compare[1]:
            if SnapFile == RegFile:
                SnapFile = Snapshots+"\\"+SnapFile
                RegFile = Regression+"\\"+RegFile
                compare_pdf(SnapFile,RegFile)
            elif RegFile not in pdfs_to_compare[0]:
                f = open("Reports_Only_In_Regression_Folder-%s.txt"%time.strftime("%m%d%y"),"at")
                f.write("%s\n\n"%RegFile)
                f.close
            elif SnapFile not in pdfs_to_compare[1]:
                f = open("Reports_Only_In_SnapShot_Folder-%s.txt"%time.strftime("%m%d%y"),"at")
                f.write("%s\n\n"%SnapFile)
                f.close
