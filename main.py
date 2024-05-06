# playground. Don't pay attention
from copy import deepcopy
import json


with open('usa_colleges.json', 'r') as f:
    unis = json.loads(f.read())

universities = []
for i in unis:
    item = deepcopy(i)
    if not item.get('emails'):
        item['emails'] = []
    if not item.get('phone_numbers'):
        item['phone_numbers'] = []
    universities.append(item)
        

with open('usa_colleges.json', 'w') as f:
    f.write(json.dumps(universities))
