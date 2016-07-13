def foo(bar, result, index):
    print 'hello {0}'.format(bar)
    result[index] = "foo"+str(index)

from threading import Thread

num=8

threads = [None] * num
results = [None] * num

for i in range(len(threads)):
    threads[i] = Thread(target=foo, args=('world!', results, i))
    threads[i].start()

# do some other stuff

for i in range(len(threads)):
    threads[i].join()

print " ".join(results)  # what sound does a metasyntactic locomotive make?