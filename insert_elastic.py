from elasticsearch import Elasticsearch
import pathlib
import json

host = 'localhost'
port = 9200
input_path = 'data/html/'

index_settings = {
    'name': 'copom',
    'type': 'publications',
    'settings': {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 0
        },
        'mappings': {
            'members': {
                'dynamic': 'strict',
                'properties': {
                    'title': {
                        'type': 'text'
                    },
                    'content': {
                        'type': 'text'
                    },
                    'clean': {
                        'type': 'text'
                    }
                }
            }
        }
    }
}

def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': host, 'port': port}])
    if _es.ping():
        print('Connected to Elasticsearch')
    else:
        print('Could not connect to Elasticsearch')
    return _es

def create_index(es_object, index_name):
    created = False
    settings = index_settings['settings']
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(index=index_name, ignore=400, body=settings)
        created = True
    except Exception as e:
        print(str(e))
    finally:
        return created

def store_record(elastic_object, index_name, doc_type, record):
    is_stored = True
    try:
        outcome = elastic_object.index(index=index_name, doc_type=doc_type, body=record)
        print(outcome)
    except Exception as e:
        print('Error in indexing data:')
        print(str(e))
        is_stored = False
    finally:
        return is_stored

def generate_data(dataset, index_name, doc_type):
    for proc in dataset:
        data = {
            '_index': index_name,
            '_type': doc_type
        }
        yield data

dataGen = genData(json_data)
        
for success, info in helpers.parallel_bulk(es, list(dataGen), thread_count=16):
    if not success:
        print('A document failed:', info)

    print(es.indices.refresh())
    print(es.count(index=indexName))

if __name__ == '__main__':
    es = connect_elasticsearch()
    if  es is not None:
        with open('20040225.json', 'r') as jf:
            result = json.load(jf)
        if create_index(es, index_settings['name']):
            print(f'Successfully created index')
            out = store_record(es, index_settings['name'], index_settings['type'], result)
