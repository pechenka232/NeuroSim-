class Neuron:
    def __init__(self, id, threshold=3):
        self.id = id
        self.threshold = threshold
        self.charge = 0
        self.connections = []

    def connect(self, neuron):
        self.connections.append(neuron)

    def receive_signal(self):
        self.charge += 1
        if self.charge >= self.threshold:
            self.fire()

    def fire(self):
        self.charge = 0
        for neuron in self.connections:
            neuron.receive_signal()
