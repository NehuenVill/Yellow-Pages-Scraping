import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

#srp-listing clickable-area paid-listing astro-dxc
#srp-listing clickable-area gump
#srp-listing clickable-area sp
#srp-listing clickable-area rd
#srp-listing clickable-area mdm

main_list = []

def extract(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    arts_1 = soup.find_all('div', class_ = 'srp-listing clickable-area paid-listing astro-dxc')
    arts_2 = soup.find_all('div', class_ = 'srp-listing clickable-area gump')
    arts_3 = soup.find_all('div', class_ = 'srp-listing clickable-area sp')
    arts_4 = soup.find_all('div', class_ = 'srp-listing clickable-area rd')
    arts_5 = soup.find_all('div', class_ = 'srp-listing clickable-area mdm')

    arts = arts_1 + arts_2 + arts_3 + arts_4 + arts_5

    return arts

def transform(articles):
    for item in articles:
        name = item.find('a', class_ = 'business-name').text
        address = item.find('p', class_ = 'adr').text.strip().replace('\n', '')
        try:
            website = item.find('a', class_ = 'track-visit-website')['href']
        except:
            website = 'NO WEBSITE'
        try:
            tel = item.find('div', class_ = 'phones phone primary').text.strip()
        except:
            tel = 'NO TELLEPHONE'

        business = {
            'Name': name,
            'Adress': address,
            'Website': website,
            'Tellephone': tel
        }

        main_list.append(business)

    return

def load():
    df = pd.DataFrame(main_list, columns= ["Name", "Adress", "Website", "Tellephone"])
    print(main_list)
    print(df)
    df.to_excel('LA_Dentists.xls', index= False, columns= ["Name", "Adress", "Website", "Tellephone"])

for x in range(1,3):
    print(f'Getting page {x}')
    
    try:
    
        articles = extract(f'https://www.yellowpages.com/search?search_terms=dentist&geo_location_terms=Los%20Angeles%2C%20CA&page={x}')
        transform(articles)
        time.sleep(2)

    except:

        break


load()
print('Saved to Excel')