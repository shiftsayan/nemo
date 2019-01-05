from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import datetime
from flask_cors import CORS

from youtube import CustomYouTube
from kensho_tests import Kensho
from watson import Watson
from timeline_types import timeline_types

import requests
from transcribe import Transcribe
import json
import re
from string import punctuation
import ast

app = Flask(__name__)
CORS(app)
api = Api(app)
wat = Watson()
Kensho = Kensho()

transcribe = Transcribe()

class Res(Resource):

    def get(self):
        pass

    def post(self):

        def parse(response, type):
            str = response.text
            str = str.replace('{', '[')
            str = str.replace('}', ']')
            str = str.replace('*^', '*')

            if (type == 'finance'):
                str = str[2:-2]
                str = re.sub(r"Entity\[[\s\"\'\-,:a-zA-Z0-9]*\]\s->\s(\$Failed)*(,)*", '', str)
                str = str.strip(', ')

            try:
                l = eval(str)
                return l
            except:
                print("Failed...")
                pass

        def format_datetime(t,category):
            if category in ['climate','government']:
                return dt.fromtimestamp(t).strftime('%Y-%m-%d')
            else:
                dt2 = []
                for d in t:
                    dt2.append(str(d))
                return '-'.join(dt2)

        def get_start_and_end(elements):
            min = elements[0][0]
            max = elements[0][0]
            for el in elements:
                if el[0] > max: max = el[0]
                if el[0] < min: min = el[0]
            return (format_datetime(min), format_datetime(max))

        yt = CustomYouTube()
        yt.save_clip(request.values['url'])
        corpus = transcribe.main()

        payload = []

        for corpse in corpus:
            sentence, start, end, category = corpse
            dataElem = {}
            if category == "finance":
                try:
                    keywords = watson.get_keywords(sentence)
                    search_term = filter(lambda x, y: y == "Company", keywords)[0][0]
                except:
                    search_term = ""

                wolfram = requests.get("https://www.wolframcloud.com/objects/16cd3aae-8120-45be-b052-17d6e010864a?text=" + sentence )

                data = parse(wolfram, 'finance')
                if data:
                    series = []
                    if (len(data) > 5):
                        counter = 0
                        for i in data:
                            series.append({'name' : counter, "value" : i[1]})
                            counter += 1
                        dataElem['startTime'] = start
                        dataElem['endTime'] = end
                        dataElem['name'] = category
                        dataElem['series'] = series
                    start_time, end_time = get_start_and_end(wolfram)

                # wolfram = map(lambda x : x, wolfram)
                # kensho  = Kensho.get_finance_events(start_time, end_time, search_term, category)

            elif category == "climate":
                wolfram = requests.get("https://www.wolframcloud.com/objects/10970734-bd5a-4850-a0fe-e7557cde86a2?text=" + sentence)
                data = parse(wolfram, 'climate')
                series = []
                if data:
                    series = []
                    if (len(data) > 5):
                        counter = 0
                        for i in data:
                            series.append({'name' : counter, "value" : i[1]})
                            counter += 1
                        dataElem['startTime'] = start
                        dataElem['endTime'] = end
                        dataElem['name'] = category
                        dataElem['series'] = series
                        counter += 1
                    start_time, end_time = get_start_and_end(wolfram)

                start_time, end_time = get_start_and_end(wolfram)
                # wolfram = map(lambda x : x, wolfram)
                # kensho  = Kensho.get_climate_events(start_time, end_time, category)

            elif category == "unemployment":
                wolfram = requests.get("https://www.wolframcloud.com/objects/12982256-3b25-4e62-9578-9b304382594c?text=" + sentence )
                data = parse(wolfram, 'unemployment')
                series = []
                if data:
                    series = []
                    if (len(data) > 5):
                        counter = 0
                        for i in data:
                            series.append({'name' : counter, "value" : i[1]})
                            counter += 1
                        dataElem['startTime'] = start
                        dataElem['endTime'] = end
                        dataElem['name'] = category
                        dataElem['series'] = series
                        counter += 1
                    start_time, end_time = get_start_and_end(wolfram)

                start_time, end_time = get_start_and_end(wolfram)
                # wolfram = map(lambda x : x, wolfram)
                # kensho  = Kensho.get_unemployment_events(start_time, end_time, category)

            elif category == "economy":
                wolfram = requests.get("https://www.wolframcloud.com/objects/d7b3d0f7-4e10-45eb-ae50-da4f7fa808a2?text=" + sentence)
                data = parse(wolfram, 'government')
                series = []
                if data:
                    series = []
                    if (len(data) > 5):

                        counter = 0
                        for i in data:
                            series.append({'name' : counter, "value" : i[1]})
                            counter += 1
                        dataElem['startTime'] = start
                        dataElem['endTime'] = end
                        dataElem['name'] = category
                        dataElem['series'] = series
                        counter += 1
                    start_time, end_time = get_start_and_end(wolfram)

                start_time, end_time = get_start_and_end(wolfram)
                # kensho  = Kensho.get_government_events(start_time, end_time, category)

            elif category == "crime":
                wolfram = requests.get("https://www.wolframcloud.com/objects/37c3b900-9290-447a-a7dd-22e47a142273?text=" + sentence )

                data = parse(wolfram, 'crime')
                series = []
                if data:
                    series = []
                    if (len(data) > 5):
                        counter = 0
                        for i in data:
                            series.append({'name' : counter, "value" : i[1]})
                            counter += 1
                        dataElem['startTime'] = start
                        dataElem['endTime'] = end
                        dataElem['name'] = category
                        dataElem['series'] = series
                        counter += 1
                    start_time, end_time = get_start_and_end(wolfram)

                start_time, end_time = get_start_and_end(wolfram)
                # wolfram = map(lambda x : x, wolfram)
                # kensho  = Kensho.get_crime_events(start_time, end_time, category)

            elif category == "immigration":
                wolfram = requests.get("https://www.wolframcloud.com/objects/6c601718-732f-4743-b665-633519ff9f98?text=" + sentence )

                data = parse(wolfram, 'immigration')
                series = []
                if data:
                    series = []
                    if (len(data) > 5):
                        counter = 0
                        for i in data:
                            series.append({'name' : counter, "value" : i[1]})
                            counter += 1
                        dataElem['startTime'] = start
                        dataElem['endTime'] = end
                        dataElem['name'] = category
                        dataElem['series'] = series
                        counter += 1
                    start_time, end_time = get_start_and_end(wolfram)

                start_time, end_time = get_start_and_end(wolfram)
                # wolfram = map(lambda x : x, wolfram)
                # kensho  = Kensho.get_immigration_events(start_time, end_time, category)

            payload.append(dataElem)

        return payload

    def put(self, url):
        pass

    def delete(self, url):
        pass

api.add_resource(Res, "/api")
app.run(host='0.0.0.0', debug=True) # remove debug=True when finally deploying
