# coding: UTF-8
from google.cloud import datastore

client = datastore.Client()

class QiitaModel():
    @staticmethod
    def get(limit=100):
        q = client.query(kind='Qiita')
        return q.fetch(limit=limit)

    @staticmethod
    def get_dict(limit=100):
        return [_entity_to_dict(e) for e in QiitaModel.get(limit)]

    @staticmethod
    def put(dict_list):
        entities = []
        for d in dict_list:
            entity = datastore.Entity(key=client.key('Qiita', d['id']))
            entity.update({
                'title': d['title'],
                'user_id': d['user']['id'],
                'url': d['url']
            })
            entities.append(entity)
        client.put_multi(entities)

    @staticmethod
    def delete():
        q = client.query(kind='Qiita')
        client.delete_multi(q.keys_only())


def _entity_to_dict(entity):
    _list = entity.items()
    _dict = {}
    for x in _list:
        _dict[x[0]] = x[1]
    return _dict
