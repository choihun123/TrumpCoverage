import sys
import os
import json

from subprocess import Popen
from multiprocessing import Pool

NUM_THREADS = 30

output_dir = sys.argv[1]
input_filename = sys.argv[2]
end_num = int(sys.argv[3])

if len(sys.argv) == 5:
    start_num = int(sys.argv[4])
else:
    start_num = 0

def targ(idx):
    path = os.path.join(output_dir, str(idx))
    cmd = ["java", "-cp", "stanford-corenlp-full-2016-10-31/*:.", "CorefFinder", input_filename, path, str(idx)]
    process = Popen(cmd)
    process.wait()
    print 'done', idx

def main():
    p = Pool(NUM_THREADS)
    p.map(targ, range(start_num, end_num + 1, 5))


if __name__ == '__main__':
    main()
