from GIS.graphics import *


class View():
    def __init__(self, configuration):
        self.window = GraphWin('Symulator', 700, 700)

        # sets origin and converts x and y coords to go as in algebra
        self.window.setCoords(0, 0, 1000, 1000)

        # List of airport objects
        self.airport_list = list(configuration.airports.values())

        # List of connecton objects
        self.connection_list = configuration.connections

        # List or Circle objects representing airports
        self.airports_to_draw = []
        # List of labels on airports
        self.airport_labels = []

        for airport in self.airport_list:
            self.airports_to_draw.append(Circle(Point(airport.coord_x, airport.coord_y), 15))
            self.airport_labels.append(Text(Point(airport.coord_x, airport.coord_y), airport.name))

        # List of Line objects representing connections
        self.connections_to_draw = []

        for connection in self.connection_list:
            self.connections_to_draw.append(
                Line(
                    Point(connection.beginning.coord_x, connection.beginning.coord_y),
                    Point(connection.end.coord_x, connection.end.coord_y)
                )
            )

        for connection_to_draw in self.connections_to_draw:
            connection_to_draw.setWidth(1)
            connection_to_draw.draw(self.window)

        for airport_to_draw in self.airports_to_draw:
            airport_to_draw.setFill('red')
            airport_to_draw.draw(self.window)

        for label_to_draw in self.airport_labels:
            label_to_draw.draw(self.window)
