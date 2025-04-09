import random

class Neuron:
    def __init__(self, id, threshold=1.0):
        self.id = id
        self.charge = 0.0
        self.threshold = threshold
        self.outgoing = []

    def connect(self, other):
        self.outgoing.append(other)

    def stimulate(self, amount):
        self.charge += amount

    def update(self):
        fired = False
        if self.charge >= self.threshold:
            self.charge = 0.0
            fired = True
            for neuron in self.outgoing:
                neuron.stimulate(0.3 + random.random() * 0.4)
        return fired
