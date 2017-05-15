import sys
import json

resolved_input = sys.argv[1]
with open(resolved_input) as fp:
    resolveds = {kv[0]: kv[1] for kv in json.loads(fp.read())}

unresolved_input = sys.argv[2]
with open(unresolved_input) as fp:
    unresolveds = json.loads(fp.read())


output_filename = argv[3]
for idx, unresolved in unresolveds:
    unresolved['resolved'] = resolveds[idx]

with open(output_filename) as fp:
    fp.write(json.dumps(unresolveds))
