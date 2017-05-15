import os
import json
import math

filenames = [filename for filename in os.listdir('new-json') if '_trump' in filename]

for filename in filenames:
    outlet = filename.split('_')[0]
    filepath = os.path.join('new-json', filename)
    with open(filepath) as fp:
        l = len(json.loads(fp.read()))
    start = 0
    for end in xrange(220, l+1, 220):
        print 'python run_resolver.py', outlet, outlet + '_trump.xml', end, start
        start = end
        
        
        
    





