import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre de simulation
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation d'une Mare")

# Couleurs
BLUE = (0, 100, 200)
GREEN = (34, 139, 34)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)

# Classe de base pour les plantes (Algues)
class Algae:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5

    def grow(self):
        self.size += 0.1  # Croissance basique des algues

    def draw(self, window):
        pygame.draw.circle(window, GREEN, (int(self.x), int(self.y)), int(self.size))

# Classe de base pour un Herbivore (Grenouille)
class Frog:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.energy = 100

    def move(self):
        # Mouvement aléatoire pour représenter le déplacement de la grenouille
        self.x += random.choice([-1, 1])
        self.y += random.choice([-1, 1])
        self.energy -= 1  # Consommation d'énergie

    def eat(self, algae):
        # Manger les algues proches pour regagner de l'énergie
        if abs(self.x - algae.x) < 10 and abs(self.y - algae.y) < 10:
            self.energy += 20
            algae.size = 0  # Algues mangées

    def draw(self, window):
        pygame.draw.circle(window, YELLOW, (int(self.x), int(self.y)), self.size)

# Classe de base pour un Carnivore (Poisson carnivore)
class CarnivorousFish:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 15
        self.energy = 200

    def hunt(self, prey):
        # Déplacement vers la proie
        if prey:
            if self.x < prey.x:
                self.x += 1
            elif self.x > prey.x:
                self.x -= 1
            if self.y < prey.y:
                self.y += 1
            elif self.y > prey.y:
                self.y -= 1
            self.energy -= 1  # Consommation d'énergie

            # Si proche de la proie, consomme l'énergie de la proie
            if abs(self.x - prey.x) < 10 and abs(self.y - prey.y) < 10:
                self.energy += 50
                prey.size = 0  # Proie mangée

    def draw(self, window):
        pygame.draw.circle(window, RED, (int(self.x), int(self.y)), self.size)

# Fonction principale
def main():
    clock = pygame.time.Clock()
    algae_list = [Algae(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(10)]
    frogs = [Frog(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]
    carnivores = [CarnivorousFish(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(2)]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Remplir la fenêtre avec la couleur de l'eau
        window.fill(BLUE)

        # Mise à jour et affichage des algues
        for algae in algae_list:
            algae.grow()
            algae.draw(window)

        # Mise à jour et affichage des grenouilles
        for frog in frogs:
            frog.move()
            for algae in algae_list:
                frog.eat(algae)
            frog.draw(window)

        # Mise à jour et affichage des carnivores
        for carnivore in carnivores:
            target = random.choice(frogs) if frogs else None
            carnivore.hunt(target)
            carnivore.draw(window)

        pygame.display.flip()
        clock.tick(30)  # Limite de 30 FPS pour la simulation

    pygame.quit()

if __name__ == "__main__":
    main()
