from GIS.graphics import *
import math


class View():
    def __init__(self, configuration, model):
        self.window = GraphWin('Symulator', 700, 700)

        # sets origin and converts x and y coords to go as in algebra
        self.window.setCoords(0, 0, 1000, 1000)

        # List of airport objects
        self.airport_list = list(configuration.airports.values())

        # List of connection objects
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
            beginning = Point(connection.beginning.coord_x, connection.beginning.coord_y)
            end = Point(connection.end.coord_x, connection.end.coord_y)

            # Calculating line position to only touch edges of the airport
            # Vector from beginning to end
            vector_x = end.x - beginning.x
            vector_y = end.y - beginning.y

            # Length of vector
            magnitude = math.sqrt(math.pow(vector_x, 2) + math.pow(vector_y, 2))

            # Making a unit vector
            unit_vector_x = vector_x / magnitude
            unit_vector_y = vector_y / magnitude

            # Moving beginning and end of lines a set amount of units in a given direction
            beginning.x += unit_vector_x * 15
            beginning.y += unit_vector_y * 15
            end.x -= unit_vector_x * 15
            end.y -= unit_vector_y * 15
            self.connections_to_draw.append(Line(beginning, end))

        self.airplane_list = model.airplanes

        self.airplanes_to_draw = []
        for airplane in self.airplane_list:
            self.airplanes_to_draw.append(Circle(Point(airplane.origin.coord_x, airplane.origin.coord_y), 7))

        for connection_to_draw in self.connections_to_draw:
            connection_to_draw.setWidth(1)
            connection_to_draw.setArrow('last')
            connection_to_draw.draw(self.window)

        for airport_to_draw in self.airports_to_draw:
            airport_to_draw.setFill('red')
            airport_to_draw.draw(self.window)

        for label_to_draw in self.airport_labels:
            label_to_draw.draw(self.window)

        for airplane_to_draw in self.airplanes_to_draw:
            airplane_to_draw.setFill('blue')
            airplane_to_draw.draw(self.window)

