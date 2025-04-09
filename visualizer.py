import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation
from brain import Neuron
import random

# Инициализация нейросети
NUM_NEURONS = 10
neurons = [Neuron(i) for i in range(NUM_NEURONS)]

edges = []
for i in range(NUM_NEURONS):
    targets = random.sample(range(NUM_NEURONS), k=random.randint(2, 4))
    for j in targets:
        if i != j:
            neurons[i].connect(neurons[j])
            edges.append((i, j))

G = nx.DiGraph()
G.add_edges_from(edges)

pos = nx.spring_layout(G)

fig, ax = plt.subplots(figsize=(8, 6))

def draw_graph(frame):
    ax.clear()
    fired_nodes = []

    # Обновляем нейроны
    for neuron in neurons:
        if random.random() < 0.05:
            neuron.stimulate(0.2)
        if neuron.update():
            fired_nodes.append(neuron.id)

    node_colors = []
    for neuron in neurons:
        if neuron.id in fired_nodes:
            node_colors.append('red')
        else:
            blue = max(0.0, min(1.0, neuron.charge))
            node_colors.append((0.2, 0.2, 1.0 * blue + 0.1))

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', arrows=True, arrowstyle='->', width=1.0)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=600)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color='white')

    ax.set_title("Симуляция нейронной сети")
    ax.axis('off')

ani = animation.FuncAnimation(fig, draw_graph, interval=400)
plt.show()
