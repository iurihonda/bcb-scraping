import json
import requests
import pathlib

url_base = 'https://www.bcb.gov.br/api/servico/sitebcb/atascopom-conteudo/principal?filtro=IdentificadorUrl%20eq%20%27'

json_path = 'data/json/'
pathlib.Path(json_path).mkdir(parents=True, exist_ok=True)

html_path = 'data/html/'
pathlib.Path(html_path).mkdir(parents=True, exist_ok=True)

with open('crono_html.json', 'r') as jf:
    data = json.load(jf)

for item in data['conteudo']:
    identification = item['LinkPagina'].split('/')[-1]
    link = f"{url_base}{identification}%27"
    response = requests.get(link)
    data = json.loads(response.text)
    identification = identification[4:] + identification[2:4] + identification[0:2]
    with open(f'{json_path}{identification}.json', 'w') as jf:
        json.dump(data, jf)
    with open(f'{html_path}{identification}.html', 'w') as f:
        f.write(data['conteudo'][0]['OutrasInformacoes'])
