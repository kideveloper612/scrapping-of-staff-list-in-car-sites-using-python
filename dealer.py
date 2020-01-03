import requests
import os
import csv

Base_URL = "http://api.marketcheck.com/v1"
api_key = "zmjA831xdvmIXl0AQ4JGM7U7pRuVA1BV"

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

def single_pagenate(start):
    URL = Base_URL + "/dealers?api_key=%s&rows=%s&start=%s" % (api_key, 50, start)
    header = {
        'Host': 'marketcheck-prod.apigee.net'
    }
    response = requests.get(url=URL, headers=header)
    return response

results = [['ID', 'SELLER_NAME', 'INVENTORY_URL', 'DATA_SOURCE', 'STATUS', 'DEALER_TYPE', 'STREET', 'CITY', 'STATE', 'COUNTRY', 'ZIP', 'LATITUDE', 'LONGITUDE', 'SELLER_PHONE']]
write_csv(results, 'dealer_list.csv')
results = []
def get_all_dealers():
    start = 0
    while True:
        single_res = single_pagenate(start=start)
        if single_res.status_code != 200:
            break
        for dealer in single_res.json()['dealers']:
            try:
                id = dealer['id']
                seller_name = dealer['seller_name']
                inventory_url = dealer['inventory_url']
                data_source = dealer['data_source']
                status = dealer['status']
                dealer_type = dealer['dealer_type']
                street = dealer['street']
                city = dealer['city']
                state = dealer['state']
                country = dealer['country']
                zip = dealer['zip']
                latitude = dealer['latitude']
                longitude = dealer['longitude']
                seller_phone = dealer['seller_phone']
                print(id, seller_name, inventory_url, data_source, status, dealer_type, street, city, state, country, zip, latitude, longitude, seller_phone)
                results.append([id, seller_name, inventory_url, data_source, status, dealer_type, street, city, state, country, zip, latitude, longitude, seller_phone])
            except:
                continue
        start += 50
        write_csv(results, 'dealer_list.csv')
get_all_dealers()

