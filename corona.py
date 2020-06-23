# corona.py
# importing libraries 

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import os
import numpy as np
import matplotlib.pyplot as plt

extract_contents = lambda row: [x.text.replace('\n', '') for x in row]                    # Extract from database
URL = 'https://www.mohfw.gov.in/'

response = requests.get(URL).content
soup = BeautifulSoup(response, 'html.parser')
header = extract_contents(soup.tr.find_all('th'))

stats = []                                                                                # Converting data into table
all_rows = soup.find_all('tr')

for row in all_rows:
    stat = extract_contents(row.find_all('td'))
    if stat:
        if len(stat) == 5:
            # last row
            stat = ['', stat]
            stats.append(stat)
        elif len(stat) == 6:
            stats.append(stat)

stats[-1][1] = "Total Cases"                                                              # Add Total

SHORT_HEADERS = ['SNo', 'State', 'Active Cases', 'Recoveries', 'Deaths', 'Total Cases']   # Table headers
table = tabulate(stats, headers=SHORT_HEADERS)
print(table)                                                                              # Result

stats.remove(stats[-1])                                                                   # Remove total

objects = []                                                                              # States list
for row in stats:
    objects.append(row[1])

y_pos = np.arange(len(objects))

Total_cases = []                                                                          # Total cases list
for row in stats:
    Total_cases.append(int(row[5]))

plt.barh(y_pos, Total_cases, align='center', alpha=0.5)                                   # Graph

plt.yticks(y_pos, objects)
plt.xlabel('Number of Cases')
plt.ylabel('States')
plt.title('Corona Virus Cases')
plt.show()                                                                                # Output
