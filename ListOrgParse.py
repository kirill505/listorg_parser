import requests, lxml, csv
from bs4 import BeautifulSoup

#get content from the page
def get_page(url):
    headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0(X11;Linux x86_64...)Geco/20100101 Firefox/60.0'}
    session = requests.session()
    
    request = session.get(url, headers=headers)
    
    if request.ok:
        return request.text

#parse necessery fields
def parse_data(soup, keys):
    all = soup.find_all("div", class_='c2m')
    
    #parse all non table data
    non_table = [i.find_all("p") for i in all]
    non_table = [i for i in non_table]
    non_table2 = []
    for i in non_table:
        for j in i:
            non_table2.append(j.text.split(': '))

    #parse all table data
    table = [i.text.split(':') for i in all[0].table.find_all("tr")]
    
    #join all data
    data = non_table2 + table

    #save to dict with correct order
    res = dict()
    for key in keys:
        for i in data:
            if i[0] == key:
                res[i[0]] = i[1]
    return res

#save data to csv
def write_csv(dict):
    with open('list-org.csv', 'w') as file:
        w = csv.writer(file)
        for key, val in dict.items():
            w.writerow([key, val])

#main function of this module
def ListOrgParse_csv(url, *args):
    html = get_page(url)
    soup = BeautifulSoup(html, 'lxml')
    data = parse_data(soup, args)
    write_csv(data)