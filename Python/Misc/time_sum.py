from time import time

tic = time()
for i in range(0, 1000):
    x = sum(range(0, 100))
print time() - tic


tic = time()
for i in range(0, 1000):
    x = 0
    for ix in range(0, 100):
        x += ix
print time() - tic
