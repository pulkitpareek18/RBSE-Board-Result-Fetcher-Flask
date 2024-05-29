from lxml import etree
from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def remove_html_entities(text):
    # Define regular expression pattern to match HTML entities like &nbsp;
    pattern = r'&[A-Za-z]+;|^\s+'
    # Remove HTML entities
    clean_text = re.sub(pattern, '', text)
    return clean_text

formatted_marks_list = []
titles_main = []


def add_to_df(roll_no):
    global titles_main

    print(roll_no)

    soup = BeautifulSoup(requests.get(f"https://rajeduboard.rajasthan.gov.in/RESULT2024/SEV/Roll_Output.asp?roll_no={roll_no}").text,'html.parser')

    rollno = soup.find_all('table')[1].find_all('td')[2].text
    name = soup.find_all('table')[0].find_all('tr')[4].find_all('td')[1].text[3:]
    mother_name = soup.find_all('table')[0].find_all('tr')[5].find_all('td')[1].text[3:]
    father_name = soup.find_all('table')[0].find_all('tr')[6].find_all('td')[1].text[3:]
    school_name = soup.find_all('table')[1].find_all('td')[3].text
    total_marks = soup.find_all('table')[3].find_all('strong')[0].text[22:]
    percentage = soup.find_all('table')[3].find_all('strong')[1].text[13:]
    result = soup.find_all('table')[3].find_all('tr')[2].find('td').find('strong').text
    result = remove_html_entities(result)


    subjects_list = soup.find_all('table')[2].find_all('tr')[2:]
    subjects = [subject for subject in subjects_list]


    titles = ["Name","Roll No","Mother's Name","Father's Name","School"]


    # print(name,rollno)

    formatted_marks = [name,rollno,mother_name,father_name,school_name]


    for subject in subjects:
        data = subject.find_all('font')
        titles.append(remove_html_entities(data[0].text))
        formatted_marks.append(remove_html_entities(data[-1].text))
        # for i in data:
        #     print(remove_html_entities(i.text))
        # print("---------")

    # print(titles)
    
        
    if(subjects == []):
        for i in range(6):
            print(f"Append: {i}")
            formatted_marks.append(result[8:])

    formatted_marks.append(total_marks)
    formatted_marks.append(percentage)
    formatted_marks.append(result[8:])


    titles.append("Total Marks")
    titles.append("Percentage")
    titles.append("Remarks")

    
    formatted_marks_list.append(formatted_marks)
    titles_main = titles
    # print(titles)
    # print(formatted_marks_list)



     



# for i in range(1931535, 1931540):
#     print(i)
#     add_to_df(f"https://rajeduboard.rajasthan.gov.in/RESULT2023/SEV/Roll_Output.asp?roll_no={i}")

rollnos = [rollno for rollno in range(1836268 , 1836312)]

with ThreadPoolExecutor(max_workers=100) as executor:
                results = executor.map(add_to_df, rollnos)


print("Number of rows appended:", len(formatted_marks_list))  # Debugging statement

df = pd.DataFrame(columns=titles_main)
df.index.name = 'S No.'
for row in formatted_marks_list:
    df = df.append(pd.Series(row, index=df.columns), ignore_index=True)



# Remove non-numeric characters from mark columns
numeric_columns = df.columns.difference(['Name','Mother\'s Name','Father\'s Name','School','Remarks'])  # Exclude 'Name' and 'Roll No' columns
df[numeric_columns] = df[numeric_columns].replace('[^\d.]', '', regex=True)

# Convert numeric columns to numeric data types
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')


# Adjust index name and values
df = df.sort_values(by=df.columns[1])
df = df.reset_index(drop=True)
df.index = df.index + 1
df.index.name = 'S. No.'

print(df)

# Write the DataFrame to an Excel file
df.to_excel("results.xlsx")