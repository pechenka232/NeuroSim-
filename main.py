import pygame
import random
import math

# Параметры экрана
WIDTH, HEIGHT = 800, 600
FPS = 60
NEURON_COUNT = 10
CONNECTIONS = 18

# Цвета
BG_COLOR = (10, 10, 20)
WHITE = (255, 255, 255)

# Класс нейрона
class Neuron:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.charge = 0.0
        self.radius = 20
        self.dragging = False
        self.impulses = 0

    def stimulate(self):
        self.charge = 1.0
        self.impulses += 1

    def update(self):
        self.charge = max(0.0, self.charge - 0.01)

    def draw(self, screen):
        # Переход цвета от синего к красному
        red = int(255 * self.charge)
        blue = int(255 * (1 - self.charge))
        color = (red, 0, blue)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

        # Обводка и номер
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        font = pygame.font.SysFont("Arial", 14)
        text = font.render(str(self.id), True, WHITE)
        screen.blit(text, (self.x - 6, self.y - 8))


# Класс соединения
class Connection:
    def __init__(self, a: Neuron, b: Neuron):
        self.a = a
        self.b = b

    def draw(self, screen):
        pygame.draw.line(screen, (100, 100, 100), (self.a.x, self.a.y), (self.b.x, self.b.y), 1)


# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🧠 Симуляция нейронной сети")
clock = pygame.time.Clock()

# Создание нейронов
neurons = [Neuron(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), i) for i in range(NEURON_COUNT)]

# Создание случайных соединений
connections = []
while len(connections) < CONNECTIONS:
    a, b = random.sample(neurons, 2)
    if not any((conn.a == a and conn.b == b) or (conn.a == b and conn.b == a) for conn in connections):
        connections.append(Connection(a, b))

# Главный цикл
running = True
selected = None
offset_x, offset_y = 0, 0

while running:
    screen.fill(BG_COLOR)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for neuron in neurons:
                dist = math.hypot(event.pos[0] - neuron.x, event.pos[1] - neuron.y)
                if dist <= neuron.radius:
                    if event.button == 1:
                        neuron.stimulate()
                        selected = neuron
                        offset_x = neuron.x - event.pos[0]
                        offset_y = neuron.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            selected = None

        elif event.type == pygame.MOUSEMOTION:
            if selected:
                selected.x = event.pos[0] + offset_x
                selected.y = event.pos[1] + offset_y

    # Обновление и отрисовка
    for conn in connections:
        conn.draw(screen)

    for neuron in neurons:
        neuron.update()
        neuron.draw(screen)

    # Вывод количества стимуляций
    font = pygame.font.SysFont("Arial", 16)
    text = font.render(f"Стимуляций: {sum(n.impulses for n in neurons)}", True, (200, 200, 200))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
