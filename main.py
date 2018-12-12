import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://enterthegungeon.gamepedia.com/Guns"
response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')


class HTMLTableParser:

    def parse_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        return[(table['id'],self.parse_html_table(table))\
               for table in soup.find_all('table')]

    def parse_html_table(self,table):
        n_columns = 0
        n_rows = 0
        column_names = []

        # Find number of rows and columns, and column titles
        for row in table.find_all('tr'):

            # Determine number of rows
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows += 1
                if n_columns == 0:
                    # set num of columns for table
                    n_columns = len(td_tags)

            #handle column names if found
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    print(th.get_text())
                    column_names.append(th.get_text())

            # safeguard column titles
            if len(column_names) > 0 and len(column_names) != n_columns:
                raise Exception("Column titles do not match number of columns")

            columns = column_names if len(column_names) > 0 else range(0, n_columns)
            df = pd.DataFrame(columns=columns, index=range(0,n_rows))
            row_marker = 0
            for row in table.find_all('tr'):
                column_marker = 0
                columns = row.find_all('td')
                print(columns)
                for column in columns:
                    df.iat[row_marker, column_marker] = column.get_text()
                    column_marker += 1
                if len(columns) > 0:
                    row_marker += 1

            for col in df:
                try:
                    df[col] = df[col].astype(float)
                except ValueError:
                    pass

                return df

soup = BeautifulSoup(response.text, 'lxml') # parsing HTML

table = soup.find_all('table')[0]

new_table = pd.DataFrame(columns=range(0,2), index=[0])

row_marker = 0

# for row in table.find_all('tr', limit=2):
#     print(row)
#     columns = row.find_all('td', limit=2)
#     for column in columns:
#         print(column)


