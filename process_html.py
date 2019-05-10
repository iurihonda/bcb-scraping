from bs4 import BeautifulSoup
import pathlib
from pprint import pprint
import re
import json

input_path = 'data/html/'
output_path = 'data/processed/html/'
pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

def clean_content(text):
    clean = re.sub(r'^\s+', '', text)
    clean = re.sub(r'(?<=\w)\n(?=\w)', ' ', clean)
    clean = re.sub(r'(?<=\d\.)\n(?=\w)', ' ', clean)
    clean = re.sub(r'(?<!\.)\s*\n(?=\w)', ' ', clean)
    clean = re.sub(r'(?<=\.)\s*\d{1,2}\.\s*(?=\d{1,2})', r'\n', clean)
    clean = re.sub(r'(?<=\.)\s*\d{1,2}\.$', '', clean)
    return clean

for f in pathlib.Path(input_path).glob('*.html'):
    soup = BeautifulSoup(open(f), 'html.parser')
    sections = []
    for a in soup.find_all('a', href=True):
        nextNode = soup.find('a', {'name': a['href'][1:]})
        content = []
        while True:
            if nextNode:
                nextNode = nextNode.next_element
                try:
                    tag_name = nextNode.name
                    tag_text = nextNode.text
                except AttributeError:
                    tag_name = ''
                    tag_text = ''
                if tag_name == 'a':
                    break
                if tag_name != 'i' and tag_name != 'b' and tag_name != 'strong':
                    content.append(tag_text)
            else:
                break
        content = list(filter(None, content))
        content = content[:-1]
        content = '\n'.join(content)
        sections.append({
            'title': re.sub('\s+', ' ', a.text.strip()),
            'content': content,
            'clean': clean_content(content)
        })
    with open(f'{output_path}{f.stem}.json', 'w') as jf:
        json.dump(sections, jf)
