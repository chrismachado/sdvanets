from sklearn.linear_model import Perceptron
from datasets import normalize
import math


class Decider(object):
    def __init__(self, inputs, name):
        self._inputs = inputs
        self.clf = Perceptron(max_iter=1000, eta0=0.15, tol=1e-3)
        self.name = name

    def set_inputs(self, new_inputs):
        self._inputs = new_inputs

    def get_inputs(self):
        return self._inputs

    def verify_road(self):
        return self.clf.predict(self._inputs)

    def eval(self, hour=None):
        if not len(self._inputs):
            return -1

        if hour is not None:
            inputs_ = [i for i in self._inputs if i[2] == hour]
        else:
            inputs_ = self._inputs

        rvalue = 0
        for inputs in inputs_:
            rvalue += (inputs[1] + (inputs[3] / inputs[4])) / inputs[0]
        return rvalue / len(inputs_)



