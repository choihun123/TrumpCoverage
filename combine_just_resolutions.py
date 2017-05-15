import sys
import json

resolutions_input = sys.argv[1]
with open(resolutions_input) as fp:
    resolutions = {kv[0]: kv[1] for kv in json.loads(fp.read())}

unresolved_input = sys.argv[2]
with open(unresolved_input) as fp:
    unresolveds = json.loads(fp.read())

for idx, unresolved in enumerate(unresolveds):
    
    unresolved['resolutions'] = resolutions.get(idx, None)

output_filename = sys.argv[3]    
with open(output_filename, 'w+') as fp:
    fp.write(json.dumps(unresolveds))
