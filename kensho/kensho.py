import os

import pandas as pd
import requests


def _api_result_to_frame(api_result):
    """Convert API result into dataframe"""
    ordered_columns = [c['key'] for c in api_result['metadata']]
    # Create the dataframe
    return api_result['data']
    df = pd.DataFrame(api_result['data'])
    
    existence_filtered_columns = [c for c in ordered_columns if c in df.columns]
    reordered_frame = df[existence_filtered_columns]

    for column in api_result['metadata']:
        if column['key'] not in reordered_frame.columns:
            continue
        if column['unit'] == 'DateTime' or column['unit'] == 'Date':
            reordered_frame[column['key']] = pd.to_datetime(reordered_frame[column['key']])
    return reordered_frame


class _KenshoGraphClient(object):
    """Basic implementation of the Kensho Graph API client"""

    def __init__(self, host, api_key, converter_func, retries=1):
        """Initialize the client"""
        self._host = host
        self._api_key = api_key
        self._retries = retries
        self._converter_func = converter_func

    def list_entity_classes(self):
        """List all available entity classes"""
        return self._get_json_or_raise('list_entity_classes')

    def get_class_relationships(self, class_name):
        """Return all potential relationships of an entity of this class"""
        return self._get_json_or_raise(
            'get_class_relationships', class_name=class_name)

    def search_entities(self, class_name, search_string):
        """Search entities of the class_name that match search_string"""
        return self._get_json_or_raise(
            'search_entities', class_name=class_name, search_string=search_string)

    def list_entities_of_class(self, class_name):
        """List all entities of class"""
        return self._get_json_or_raise(
            'list_entities_of_class', class_name=class_name)

    def get_entity(self, entity_id):
        """Get entity by id"""
        return self._get_json_or_raise('get_entity', entity_id=entity_id)

    def get_related_entities(self, entity_id, relationship):
        """Get all entities related by one identified by entity_id by 'relationship'"""
        return self._get_json_or_raise(
            'get_related_entities', entity_id=entity_id, relationship=relationship)

    def get_timeline(self, timeline_id, start_date=None, end_date=None):
        """Get all events in a timeline. Optionally bound by start and end dates"""
        return self._get_json_or_raise(
            'get_timeline', timeline_id=timeline_id, start_date=start_date, end_date=end_date)

    def get_calendar(self, start_date, end_date):
        """Get all events happening in the interval [start_date, end_date)"""
        return self._get_json_or_raise('get_calendar', start_date=start_date, end_date=end_date)

    def get_ongoing_episodes(self, start_date, end_date):
        """Get all episodes ongoing in the interval [start_date, end_date)"""
        return self._get_json_or_raise(
            'get_ongoing_episodes', start_date=start_date, end_date=end_date)

    def translate_asset_id(self, id_type, asset_id):
        """Given an identification string for an asset return all known identifiers"""
        return self._get_json_or_raise('translate_asset_id', id_type=id_type, asset_id=asset_id)

    def list_timeline_types(self):
        """Given an identification string for an asset return all known identifiers"""
        return self._get_json_or_raise('list_timeline_types')

    
    def _get_json_or_raise(self, function, **kwargs):
        """Get json from a given url. Uses get_with_retries underneath"""
        session = requests.Session()
        session.mount('https://', requests.adapters.HTTPAdapter(max_retries=self._retries))
        full_url = '/'.join([self._host.rstrip('/'), function.lstrip('/')])
        headers = {
            'Authorization': 'Token {}'.format(self._api_key),
            'Content-Type': 'application/json'
        }
        response = session.get(full_url, headers=headers, params=kwargs)
        response.raise_for_status()
        result_json = response.json()
        return self._converter_func(result_json)


def get_json_graph_client(host, api_key, retries=1):
    """Get a client that returns raw json"""
    return _KenshoGraphClient(host, api_key, lambda x: x, retries=retries)


def get_pandas_graph_client(host, api_key, retries=1):
    """Get a client that returns raw json"""
    return _KenshoGraphClient(
        host, api_key, _api_result_to_frame, retries=retries)