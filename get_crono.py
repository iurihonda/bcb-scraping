import json
import requests
import pathlib

headers = {'content-type': 'application/json'}

url_base = 'https://www.bcb.gov.br/'
url_pdf = f'{url_base}api/servico/sitebcb/atascopom/ultimas?quantidade=1000&filtro='
url_html = f'{url_base}api/servico/sitebcb/atascopom-conteudo/ultimas?quantidade=1000&filtro='

crono_path = 'data/crono/'
pathlib.Path(crono_path).mkdir(parents=True, exist_ok=True)

def get_crono(url, filename):
    response = requests.get(url=url, headers=headers)
    data = json.loads(response.text)
    with open(filename, 'w') as jf:
        json.dump(data, jf)

get_crono(url_pdf, f'{crono_path}crono_pdf.json')
get_crono(url_html, f'{crono_path}crono_html.json')
