import requests
import json
import pprint
import time
import paralleldots
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, ConceptsOptions, CategoriesOptions, EmotionOptions, MetadataOptions, RelationsOptions, SemanticRolesOptions, SentimentOptions
import subprocess
import stage1
import stage2
import stage3
import stage4

categories  = { "finance" : [
                            # "economics",
                            # "stock",
                            # "funding",
                            # "points",
                            # "nasdaq",
                            # "market",
                            # "monetory",
                            # "corporate",
                            # "banker",
                            # "investment",
                            # "business",
                            ],
                "economy" : [
                            # "taxes",
                            # "administration",
                            # "gdp",
                            # "fiscal",
                            # "congress",
                            # "budget",
                            # "per capita",
                            # "bureaucracy",
                            # "debt",
                            # "economy"
                            ],
                "climate": [
                            # "ice caps",
                            # "global warming",
                            # "climate change",
                            # "earth",
                            # "biosphere",
                            # "weather",
                            # "greenhouse gas",
                            # "atmosphere",
                            # "pollution",
                            ] ,
                "crime": [
                            # "gun",
                            # "theft",
                            # "law",
                            # "murder",
                            # "felony",
                            # "rape",
                            # "punishment",
                            # "fraud",
                            # "jurisdiction",
                            # "criminal",
                            # "kill",
                            # "homicide"
                            ] ,
                "immigration" : [
                            # "border",
                            # "border control",
                            # "emigration",
                            # "migration",
                            # "asylum",
                            # "refugee",
                            # "customs",
                            # "citizenship"
                            ] ,
                "unemployment": [
                            # "recession",
                            # "minimum wage",
                            # "poverty",
                            # "great depression",
                ],
                'Other' : [
                    'food',
                    'sport',
                    'greeting',
                    'jokes'
                    'humour'
                ]
                }

AUTH_KEY = 'KEY'
ParallelDotKeys = ['k2AglqzGPYrD7nDmVe4tAQIJmYDhcDRjja0ph1O03mg', 'rhztjeSb7iVjEgpvYkKzKIo31yNrJGZByfHsWvTtfss', 'G5aPEjhRdziRJYanRuUlMqX0cJjddj9ZzvYPqtDU35Q']

# natural_language_understanding = NaturalLanguageUnderstandingV1(version='2018-03-16', username='da73080e-f8e5-465c-b6df-a50caf6ec65a', password='u1u8mF05XvpI')

class Transcribe(object):
	def main(self):
		data = {

			"media_url" : "https://drive.google.com/file/d/1O6qi-tA3wl-8hGjfHu4p_B1lb6mGjO9O/view"
		}
		headers = {
				"Authorization" : "Bearer " + AUTH_KEY,
		}

		files = {'media': ('youtube.mp3', open('youtube.mp3', 'rb'), 'audio/mp3')}

		r = requests.post('https://api.rev.ai/revspeech/v1beta/jobs', headers=headers, files=files )
		result = r.json()

		id = 184821792
		while True:
		    results = self.retrieve(id)
		    print("Trying")
		    if(not (results == None)):
		        break

		self.write(results, categories)
		self.summarize()

		return(self.read())


	def isSentenceEnd(self, char):
		if char.strip() in ['.', '?', '!']:
			return True
		else:
			return False

	def retrieve(self, id):
		headers = {
				"Authorization" : "Bearer " + AUTH_KEY,
				'Accept' : 'application/vnd.rev.transcript.v1.0+json'
		}


		nr = requests.get('https://api.rev.ai/revspeech/v1beta/jobs/' + str(id) + '/transcript', headers =headers)
		result = nr.json()
		if('current_value' in result.keys() and result['current_value'] == 'in_progress' ):
			time.sleep(2)
			return None

		j = nr.json()['monologues']
		sentences = []

		for monologue in j:
			print('\n')
			print (monologue['speaker'], end=' \n')
			elements = monologue['elements']
			sentence = ""
			ts = 0
			e_ts = 0
			for element in elements:
				val = element['value']
				if sentence == '':
					if self.isSentenceEnd(val):
						pass
					else:
						ts = element['ts']
						sentence += val
				else:
					if self.isSentenceEnd(val):
						sentence += val
						sentences.append((sentence, ts, e_ts))
						sentence = ""
						ts = 0
						e_ts = 0
					elif not (element['type'] == 'punct'):
						sentence +=' ' + (element['value'])
						e_ts = element['end_ts']

		print(sentences)
		return sentences

	def write(self, sentences, categories):
		merged = " "
		for i in sentences:
			merged += i[0]
		data = {'id' : '100', 'text': merged}

		with open('text.json', 'w') as outfile:
			json.dump(data, outfile)

		data = {'sentences' : sentences}

		with open('transcribed.json', 'w') as outfile:
			json.dump(data, outfile)

	def summarize(self):
		subprocess.call('./bash.sh')

	def read(self):
		final = []
		count = 0
		paralleldots.set_api_key( ParallelDotKeys[count] )
		with open('output.json', 'r') as file:
			filtered_sentences = json.loads(file.read())
		with open('transcribed.json', 'r') as file:
			all_sentences = json.loads(file.read())
		for sentence in all_sentences['sentences']:
			if (sentence[0].strip() in filtered_sentences['sentences']):
				classification = paralleldots.custom_classifier( sentence[0], categories )
				while('taxonomy' not in classification.keys()):
					count += 1
					if (count >= len(ParallelDotKeys)):
						paralleldots.set_api_key( ParallelDotKeys[0] )
						count = 0
					else:
						paralleldots.set_api_key( ParallelDotKeys[count] )
					classification = paralleldots.custom_classifier( sentence[0], categories )
				if classification['taxonomy'][0]['confidence_score'] >= 0.85:
					temp = (sentence[0], sentence[1], sentence[2], classification['taxonomy'][0]['tag'])
					final.append(temp)

		return(final)
