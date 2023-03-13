from urllib.request import urlopen
import json

# https://api.cristin.no/v2/projects/2497164
# https://towardsdatascience.com/how-to-parse-json-data-with-python-pandas-f84fbd0b1025


def parseauthors(_authors):
    i = 0
    resauthors = []
    for author in _authors:
        i = i+1
        per = author['surname'] + ', ' + author['first_name']
        if i < 5:
            resauthors.append(per)
        else:
            resauthors.append('et. al')
            break
    return resauthors


# store the URL for CRIMAC in url as parameter for urlopen
url = "https://api.cristin.no/v2/projects/2497164"

# List of categories
#categories = json.loads(urlopen('https://api.cristin.no/v2/results/categories?lang=en').read())
#for _category in categories:
#    print(_category['name']['en'])

# Read results from project
response = urlopen(url)
data_json = json.loads(response.read())
results = data_json['results']

# Types of contributions
contributions = ['Academic article', 'Academic lecture', 'Poster',
                 'Masters thesis', 'Report',
                 'Article in business/trade/industry journal',
                 'Feature article', 'Interview', 'Reader opinion piece']

Ac_art = []
Ac_lec = []
Poster = []
Masters_thesis = []
Report = []
Art_business = []
Feat_art = []
Interview = []
Opinion_piece = []

dat = []
for _result in results:
    response = urlopen(_result)
    data_json = json.loads(response.read())
    _authors = data_json['contributors']['preview']
    auth = '; '.join(parseauthors(_authors))
    cat = data_json['category']['name']['en']
    year = data_json['year_published']
    title = data_json['title'][list(data_json['title'].keys())[0]].strip()
    cat = [data_json['category']['name']['en']][0]

    if cat == 'Academic article':
        pub = '. '.join([data_json['journal']['name']])
        Ac_art.append('. '.join([auth, year, title, pub]))
    elif cat == 'Academic lecture':
        pub = data_json['event']['name']
        Ac_lec.append('. '.join([auth, year, title, pub]))
    elif cat == 'Poster':
        pub = data_json['event']['name']
        Poster.append('. '.join([auth, year, title, pub]))        
    elif cat == 'Masters thesis':
        auth = ', '.join([_authors[0]['surname'], _authors[0]['first_name']])
        pub = data_json['publisher']['name']
        Masters_thesis.append('. '.join([auth, year, title, pub]))
    elif cat == 'Report':
        pub = data_json['publisher']['name']
        Report.append('. '.join([auth, year, title, pub]))
    elif cat == 'Article in business/trade/industry journal':
        pub = data_json['journal']['name']
        Art_business.append('. '.join([auth, year, title, pub]))
    elif cat == 'Feature article':
        pub = data_json['journal']['name']
        Feat_art.append('. '.join([auth, year, title, pub]))
    elif cat == 'Interview':
        pub = '' # data_json['journal']['name']
        Interview.append('. '.join([auth, year, title, pub]))
    elif cat == 'Reader opinion piece':
        pub = data_json['journal']['name']
        Opinion_piece.append('. '.join([auth, year, title, pub]))
    else:
        print('Category missing: '+cat)


file2 = '/mnt/c/DATAscratch/CRISTIN_CRIMAC_report.txt'
with open(file2, "w") as text_file:
    text_file.write('Peer reviewed publications\n\n')
    text_file.write('\n'.join(sorted(Ac_art)))
    text_file.write('\n\nAcademic lecture\n\n')
    text_file.write('\n'.join(sorted(Ac_lec)))
    text_file.write('\n\nPosters\n\n')
    text_file.write('\n'.join(sorted(Poster)))
    text_file.write('\n\nMasters thesis\n\n')
    text_file.write('\n'.join(sorted(Masters_thesis)))
    text_file.write('\n\nReport\n\n')
    text_file.write('\n'.join(sorted(Report)))
    text_file.write('\n\nBusiness journal publication\n\n')
    text_file.write('\n'.join(sorted(Art_business)))
    text_file.write('\n\nDissemination\n\n')
    text_file.write('\n\nFeature article\n\n')
    text_file.write('\n'.join(sorted(Feat_art)))
    text_file.write('\n\nInterview\n\n')
    text_file.write('\n'.join(sorted(Interview)))
    text_file.write('\n\nReder Opinion Piece\n\n')
    text_file.write('\n'.join(sorted(Opinion_piece)))




