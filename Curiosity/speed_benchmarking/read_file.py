import time
import sys


if len(sys.argv) < 2:
    print 'Usage: python read_file.py <file_name>'
    exit(0)
print 'Reading: %s' % sys.argv[1]
t0 = time.time()
data = list()
[data.append(line.replace('\n', '')) for line in open(sys.argv[1], 'r').readlines()]

print '%d Lines Read\t %fs Elapsed' % (len(data), time.time() - t0)
