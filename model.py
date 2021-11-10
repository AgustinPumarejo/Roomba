from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from agent import Roomba, Dirt, ObstacleAgent

class RoombaSim(Model):
    """ 
    Crea un modelo para que las roombas limpien el piso
    Args:
        N: Número de Roombas
        height, width: Tamaño del modelo
    """
    def __init__(self, N, width, height, density = 0.4):
        self.num_agents = N
        self.grid = Grid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Agrega el piso
        for (contents, x, y) in self.grid.coord_iter():
            # Ensucia el piso
            if not x in [0, width - 1] and not y in [0, height-1]:
                if self.random.random() < density:
                    newDirt = Dirt((x, y), self)
                    self.grid._place_agent((x, y), newDirt)
                    self.schedule.add(newDirt)

        # Agrega Roombas
        for i in range(self.num_agents):
            a = Roomba(i+1000, self) 
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

    def step(self):
        '''Avanza un paso'''
        self.schedule.step()