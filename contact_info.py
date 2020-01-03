from bs4 import BeautifulSoup
import requests
import os
import csv

def write_csv(lines, filename):
    """
    Write lines to csv named as filename
    """
    if not os.path.isdir('output'):
        os.mkdir("output")
    file_path = "output/%s" % filename
    with open(file_path, 'a', encoding='utf-8', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=',')
        writer.writerows(lines)

URL = "https://www.londoff.com/MeetOurDepartments"

def get_contact_list(URL):
    res = requests.get(url=URL).text
    soup = BeautifulSoup(res, 'html.parser')
    main = soup.find('main')
    div1 = main.find('div', {'class': 'deck', 'each': 'cards'})
    section1 = div1.find('section', {'id': 'card-view/card/4a0a09c2-9e3f-4c1e-8657-3c2bd9fadd9f'})
    div2 = section1.find('div', {'class': 'deck', 'each': 'cards'})
    records = []
    filename = 'londoff_staff.csv'
    title_record = [['NAME', 'ROLE', 'PHONE', 'EMAIL', 'IMG_URL']]
    write_csv(title_record, filename)
    for j in div2.find_all(recursive=False):
        sections = j.find('div', {'class': 'deck', 'each': 'cards'}).find_all('section')
        for section in sections:
            content = section.find('div', {'class': 'content'})
            text = content.find('div', {'class': 'text'})
            media = content.find('div', {'class': 'media'})
            phone = email = name = role = figure = ''
            if text:
                try:
                    name_role = text.find('div', {'class': 'title'})
                    link_dev = text.find('div', {'class': 'link'}).find('div', {'class': 'tertiary'})
                    if link_dev.find('a', {'itemprop': 'telephone'}):
                        phone = link_dev.find('a', {'itemprop': 'telephone'}).text
                    if link_dev.find('a', {'itemprop': 'email'}):
                        email = link_dev.find('a', {'itemprop': 'email'})['href']
                    name_tag = name_role.find('h4').find_all('span')
                    name = ''
                    for sub_name in name_tag:
                        name += sub_name.text + ' '
                    name = name.strip()
                    role = name_role.find('p').text.strip()
                except:
                    continue
            if media:
                if media.find('figure'):
                    figure = media.find('figure').find('img')['data-src']
            record = [[name, role, phone, email, figure]]
            print(record)
            records.append(record)
            write_csv(record, filename)
get_contact_list(URL=URL)
