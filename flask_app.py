from flask import Flask, render_template, request, redirect, url_for
import os, shutil
import pandas as pd
import pdfkit
from pypdf import PdfMerger
from concurrent.futures import ThreadPoolExecutor
import time
import json
import threading
from wkhtmltopdf import wkhtmltopdf



app = Flask(__name__, static_url_path='/static')


def cleanGarbage():
    threading.Timer(600, cleanGarbage).start()
    for file in os.listdir('static/output'):
        if file != ".gitkeep":
            os.remove(os.path.join('static/output',file))
    print(f'Garbage Cleaned at {time.strftime("%m/%d/%Y, %H:%M:%S")}.')

cleanGarbage()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/api/result', methods=['GET'])
def result():

    class_std = request.args.get("class")
    subject_stream = request.args.get("stream")

    start = request.args.get("start")
    end = request.args.get("end")


    try:
        os.mkdir(".Results")
    except Exception as e:
        pass

    try:
        os.mkdir("static/output")
    except Exception as e:
        pass
        
    
    print("-----RBSE Class 10th Results Fetcher-----")
    f = open('config.json')
    json_data = json.load(f)
        
    startingRange = int(start)
    endingRange = int(end)

    rollnos = [rollno for rollno in range(startingRange,endingRange+1)]

    choice = 0

    if(class_std == "tenth"):
            baseUrl = json_data['tenth_base_url']
    elif(class_std == "twelfth"):
        if(subject_stream == "science"):
            choice=1
            baseUrl = json_data['twelfth_science_base_url']
        elif(subject_stream == "commerce"):
            choice=2
            baseUrl = json_data['twelfth_commerce_base_url']
        elif(subject_stream == "arts"):
            choice=3
            baseUrl = json_data['twelfth_arts_base_url']
    

        
    if(class_std == "tenth"):
            
            def result(rollno):

                try:
                    wkhtmltopdf(f"{baseUrl}{rollno}", os.path.join(os.getcwd(),".Results",f'{rollno}.pdf'))  
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

            merger.write(os.path.join(os.getcwd(),"static/output",f"RBSE Class 10th Result {rollnos[0]}-{rollnos[len(rollnos)-1]}.pdf"))
            result_filename = f"RBSE Class 10th Result {rollnos[0]}-{rollnos[len(rollnos)-1]}.pdf"
            merger.close()
            shutil.rmtree(os.path.join(os.getcwd(),".Results"), ignore_errors=True)

            finalTime = time.time()
            print(f"Results Fetched In: {time.strftime('%H:%M:%S', time.gmtime(finalTime-initTime))}")

            return redirect(url_for('static', filename=f"output/RBSE Class 10th Result {rollnos[0]}-{rollnos[len(rollnos)-1]}.pdf"))

    elif(class_std == "twelfth"):
            print("-----RBSE Class 12th Results Fetcher-----")
                
            streamNames = ["Science","Commerce","Arts"]
                
            def result(rollno):

                try:
                    wkhtmltopdf(f"{baseUrl}{rollno}&B1=Submit", os.path.join(os.getcwd(),".Results",f'{rollno}.pdf'))  
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

            merger.write(os.path.join(os.getcwd(),"static/output",f"RBSE Class 12th {streamNames[choice-1]} Result {rollnos[0]}-{rollnos[len(rollnos)-1]}.pdf"))
            merger.close()
            shutil.rmtree(os.path.join(os.getcwd(),".Results"), ignore_errors=True)
            return redirect(url_for('static', filename=f"output/RBSE Class 12th {streamNames[choice-1]} Result {rollnos[0]}-{rollnos[len(rollnos)-1]}.pdf"))



app.run(debug=True)