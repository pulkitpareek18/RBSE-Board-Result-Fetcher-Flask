import os, shutil
import pandas as pd
import pdfkit
from pypdf import PdfMerger
from concurrent.futures import ThreadPoolExecutor
import time

    
try:
    os.mkdir(".Results")
except Exception as e:
    pass

try:
    os.mkdir("Output")
except Exception as e:
    pass
    
# configuring pdfkit to point to our installation of wkhtmltopdf  
config = pdfkit.configuration(wkhtmltopdf = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")  
  
print("-----RBSE Class 10th Results Fetcher-----")
choice = 0
    
startingRange = int(input("Enter starting range of Roll No.: "))
endingRange = int(input("Enter ending range of Roll No.: "))

rollnos = [rollno for rollno in range(startingRange,endingRange+1)]

    
baseUrl = "https://rajeduboard.rajasthan.gov.in/RESULT2023/SEV/Roll_Output.asp?roll_no="  #Default for ARTS



    
def result(rollno):

    try:
        pdfkit.from_url(f"{baseUrl}{rollno}", os.path.join(os.getcwd(),".Results",f'{rollno}.pdf'), configuration = config)  
        return( f'{rollno}.pdf',"Done")
    except Exception as e:
        return(e)
    
    


print("Fetching Results.....")
initTime = time.time()

with ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(result, rollnos)
    for result in results:
      print(result)

pdfs = sorted([os.path.join(os.getcwd(),".Results",pdf) for pdf in os.listdir(os.path.join(os.getcwd(),".Results"))])

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write(os.path.join(os.getcwd(),"Output",f"RBSE Class 10th Result {rollnos[0]}-{rollnos[len(rollnos)-1]}.pdf"))
merger.close()
shutil.rmtree(os.path.join(os.getcwd(),".Results"), ignore_errors=True)

finalTime = time.time()
print(f"Results Fetched In: {time.strftime('%H:%M:%S', time.gmtime(finalTime-initTime))}")