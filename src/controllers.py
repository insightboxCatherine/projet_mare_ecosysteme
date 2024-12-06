from models import Plante, Fish, Heron

class SimulationController:
    def __init__(self, mare):
        self.mare = mare
        self.population_data = {'generation': [], 'plants': [], 'fish': [], 'herons': []}

    def apply_initial_conditions(self, num_plants=5, num_fish=3, num_herons=2):
        """Initialize the pond with the given number of plants, fish, and herons."""
        self.mare.plants.clear()
        self.mare.fishes.clear()
        self.mare.herons.clear()

        # Add plants
        for _ in range(num_plants):
            self.mare.add_plant(Plante())

        # Add fish
        for _ in range(num_fish):
            self.mare.add_fish(Fish())

        # Add herons
        for _ in range(num_herons):
            self.mare.add_heron(Heron())

    def log_population(self, generation):
        """Logs the current population data."""
        self.population_data['generation'].append(generation+1)
        self.population_data['plants'].append(len(self.mare.plants))
        self.population_data['fish'].append(len(self.mare.fishes))
        self.population_data['herons'].append(len(self.mare.herons))

    def simulate_generation(self, generations):
        """Simulate given number of generations."""
        self.mare.simulate_growth()
        self.log_population(generations)  # Log data for each generation