import pprint
from bs4 import BeautifulSoup

DASH = "\u2013"

def d100_to_int(n):
    return 100 if n == "00" else int(n)

with open('data/source.html') as f: html = f.read()
soup = BeautifulSoup(html, 'html.parser')

table1 = soup.find_all('table')[1]
table2 = soup.find_all('table')[2]

rows = [[cell.text for cell in row.find_all('td')] for row in table1.find_all('tr')][2:]
rows += [[cell.text for cell in row.find_all('td')] for row in table2.find_all('tr')][2:]

beach_column = [(row[0], row[1]) for row in rows if any(c.isdigit() for c in row[1])]

beach = []
for row in beach_column:
    bounds = None
    if DASH in row[1]:
        bounds = [d100_to_int(c) for c in row[1].split(DASH)]
    else:
        bounds = [d100_to_int(row[1])] * 2

    beach += ([row[0]] * (bounds[1] - bounds[0] + 1))



pp = pprint.PrettyPrinter()
pp.pprint(beach)
