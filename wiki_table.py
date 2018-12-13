import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://enterthegungeon.gamepedia.com/Guns"



# Generating a usable data structure from Wikitable elements.
class TableParser():
    def __init__(self, url):
        self.req = requests.get(url)
        self.soup = BeautifulSoup(self.req.content, 'lxml')
        self.table_classes = {"class": ["sortable", "plainrowheaders"]}
        self.guntable = self.soup.find("table", self.table_classes)

    def parseHTMLtable(self):
        list_of_rows = []
        for row in self.guntable.findAll('tr'):
            list_of_cells = []
            for cell in row.findAll(['th','td']):
                text = cell.text
                list_of_cells.append(text)
            list_of_rows.append(list_of_cells)
        return list_of_rows

# instantiate a new TableParser class
tp = TableParser(url)
rows = tp.parseHTMLtable()
conventional_damages = []

count = 0
for row in rows:
    try:
        damage_val = float(row[7])
    except ValueError:
        print("Error.")
        count += 1
    else:
        conventional_damages.append(damage_val)

print(conventional_damages)
print(f'There are {count} unconventional or multi-damage weapons')


#TODO: Handle unconventional damage (OOF 101..)
#TODO: Analyze conventional damage










