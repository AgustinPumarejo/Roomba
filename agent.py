from mesa import Agent

class Roomba(Agent):
    """
    Agente que limpia la celda en la que se encuentra,
    si ya está libre se mueva a una celda libre aleatoria vecina
    Atributos:
        id: Identificador único del agente
        dirección: dirección a la que se moverá el agente
    """
    def __init__(self, unique_id, model):
        """
        Crea una Roomba nueva
        Args:
            id: identificador
            model: modelo en el que se encuentra el agente
            condition: estado que sirve para hacer que el roomba se detenga al limpiar
            moves: Número de movimiento, se utiliza para calcular estadísticas al final
        La dirección por default es 4, la cual corresponde a su posición actual
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.condition = "running"
        self.moves = 0

    """
    Función para obtener fácilmente los agentes que se encuentran en una celda
    """
    def get_state(self, pos):
        objects = self.model.grid.get_cell_list_contents(pos)
        for obj in objects:
            if isinstance(obj, Roomba) or isinstance(obj, ObstacleAgent):
                return "busy"
            elif isinstance(obj, Dirt):
                return "dirty"
        return "free"

    def move(self):
        """ 
        Limpia el piso de ser necesario, se mueve a una celda adyacente aleatoria de no serlo
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, 
            include_center=True) 

        spaces = list(map(self.get_state, possible_steps))

        if spaces[self.direction] != "busy":
            if spaces[self.direction] == "dirty":
                self.condition = "cleaning"
                self.model.dirtyCells -= 1
            self.model.grid.move_agent(self, possible_steps[self.direction])
            self.moves += 1
            #print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        else:
            #print(f"No se puede mover de {self.pos} en esa direccion.")
            pass

    def step(self):
        """ 
        Determina hacia donde se va a mover el Roomba
        """
        if self.condition == "cleaning":
            self.direction = 4
            self.condition = "running"
        else:
            self.direction = self.random.randint(0, 8)
        #print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()

class Dirt(Agent):
    """
    Mugre, solo tiene posición y es eliminada al limpiarse
    """
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos

    def step(self):
        pass

class ObstacleAgent(Agent):
    """
    Obstáculo que evita que los roomba elijan direcciónes que no son posibles en el grid
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass