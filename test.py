from lxml import etree
from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd

soup = BeautifulSoup(requests.get("https://rajeduboard.rajasthan.gov.in/RESULT2023/SEV/Roll_Output.asp?roll_no=1931560").text,'html.parser')

subjects_list = soup.find_all('table')[2].find_all('tr')[2:]
subjects = [subject for subject in subjects_list]

school_name = soup.find_all('table')[1].find_all('td')[3].text

mother_name = soup.find_all('table')[0].find_all('tr')[5].find_all('td')[1].text[3:]
father_name = soup.find_all('table')[0].find_all('tr')[6].find_all('td')[1].text[3:]


print(mother_name)
