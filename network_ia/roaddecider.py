from sklearn.linear_model import Perceptron


class Decider(object):
    def __init__(self, inputs, name):
        self.__inputs = inputs
        self.clf = Perceptron(max_iter=1000, eta0=0.15, tol=1e-3)
        self.name = name

    def set_inputs(self, new_inputs):
        self.__inputs = new_inputs

    def get_inputs(self):
        return self.__inputs

    def verify_road(self):
        return self.clf.predict(self.__inputs)

    def eval(self, hour=None):
        if not len(self.__inputs):
            return -1

        if hour is not None:
            inputs_ = [i for i in self.__inputs if i[2] == hour]
        else:
            inputs_ = self.__inputs

        rvalue = 0
        for inputs in inputs_:
            rvalue += (inputs[1] + inputs[3] + inputs[4]) / inputs[0]
        return rvalue / len(inputs_)



