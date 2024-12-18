import pygame
import pygame_gui
import pygame.mixer
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from models import random_coordinate, Plante, Fish, Heron

class UserInterface:
    def __init__(self, simulation_controller):
        self.simulation_controller = simulation_controller
        self.running = True
        self.simulation_running = False
        self.showing_graph = False  # New flag for graph display
        self.showing_help = False # New flag for help display

        # Placeholder entities for initial display
        self.placeholder_plants = [Plante() for _ in range(5)]
        self.placeholder_fish = [Fish() for _ in range(3)]
        self.placeholder_herons = [Heron() for _ in range(2)]

        pygame.init()
        self.screen = pygame.display.set_mode((1500, 800))
        pygame.display.set_caption("Dynamic Pond Simulation")
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((1500, 900))
        self.font = pygame.font.Font(None, 24)

        # Initialize pygame mixer for music
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/marsh.ogg")  # Adjust file path if needed
        pygame.mixer.music.set_volume(0.5)  # Set volume from 0.0 to 1.0

        # Load background, plant, fish, and heron images
        self.background_image = pygame.image.load("assets/images/pond_background.png").convert()
        self.plant_image = pygame.image.load("assets/images/algae.png").convert_alpha()
        self.plant_image = pygame.transform.scale(self.plant_image, (30, 30))
        self.fish_image = pygame.image.load("assets/images/fish02.png").convert_alpha()
        self.fish_image = pygame.transform.scale(self.fish_image, (50, 50))
        self.heron_image = pygame.image.load("assets/images/heron.png").convert_alpha()
        self.heron_image = pygame.transform.scale(self.heron_image, (120, 120))

        # Start button
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (100, 40)),  # Positioned at the top-left
            text='Start',
            manager=self.manager
        )

        # "Show Graph" button
        self.graph_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((140, 20), (120, 40)),  # Right of "Start"
            text='Show Graph',
            manager=self.manager
        )

        # "Help" button
        self.help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((280, 20), (100, 40)),  # Positionné à droite de "Show Graph"
            text='Help',
            manager=self.manager
        )

        # Toggle Music Button
        self.music_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((400, 20), (120, 40)),
            text="Toggle Music",
            manager=self.manager
        )
        self.music_playing = True
    
        # Sliders for Plants, Fish, Herons, and Years
        self.plant_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((20, 80), (200, 40)),
            start_value=20,  # Default plants
            value_range=(20, 100),
            manager=self.manager
        )

        self.fish_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((250, 80), (200, 40)),
            start_value=10,  # Default fish
            value_range=(10, 50),
            manager=self.manager
        )

        self.heron_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((480, 80), (200, 40)),
            start_value=3,  # Default herons
            value_range=(3, 20),
            manager=self.manager
        )

        self.year_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((710, 80), (200, 40)),  # Spaced right of Heron slider
            start_value=10,
            value_range=(1, 50),
            manager=self.manager
        )

        # Labels for sliders
        self.plant_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 120), (200, 30)),  # Below Plant slider
            text='Plants: 20',
            manager=self.manager
        )
        self.fish_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 120), (200, 30)),  # Below Fish slider
            text='Fish: 10',
            manager=self.manager
        )
        self.heron_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((480, 120), (200, 30)),  # Below Heron slider
            text='Herons: 3',
            manager=self.manager
        )
        self.year_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((710, 120), (200, 30)),  # Below Year slider
            text='Years: 10',
            manager=self.manager
        )

        # Results Panel
        self.results_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((1200, 0), (300, 800)),  # Right side
            manager=self.manager
        )
        self.results_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (280, 30)),
            text="Simulation Results",
            manager=self.manager,
            container=self.results_panel
        )
        self.results_plants = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 50), (280, 30)),
            text="Plants: 0",
            manager=self.manager,
            container=self.results_panel
        )
        self.results_fish = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 90), (280, 30)),
            text="Fish: 0",
            manager=self.manager,
            container=self.results_panel
        )
        self.results_herons = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 130), (280, 30)),
            text="Herons: 0",
            manager=self.manager,
            container=self.results_panel
        )
        self.results_years = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 170), (280, 30)),
            text="Year: 0",
            manager=self.manager,
            container=self.results_panel
        )

    def toggle_music(self, play=True):
        """Plays or stops the background music."""
        if play:
            pygame.mixer.music.play(-1)  # Infinite loop
        else:
            pygame.mixer.music.stop()    

    def update_results_panel(self, gen):
        """Update the results panel with current simulation data."""
        if self.simulation_running:
            plants = len(self.simulation_controller.mare.plants)
            fish = len(self.simulation_controller.mare.fishes)
            herons = len(self.simulation_controller.mare.herons)
            years = gen +1

            self.results_plants.set_text(f"Plants: {plants}")
            self.results_fish.set_text(f"Fish: {fish}")
            self.results_herons.set_text(f"Herons: {herons}")
            self.results_years.set_text(f"Year: {years}")
        
    def plot_population_dynamics(self, data):
        
        """Generate and save the population dynamics graph as a surface."""
        if not data['generation']:
            return None  # Avoid plotting empty data

        plt.figure(figsize=(10, 6))
        generations = data['generation']

        # Plot each population type
        plt.plot(generations, data['plants'], 'g--', label='Plants', linewidth=2)
        plt.plot(generations, data['fish'], 'b-', label='Prey', linewidth=2)
        plt.plot(generations, data['herons'], 'brown', label='Predator', linewidth=2)

        # Axis labeling
        plt.title("Population Dynamics")
        plt.xlabel("Generation")
        plt.ylabel("Population")
        plt.legend(loc='upper right')

        # Save the plot to an in-memory buffer
        buffer = BytesIO()
        plt.savefig(buffer, format="PNG")
        buffer.seek(0)
        plt.close()

        # Convert buffer to a pygame surface
        image = Image.open(buffer)
        graph_surface = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        buffer.close()

        return graph_surface

    def get_user_inputs(self):
        time_delta = self.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.showing_graph and event.key == pygame.K_ESCAPE:  # Close the graph display
                    self.showing_graph = False
                elif self.showing_help and event.key == pygame.K_ESCAPE:  # Close the help display
                    self.showing_help = False
            
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        # Clear placeholders and population data
                        self.placeholder_plants = []
                        self.placeholder_fish = []
                        self.placeholder_herons = []
                        self.simulation_controller.population_data = {
                            'generation': [], 'plants': [], 'fish': [], 'herons': []
                        }

                        self.simulation_running = True

                        # Get slider values and apply initial conditions
                        num_plants = int(self.plant_slider.get_current_value())
                        num_fish = int(self.fish_slider.get_current_value())
                        num_herons = int(self.heron_slider.get_current_value())
                        years = int(self.year_slider.get_current_value())

                        self.simulation_controller.apply_initial_conditions(num_plants, num_fish, num_herons)
                        
                        # Simulate year by year
                        for gen in range(years):
                            self.simulation_controller.simulate_generation(gen)
                            self.update_results_panel(gen)
                            self.display_interface()
                            
                            for sub_event in pygame.event.get():
                                if sub_event.type == pygame.QUIT:
                                    self.running = False
                                    return
                            
                            self.manager.update(0.01)
                            pygame.time.wait(750)

                        self.simulation_running = False  # Stop simulation after running all years

                    elif event.ui_element == self.graph_button:
                        if self.simulation_controller.population_data['generation']:
                            self.graph_surface = self.plot_population_dynamics(self.simulation_controller.population_data)
                            self.showing_graph = True

                    elif event.ui_element == self.help_button:
                        self.showing_help = True

                    elif event.ui_element == self.music_button:
                        #Toggle music on/off
                        self.music_playing = not self.music_playing
                        self.toggle_music(play=self.music_playing)

                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    # Update slider labels dynamically
                    if event.ui_element == self.plant_slider:
                        self.plant_label.set_text(f"Plants: {int(self.plant_slider.get_current_value())}")
                    elif event.ui_element == self.fish_slider:
                        self.fish_label.set_text(f"Fish: {int(self.fish_slider.get_current_value())}")
                    elif event.ui_element == self.heron_slider:
                        self.heron_label.set_text(f"Herons: {int(self.heron_slider.get_current_value())}")
                    elif event.ui_element == self.year_slider:
                        self.year_label.set_text(f"Years: {int(self.year_slider.get_current_value())}")

            self.manager.process_events(event)
        self.manager.update(time_delta)

    def display_entities(self):
        """Render plants, fish, and herons on the screen."""
        if not self.simulation_running and self.placeholder_fish and self.placeholder_herons and self.placeholder_plants:  # Display placeholders
            for plant in self.placeholder_plants:
                self.screen.blit(self.plant_image, (int(plant.x), int(plant.y)))
            for fish in self.placeholder_fish:
                self.screen.blit(self.fish_image, (int(fish.x), int(fish.y)))
            for heron in self.placeholder_herons:
                self.screen.blit(self.heron_image, (int(heron.x), int(heron.y)))
        else:  # Display actual simulation entities
            for plant in self.simulation_controller.mare.plants:
                self.screen.blit(self.plant_image, (int(plant.x), int(plant.y)))
            for fish in self.simulation_controller.mare.fishes:
                self.screen.blit(self.fish_image, (int(fish.x), int(fish.y)))
            for heron in self.simulation_controller.mare.herons:
                self.screen.blit(self.heron_image, (int(heron.x), int(heron.y)))  
             
    def display_interface(self):
        """Render the interface, including sliders and entities."""
        if self.showing_graph:
            # Display graph surface
            self.screen.blit(self.graph_surface, (0, 0))
        elif self.showing_help:
            # Display help message
            self.screen.blit(self.plot_help(), (0, 0))
        else:
            # Display simulation
            self.screen.blit(self.background_image, (0, 0))
            self.display_entities()
            
            self.manager.draw_ui(self.screen)
            
        pygame.display.flip()

    def plot_help(self):
    
        # Load the image using PIL
        img = Image.open('assets/images/userGuide.png')
        
        # Display the image using Matplotlib
        fig, ax = plt.subplots(figsize=(8,7))
        ax.text(0,0,"Press ESC to close the User Guide", fontsize=8, fontweight="bold")
        ax.imshow(img)
        ax.axis('off')  # Hide axes
        
        # Save the Matplotlib figure to an in-memory buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='PNG')
        buffer.seek(0)
        plt.close()
        
        # Load the image from the buffer using PIL
        image = Image.open(buffer)
        
        # Convert the PIL image to a format suitable for Pygame
        mode = image.mode
        size = image.size
        data = image.tobytes()
        
        # Create a Pygame surface from the image data
        graph_surface = pygame.image.fromstring(data, size, mode)
        
        # Clean up the buffer
        buffer.close()
        
        return graph_surface

    def run(self):
        """Main loop for running the simulation."""
        if not pygame.mixer.music.get_busy():  # Vérifie si la musique joue déjà
            self.toggle_music(play=True)  # Démarre la musique de fond
        
        while self.running:
            self.get_user_inputs()
            if not self.showing_graph and not self.showing_help and self.simulation_running:
                self.simulation_controller.mare.simulate_growth()

            self.display_interface()
            self.clock.tick(30)

        pygame.mixer.music.stop()  # Arrête la musique à la fin
        pygame.quit()
