import json
import requests
import pathlib

url_base = 'https://www.bcb.gov.br'

data_path = 'data/pdf/'
pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)

with open('crono_pdf.json', 'r') as jf:
    data = json.load(jf)

for item in data['conteudo']:
    link = f"{url_base}{item['Url']}"
    filepath = data_path + item['Url'].split('/')[-1]
    response = requests.get(link)
    with open(filepath, 'wb') as f:
        f.write(response.content)
