from kensho import get_pandas_graph_client
from timeline_types import timeline_types
import json
# client = get_pandas_graph_client('https://www.kensho.com/external/v1', '2db502719b914d7371f6343e4f498262f1e95797')
# print(json.dumps(client.get_calendar('2018-05-23','2018-05-27'), indent=2))
# print(json.dumps(client.get_ongoing_episodes('2018-05-23','2018-05-27'), indent=2))

class Kensho(object):

    def __init__(self, retries=1):
        self._client = get_pandas_graph_client('https://www.kensho.com/external/v1', '2db502719b914d7371f6343e4f498262f1e95797')

    def get_finance_events(self, start_time, end_time, search_term, category):
        query = self._client.get_calendar(start_time, end_time)
        events = filter(lambda x : timeline_types[x['timeline_types']] == category, query.json['data'])
        if search_term != "": events = filter(lambda x : search_term in x['event_description'], query.json['data'])
        return events

    def get_climate_events(self, start_time, end_time, category):
        query = self._client.get_calendar(start_time, end_time)
        events = filter(lambda x : timeline_types[x['timeline_types']] == category, query.json['data'])
        return events

    def get_unemployment_events(self, start_time, end_time, category):
        query = self._client.get_calendar(start_time, end_time)
        events = filter(lambda x : timeline_types[x['timeline_types']] == category, query.json['data'])
        return events

    def get_government_events(self, start_time, end_time, category):
        query = self._client.get_calendar(start_time, end_time)
        events = filter(lambda x : timeline_types[x['timeline_types']] == category, query.json['data'])
        return events

    def get_crime_events(self, start_time, end_time, category):
        query = self._client.get_calendar(start_time, end_time)
        events = filter(lambda x : timeline_types[x['timeline_types']] == category, query.json['data'])
        return events

    def get_immigration_events(self, start_time, end_time, category):
        query = self._client.get_calendar(start_time, end_time)
        events = filter(lambda x : timeline_types[x['timeline_types']] == category, query.json['data'])
        return events
