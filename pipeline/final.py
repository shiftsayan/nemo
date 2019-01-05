import json

def main():
	with open('output.json', 'r') as file:
		filtered_sentences = json.loads(file.read())
	with open('transcribed.json', 'r') as file:
		all_sentences = json.loads(file.read())
	for sentence in all_sentences['sentences']:
		if (sentence[0].strip() in filtered_sentences['sentences']):
			print(sentence)

main()
