""" This script checks the format of the anime corpus JSON file. """
import json
import os


DIR_TEST = os.path.dirname(os.path.abspath(__file__))
DIR_ROOT = os.path.dirname(DIR_TEST)
DIR_CORPUS = os.path.join(DIR_ROOT, 'corpus')
DIR_ANIME_JSON = os.path.join(DIR_CORPUS, 'anime_corpus.json')

with open(DIR_ANIME_JSON, 'r', encoding='utf-8') as f:
    anime_json = json.load(f)

if len(anime_json["train"]) < 1000:
    raise ValueError("The training set must contain at least 1000 entries.")

print("size=", len(anime_json["train"]))
print("ok, the anime corpus JSON file is valid.")
