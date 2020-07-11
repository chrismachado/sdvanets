

class DeciderManager(object):
    def __init__(self):
        pass

    def compare(self, deciders, hour=None):
        best = deciders[0]
        for decider in deciders[1:]:
            print("%s: %f < %s: %f" % (best.name, best.eval(hour=hour), decider.name, decider.eval(hour=hour)))
            if best.eval(hour=hour) < decider.eval(hour=hour):
                best = decider
        return best


from utils.filereader import read_inputs
from datasets import make_dataset
from roaddecider import Decider

samples1 = read_inputs('/home/wifi/PycharmProjects/data-extractor/data_extractor/service/examples', 'output.csv')
samples2 = read_inputs('/home/wifi/PycharmProjects/data-extractor/data_extractor/service/examples', 'output2.csv')

decider1 = Decider(inputs=samples1, name='rsu1')
decider2 = Decider(inputs=samples2, name='rsu2')

trainsamples, traintargets = make_dataset()
decider1.clf.fit(trainsamples, traintargets)
decider2.clf.fit(trainsamples, traintargets)

rtargets1 = decider1.verify_road()
rtargets2 = decider2.verify_road()

decider_manager = DeciderManager()
best = decider_manager.compare([decider1, decider2])
print('melhor caminho [geral] : %s' % best.name)
best_per_hour = decider_manager.compare([decider1, decider2], hour=16)
print('melhor caminho [horario, %d] : %s' % (16, best_per_hour.name))

print(decider1.eval(16))
print(decider2.eval(16))

print(rtargets1)
print(rtargets2)