#Input
# nazwa_sklepu=asdasd&adres_sklepu=2323&powierzchnia=535353
#Output:
"""
slownik = {
    nazwa_sklepu: 'asdasd',
    adres_sklepu: '2323',
    powierzchnia: '535353'
}
"""

def parsuj(dane):
    parsed_string = dane.split('=')
    dic = {}
    dic['nazwa_sklepu'] = parsed_string[1].split('&')[0]
    dic['adres_sklepu'] = parsed_string[2].split('&')[0]
    dic['powierzchnia'] = parsed_string[3]
    return dic
    

data = 'nazwa_sklepu=asdasd&adres_sklepu=2323&powierzchnia=535353'
print(parsuj(data))
