import time
import sys

if len(sys.argv) < 2:
    print "Usage: python python_tests.py <size>"
    exit(0)

size = int(sys.argv[1])
print 'Accumulating Using For-Loop Size: %s' % size

t0 = time.time()
result = 0
for i in range(size):
    result += i
print 'Answer: %s\tTime Elapsed: %s seconds' % (result, (time.time()-t0))
