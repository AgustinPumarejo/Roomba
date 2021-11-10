from model import RoombaSim, Dirt, Roomba, ObstacleAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule

def agent_portrayal(agent):
    if agent is None: return
    
    if isinstance(agent, Roomba):
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "red",
                    "r": 1}

    if isinstance(agent, Dirt):
        portrayal = {
            "Shape": "rect",
            "h": 1,
            "w": 1,
            "Filled": "true",
            "Layer": 1
        }

        x, y = agent.pos

        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = "grey"

    if isinstance(agent, ObstacleAgent):
        x, y = agent.pos
        portrayal = {
            "Shape": "rect",
            "h": 1,
            "w": 1,
            "Filled": "true",
            "Layer": 1,
            "Color" : "black",
            "x": x,
            "y": y
        }
        

    return portrayal

"""
Parámetros iniciales del modelo, el ancho y alto no se lograron hacer deslizadores porque
se requiere de valores estáticos en el CanvasGrid
"""
model_params = {
    "N": UserSettableParameter("slider", "Number of Roombas", 5, 1, 20, 1), 
    "width": 15,
    "height": 15, 
    "density" : UserSettableParameter("slider", "Dirt Density", 0.4, 0.01, 1, 0.05),
    "maxIterations" : UserSettableParameter("slider", "Max Iterations", 100, 10, 1000, 10)
    }

# Condiciones del gráfico
chart = ChartModule([{"Label": "Dirty Cells",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, 15, 15, 500, 500)
server = ModularServer(RoombaSim, [grid, chart], "Roomba", model_params)

server.launch()