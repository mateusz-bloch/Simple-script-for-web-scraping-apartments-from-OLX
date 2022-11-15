from bs4 import BeautifulSoup
import requests
import pandas

def webscrapOLX(miasto, dzielnica = 'NULL'):

    nazwa = []
    cena = []
    metraz = []
    cena_za_metr = []
    miasta = []
    dzielnice = []
    i = 1 
    counter = 1

    print("Wyszukiwanie miasto:" + miasto)

    if dzielnica == 'NULL':
        OLX = 'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/' + miasto
    else:
        OLX = 'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/' + miasto + '/?search%5Bdistrict_id%5D=' + str(dzielnica)
    site = BeautifulSoup(requests.get(OLX).text, 'lxml')
    amount_positions = site.find('div', attrs={"data-testid": "total-count"}).text.split()
    amount_positions = int(amount_positions[(len(amount_positions))-2])

    while counter < amount_positions:
        data_stack = site.find_all('div', attrs={"data-cy": "l-card"})
        for data in data_stack:
            nazwa.append(data.find('h6').text)

            cena_temp = data.find('p').text
            cena_temp = cena_temp.replace(' ','',).replace('zł','').replace("donegocjacji","").replace(',',".")
            cena.append(float(cena_temp))

            metraz_temp = data.find('div', attrs={"color": "text-global-secondary"}).text
            metraz_temp = metraz_temp.split()
            metraz.append(float(metraz_temp[0].replace(',',".").replace('""','')))
            cena_za_metr.append(float(metraz_temp[3]))

            miasta.append(miasto)
            dzielnice.append(dzielnica)
            counter += 1
            if counter >= amount_positions: break
        i += 1
        if dzielnica == 'NULL':
            OLX = 'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/' + miasto + '?page=' + str(i)
        else:
            OLX = 'https://www.olx.pl/d/nieruchomosci/mieszkania/sprzedaz/' + miasto + '/?search%5Bdistrict_id%5D=' + str(dzielnica) + '%3Fpage%3D3&page=' + str(i)
        site = BeautifulSoup(requests.get(OLX).text, 'lxml')

    return pandas.DataFrame({'Ogloszenie':nazwa,'Cena(zł)':cena,'Metraz(m2)':metraz,'Cena za metr':cena_za_metr,'Miasto':miasta,'Dzielnica(KodOLX)':dzielnice})