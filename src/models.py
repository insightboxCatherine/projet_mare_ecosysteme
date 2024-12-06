import random
from matplotlib.patches import Ellipse
from shapely.geometry import Polygon, Point

def random_coordinate():
    # Create surface of mare
        ellipse_mare = Ellipse((600, 500), 900, 400)
        vertices_mare = ellipse_mare.get_verts() # get the vertices from the ellipse object
        ellipse_mare = Polygon(vertices_mare)
        minx, miny, maxx, maxy = ellipse_mare.bounds
     # Create random points inside the bounds of the mare
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        while not ellipse_mare.contains(pnt):
            pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        x = pnt.x
        y = pnt.y
        return(x, y, minx, miny, maxx, maxy)
    
class Plante:
    def __init__(self):
        self.age = 0
        self.x, self.y, self.minx, self.miny, self.maxx, self.maxy = random_coordinate()
            

    def grow(self):
        self.age += 1

class Fish:
    def __init__(self):
        self.x, self.y, self.minx, self.miny, self.maxx, self.maxy = random_coordinate()
        self.age = 0

    def grow(self):
        self.age += 1

    def move(self):
        """Move the plant within the pond boundaries."""
        # Move by a small random step within the bounds
        self.x += random.randint(-2, 2)
        self.y += random.randint(-2, 2)

        # Check and adjust to keep within pond bounds
        self.x = max(self.minx, min(self.x, self.maxx))
        self.y = max(self.miny, min(self.y, self.maxy))
    
    def hunt(self, plant_list):
        """Attempt to eat fish if within close range."""
        compteur = 0
        for plant in plant_list:
            if abs(self.x - plant.x) < 50 and abs(self.y - plant.y) < 50:
                plant_list.remove(plant)  # "Eat" the fish
                compteur +=1
        if compteur == 0:
            return False, plant_list # Failed hunt
        else:
            return True, plant_list # Successful hunt

class Heron:
    def __init__(self):
        self.x, self.y, self.minx, self.miny, self.maxx, self.maxy = random_coordinate()
        self.age = 0
            
    def grow(self):
        self.age += 1

    def move(self):
        """Move the heron within the pond boundaries."""
        # Move by a small random step within the bounds
        self.x += random.randint(-3, 3)
        self.y += random.randint(-3, 3)

        # Check and adjust to keep within pond bounds
        self.x = max(self.minx, min(self.x, self.maxx))
        self.y = max(self.miny, min(self.y, self.maxy))

    def hunt(self, fish_list):
        """Attempt to eat fish if within close range."""
        compteur = 0
        for fish in fish_list:
            if abs(self.x - fish.x) < 70 and abs(self.y - fish.y) < 70:
                compteur +=1
                fish_list.remove(fish)  #"Eat" the fish
        if compteur == 0:
            return False, fish_list
        else:
            return True, fish_list  # Successful hunt

class Mare:
    def __init__(self):
        self.plants = []
        self.fishes = []
        self.herons = []

    def add_plant(self, plant):
        self.plants.append(plant)

    def add_fish(self, fish):
        self.fishes.append(fish)

    def add_heron(self, heron):
        self.herons.append(heron)

    def simulate_growth(self):
        # Create lists to contain animals that didn't eat to kill them
        hungry_fishes = []
        hungry_herons = []

        # Plant Growth and Mortality
        for plant in self.plants:
            plant.grow()
        
        # Fish Movement, Eating, and Mortality
        for fish in self.fishes:
            fish.move()
            if len(self.plants) != 0:    
                manger, self.plants = fish.hunt(self.plants)  # Successful hunts improves survival, failed hunt means death
            else:
                manger = False    

            if manger is False :
                hungry_fishes.append(fish)
        for dead_fish in hungry_fishes:
            if dead_fish in self.fishes:
                self.fishes.remove(dead_fish)

        # Heron Movement, Hunting, and Conditional Reproduction
        for heron in self.herons:
            heron.move()
            if len(self.fishes) != 0:
                hunt, self.fishes = heron.hunt(self.fishes)
            else:
                hunt = False

            if hunt is False: # Failed hunt means death
                hungry_herons.append(heron)
        for dead_heron in hungry_herons:
            if dead_heron in self.herons:
                self.herons.remove(dead_heron)

        # Plant Growth Factor
        plant_growth_factor = 3
        if len(self.plants) < 1000 :
            new_plants_count = int(len(self.plants) * plant_growth_factor)
            for _ in range(new_plants_count):
                self.add_plant(Plante())

        # The fish that ate survived and will reproduce
        new_fish_count = int(len(self.fishes) * 4)
        for _ in range(new_fish_count):
            self.add_fish(Fish())    

        # Calculate heron reproduction based on successful hunts
        heron_reproduction_factor = 2

        # Add new herons based on adjusted reproduction factor
        new_herons_count = int(len(self.herons) * heron_reproduction_factor)
        for _ in range(new_herons_count):
            self.add_heron(Heron())

        # Mortality Rates
        # Normal mortality for plants
        old_plants = []
        plant_mortality_rate = 0.3
        plant_survivors_count = int(len(self.plants) * (1 - plant_mortality_rate))
        self.plants = random.sample(self.plants, plant_survivors_count)
        for plant in self.plants:
            if plant.age > 7:
                old_plants.append(plant)
        for old_plant in old_plants:
            if old_plant in self.plants:
                self.plants.remove(old_plant)

        # Adjust fish mortality rate based on population dynamics
        old_fishes = []
        fish_mortality_rate = 0.3 # Reduced to ensure sustainability
        for fish in self.fishes:
            if fish.age > 5:
                old_fishes.append(fish)
        for old_fish in old_fishes:
            if old_fish in self.fishes:
                self.fishes.remove(old_fish)
        
        fish_survivor_count = int(len(self.fishes) * (1 - fish_mortality_rate))
        self.fishes = random.sample(self.fishes, fish_survivor_count)

        # Adjust heron mortality rate based on population dynamics
        old_herons = []
        heron_mortality_rate = 0.05  # Reduced to ensure sustainability
        for heron in self.herons:
            if heron.age > 20:
                old_herons.append(heron)
        for old_heron in old_herons:
            if old_heron in old_herons:
                self.herons.remove(old_heron)

        heron_survivor_count = int(len(self.herons) * (1 - heron_mortality_rate))
        self.herons = random.sample(self.herons, heron_survivor_count)