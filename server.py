from model import RoombaSim, Dirt, Roomba, ObstacleAgent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

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

model_params = {"N":5, "width":20, "height":20, "density" : UserSettableParameter("slider", "cell Density", 0.1, 0.01, 0.4, 0.01)}

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(RoombaSim, [grid], "Roomba", model_params)

server.launch()