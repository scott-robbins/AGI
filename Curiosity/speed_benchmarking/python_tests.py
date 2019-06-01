import time

size = 1000000
print 'Using Array Size: %s' % size

t0 = time.time()
result = 0
for i in range(size):
    result += i
print 'Answer: %s\tTime Elapsed: %s seconds' % (result, (time.time()-t0))
