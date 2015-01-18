__author__ = 'Robert_Stallard'

from lxml import html
import requests
import tablib
import time


today_date = time.strftime('%Y%m%d')
print(today_date)
# cem_url = input("Specify URL for gravesite photo requests:")
cem_url = 'http://www.findagrave.com/cgi-bin/fg.cgi?page=rapList&rapMode=cemetery&rapCemeteryId=73275'
print(cem_url)

page = requests.get(cem_url)
tree = html.fromstring(page.text)

raw_string = tree.xpath('string()')

print(tree.xpath('//tr/td[1]/a[1]/text()'))

# xml structure ------
# /html/body/table/tbody/tr/td[3]/form/table/tbody/tr/td/table/tbody/tr[3]/td[1]/a[1]
# /html/body/table/tbody/tr/td[3]/form/table/tbody/tr/td/table/tbody/tr[4]/td[1]/a[1]

# Cemetery name: /html/body/table/tbody/tr/td[3]/form/table/tbody/tr/td/table/tbody/tr[1]/td/font/a
print(tree.xpath('//tr[18]/td/font/a/text()'))  # This works! Requires careful study of source. Not inspector.

cem_name = tree.xpath('//tr[18]/td/font/a/text()')
prnames = tree.xpath('//tr/td[1]/a[1]/text()')

# first entry should be 'name'. Removing it.
prnames.pop(0)
print("# of items scraped: " + str(len(prnames)))
alph_names = sorted(prnames, key = lambda x: x.split()[1])

print(alph_names)


# Create data set

name_set = tablib.Dataset()
lines_per_page = 40
columns = [alph_names[a:a+lines_per_page] for a in range(0, len(alph_names), lines_per_page)]

print(columns)
print('# of columns: ' + str(len(columns)))

# make reference to each column
print(range(len(columns)))
for i in range(len(columns) - 1):
    print(i)
    name_set.append_col(columns[i])
    print(columns[i])


filename = ' '.join(cem_name) + '_' + today_date
print(filename)
fcsv = open(filename+'.csv', 'w', newline='')
fcsv.write(name_set.csv)
fcsv.close()


with open(filename +'.xls', 'wb') as f:
    f.write(name_set.xls)



# TODO items of concern: cemetery name, site names, URL
# TODO consider 'one problem reported' being marked
# TODO Xpath is wonky -- any way to make that easier?