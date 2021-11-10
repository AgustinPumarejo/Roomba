from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from agent import Roomba, Dirt, ObstacleAgent
from mesa.datacollection import DataCollector

def get_dirt_percentage(model):
    result = round(((model.dirtyCells / model.initialDirt) * 100), 2)
    print(result)
    return result

def get_moves(agent):
    if isinstance(agent, Roomba):
        print(agent.unique_id," : ", agent.moves)
        return agent.moves
    else:
        return

class RoombaSim(Model):

    """ 
    Crea un modelo para que las roombas limpien el piso
    Args:
        N: Número de Roombas
        height, width: Tamaño del modelo
        density: Cantidad de celdas sucias
        maxIterations: Número máximo de pasos
        dirtyCells: Número de celdas sucias
    """
    def __init__(self, N, width, height, density, maxIterations):
        self.num_agents = N
        self.grid = Grid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 
        self.iterations = 0
        self.maxIterations = maxIterations
        self.dirtyCells = 0
        self.initialDirt = 0

        # Crea el borde con obstáculos
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
                    self.dirtyCells += 1
                    #print("Added dirt, now we have: ", self.dirtyCells)
        self.initialDirt = self.dirtyCells

        # Agrega Roombas
        for i in range(self.num_agents):
            a = Roomba(i+1000, self) 
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        # Recolecta datos acerca de la cantidad de celdas sucias en cada iteración
        self.datacollector = DataCollector(
            model_reporters = {"Dirty Cells": get_dirt_percentage},
            agent_reporters = {"Movements": get_moves}
        )

    def step(self):
        '''Avanza un paso'''
        self.datacollector.collect(self)
        self.schedule.step()
        self.iterations += 1
        if self.iterations >= self.maxIterations or self.dirtyCells <= 0:
            self.running = False