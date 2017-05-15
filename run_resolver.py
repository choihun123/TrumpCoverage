import sys
import os
import json

from subprocess import Popen


output_dir = sys.argv[1]
input_filename = sys.argv[2]
end_num = int(sys.argv[3])

if len(sys.argv) != 5:
    start_num = 0
else:
    start_num = int(sys.argv[4])

cmd = ["java", "-cp", "stanford-corenlp-full-2016-10-31/*:.", "CorefReplacerP", input_filename]

processes = []
print start_num, end_num
for idx in xrange(start_num, end_num, 5):
    print idx
    path = os.path.join(output_dir, str(idx))
    cmd.append(path)
    cmd.append(str(idx))
    
    p = Popen(cmd)
    processes.append(p)
    
    cmd.pop()
    cmd.pop()

for process in processes:
    process.wait()

    
