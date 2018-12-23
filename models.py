# coding: UTF-8
from google.cloud import datastore

client = datastore.Client()

class EventModel():
    @staticmethod
    def get(limit=100):
        q = client.query(kind='Event')
        return q.fetch(limit=limit)

    @staticmethod
    def get_dict(limit=100):
        return [_entity_to_dict(e) for e in EventModel.get(limit)]

    @staticmethod
    def put(dict_list):
        entities = []
        for d in dict_list:
            entity = datastore.Entity(key=client.key('Event', d['url']))
            entity.update({
                'name': d['name'],
                'organizer': d['organizer'],
                'description': d['description'],
                'location': d['location']['name'],
                'date': d['startDate'],
                'url': d['url']
            })
            entities.append(entity)
        client.put_multi(entities)

    @staticmethod
    def delete():
        q = client.query(kind='Qiita').keys_only()
        client.delete_multi(q)


def _entity_to_dict(entity):
    _list = entity.items()
    _dict = {}
    for x in _list:
        _dict[x[0]] = x[1]
    return _dict
