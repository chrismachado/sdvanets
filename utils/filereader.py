import numpy as np


def read_inputs(path, filename):
    samples = []
    with open('%s/%s' % (path, filename), 'r') as file:
        for line in file.readlines():
            line_ = list(map(float, line.split(',')))
            samples.append(line_)

    return np.array(samples)