from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions, EmotionOptions, MetadataOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions
import json

class Watson(object):

    def __init__(self):
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(version='2018-03-16', username='da73080e-f8e5-465c-b6df-a50caf6ec65a', password='u1u8mF05XvpI')

    def get_keywords(self,sentence):
        response = self. natural_language_understanding.analyze(
            text=sentence,
            return_analyzed_text='True',
            features=Features(concepts=ConceptsOptions(), categories=CategoriesOptions(), relations=RelationsOptions(), semantic_roles=SemanticRolesOptions(), sentiment=SentimentOptions(), entities=EntitiesOptions(), keywords=KeywordsOptions())).get_result()
        keywords = map(lambda x : (x['text'], x['type']), response['entities'])
        return keywords
