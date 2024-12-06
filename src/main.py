from models import Mare
from controllers import SimulationController
from ui import UserInterface

def main():
    mare = Mare()
    simulation_controller = SimulationController(mare)
    ui = UserInterface(simulation_controller)

    # Start the UI's main loop
    ui.run()

if __name__ == "__main__":
    main()