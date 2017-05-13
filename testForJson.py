import json
from pprint import pprint

with open('sample1.json') as data_file:
    data = json.load(data_file)

# pprint(data)
pprint(data["dataflow"])
print("\n")
pprint(data["layers"])
print("\n")
pprint(data["dataflow"]["D"])
