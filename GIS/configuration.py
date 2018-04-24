from GIS.model import Airport, Connection


class Configuration:
    def __init__(self):
        self.airports = {'A': Airport(name='A', country='1', coord_x=0, coord_y=1),
                         'B': Airport(name='B', country='1', coord_x=1, coord_y=0),
                         'C': Airport(name='C', country='2', coord_x=1, coord_y=2),
                         'D': Airport(name='D', country='3', coord_x=2, coord_y=0),
                         'E': Airport(name='E', country='3', coord_x=2, coord_y=3),
                         'F': Airport(name='F', country='4', coord_x=3, coord_y=1),
                         'G': Airport(name='G', country='5', coord_x=3, coord_y=2),
                         }

        self.connections = [Connection(beginning=self.airports['A'], end=self.airports['B'], distance=1),
                            Connection(beginning=self.airports['A'], end=self.airports['C'], distance=2),
                            Connection(beginning=self.airports['A'], end=self.airports['D'], distance=4),
                            Connection(beginning=self.airports['B'], end=self.airports['C'], distance=3),
                            Connection(beginning=self.airports['C'], end=self.airports['E'], distance=2),
                            Connection(beginning=self.airports['E'], end=self.airports['G'], distance=1),
                            Connection(beginning=self.airports['G'], end=self.airports['F'], distance=2)]

        for connection in self.connections:
            self.airports[connection.beginning.name].possible_destinations.append(connection.end)
