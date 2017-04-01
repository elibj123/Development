import random
import math
from matplotlib import pyplot
import itertools


def avg(v):
    return sum(v)/len(v)


def linear_regression(xy_list):
    mean_x2 = avg([xy[0]*xy[0] for xy in xy_list])
    mean_x = avg([xy[0] for xy in xy_list])
    mean_xy = avg([xy[0]*xy[1] for xy in xy_list])
    mean_y = avg([xy[1] for xy in xy_list])

    var_x = mean_x2 - mean_x*mean_x
    cov_xy = mean_xy - mean_x*mean_y

    a_hat = cov_xy / var_x
    b_hat = (mean_x2*mean_y - mean_x*mean_xy) / var_x

    return a_hat, b_hat


def bootstrap_linear_regression(xy_list, sigma):
    n = len(xy_list)
    y_list = [xy[1] for xy in xy_list]

    max_count = 0
    for i in range(0, 10):
        subset = random.sample(xy_list, int(math.floor(n/10)))
        a_strap, b_strap = linear_regression(subset)
        y_strap = [a_strap*xy[0] + b_strap for xy in xy_list]
        y_comp = list(zip(y_list, y_strap))

        good_points = [abs(y[0]-y[1]) <= 5*sigma for y in y_comp]
        count = sum(good_points)
        if count > max_count:
            max_count = count
            max_good_points = good_points

    strapped_xy_list = list(itertools.compress(xy_list, max_good_points))

    a_hat, b_hat = linear_regression(strapped_xy_list)
    return a_hat, b_hat, max_good_points


autoMode = 1

if autoMode == 1:
    a_true = 10
    b_true = 5
    sigma = 10
    n = 1000
    print "True slope is %f" % a_true
    print "True interception point is %f" % b_true
    print "Noise std is %f" % sigma
    print "Number of points is %d" % n

else:
    a_true = float(raw_input('Enter slope: '))
    b_true = float(raw_input('Enter interception point: '))
    sigma = float(raw_input('Enter noise std: '))
    n = int(raw_input('Enter number of points: '))

x_list = range(0, n)
y_list = [a_true*x + b_true + random.gauss(0, sigma) for x in x_list]

num_bad_points = 100
for i in random.sample(range(0, int(math.floor(n/10))), num_bad_points):
    y_list[i] += 1000*random.random()

for i in random.sample(range(n - int(math.floor(n/10)), n), num_bad_points):
    y_list[i] -= 1000*random.random()

xy_list = list(zip(x_list, y_list))

a_hat, b_hat = linear_regression(xy_list)
good_points = [True] * n

a_hat, b_hat, good_points = bootstrap_linear_regression(xy_list, sigma)

x_est = range(0, n)
y_est = [a_hat*x + b_hat for x in x_est]
print "Estimated slope is %f" % a_hat
print "Estimated interception point is %f" % b_hat

figHandle = pyplot.figure()

for x, y, g in zip(x_list, y_list, good_points):
    if g:
        pyplot.scatter(x, y, color = 'b')
    else:
        pyplot.scatter(x, y, color = 'k')
pyplot.plot(x_est, y_est, 'r')
pyplot.show()