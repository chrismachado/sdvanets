import numpy as np
import random


def make_dataset(days=30, hours=24, car_var=(1, 100, 100), min_var=0.5, target_values=(0, 1)):
    entry = []
    target = []
    for day in range(days):
        for hour in range(hours):
            cars = random.randint(car_var[0], car_var[1])
            cons = random.randint(0, car_var[2])
            entry.append([cars, cons, hour, 10.0/cars, 60.0/cars])

            variation = float(cons)/float(cars)  # Acceptance criteria

            if variation >= min_var:
                target.append(target_values[1])
            else:
                target.append(target_values[0])

    return np.array(entry, dtype=float), np.array(target, dtype=float)


def normalize(X):
    for i in range(X.shape[1]):
        imax = max(X[:, i])
        imin = min(X[:, i])
        for j in range(X.shape[0]):
            X[j, i] = (X[j, i] - imin)/(imax - imin)

