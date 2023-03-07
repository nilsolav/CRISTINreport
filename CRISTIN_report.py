from urllib.request import urlopen
import json
from pandas import json_normalize
import pandas as pd
import csv

# https://towardsdatascience.com/how-to-parse-json-data-with-python-pandas-f84fbd0b1025

# store the URL in url as parameter for urlopen
url = "http://api.cristin.no/ws/hentVarbeidSted?instnr=7431&avdnr=19&fra=2023&format=json"

# store the response of URL & extract data
response = urlopen(url)
data_json = json.loads(response.read())
resultat_structured = data_json['forskningsresultat']
resultat = pd.json_normalize(resultat_structured)

# Temporary file
file = '/mnt/c/DATAscratch/pubresults_detailed.csv'
resultat.to_csv(file)

# Extracting key information


authors = []
for _authors in resultat['fellesdata.person']:
    i = 0
    resauthors = []
    for author in _authors:
        i = i+1
        per = author['etternavn'] + ', ' + author['fornavn']
        if i < 5:
            resauthors.append(per)
        else:
            resauthors.append('et. al')
            break
    authors.append('; '.join(resauthors))

resultat['Forfattarar'] = pd.DataFrame(authors)
resultat.rename(columns = {
    'fellesdata.kategori.hovedkategori.navnEngelsk' : 'Kategori',
    'fellesdata.tittel' : 'Tittel'}, inplace = True)

results_clean = resultat[['Kategori', 'Forfattarar', 'Tittel']]
results_clean = results_clean.sort_values('Kategori')

file2 = 'CRISTIN_report.csv'
results_clean.to_csv(file2)
