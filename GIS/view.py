from GIS.configuration import AirplaneState
from GIS.graphics import *
import math
import random


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
        # List of labels of times the airport has been visited
        self.airport_visited_labels = []

        for airport in self.airport_list:
            self.airports_to_draw.append(Circle(Point(airport.coord_x, airport.coord_y), 15))
            self.airport_labels.append(Text(Point(airport.coord_x, airport.coord_y), airport.name))
            self.airport_visited_labels.append(
                Text(Point(airport.coord_x + 20, airport.coord_y - 20), airport.times_visited))

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
            self.airplanes_to_draw.append(
                Circle(Point(airplane.last_landing.coord_x, airplane.last_landing.coord_y), 7))

        for connection_to_draw in self.connections_to_draw:
            connection_to_draw.setWidth(1)
            connection_to_draw.setArrow('last')
            connection_to_draw.draw(self.window)

        for i in range(len(self.airports_to_draw)):
            random.seed(self.airport_list[i].country)
            self.airports_to_draw[i].setFill(
                color_rgb(random.randrange(256), random.randrange(256), random.randrange(256)))
            self.airports_to_draw[i].draw(self.window)

        for i in range(len(self.airport_labels)):
            random.seed(self.airport_list[i].country)
            if (random.randrange(256) + random.randrange(256) + random.randrange(256)) / 3 <= 120:
                self.airport_labels[i].setFill('white')
            self.airport_labels[i].draw(self.window)

        for i in range(len(self.airport_visited_labels)):
            self.airport_visited_labels[i].draw(self.window)

        for airplane_to_draw in self.airplanes_to_draw:
            airplane_to_draw.setFill('blue')
            airplane_to_draw.draw(self.window)

    def update(self):
        # Update labels
        for i in range(len(self.airport_visited_labels)):
            self.airport_visited_labels[i].setText(self.airport_list[i].times_visited)

        # Update airplane positions
        for i in range(len(self.airplane_list)):
            current_x = self.airplanes_to_draw[i].getCenter().x
            current_y = self.airplanes_to_draw[i].getCenter().y

            if self.airplane_list[i].state == AirplaneState.STATIONARY:
                end_x = self.airplane_list[i].last_landing.coord_x
                end_y = self.airplane_list[i].last_landing.coord_y

                self.airplanes_to_draw[i].move(end_x - current_x, end_y - current_y)

            else:
                connection_vector_x = \
                    self.airplane_list[i].connection.end.coord_x - self.airplane_list[i].connection.beginning.coord_x
                connection_vector_y = \
                    self.airplane_list[i].connection.end.coord_y - self.airplane_list[i].connection.beginning.coord_y

                perctentage_traveled = self.airplane_list[i].distance_traveled / self.airplane_list[
                    i].connection.distance

                end_x = self.airplane_list[i].connection.beginning.coord_x + connection_vector_x * perctentage_traveled
                end_y = self.airplane_list[i].connection.beginning.coord_y + connection_vector_y * perctentage_traveled

                self.airplanes_to_draw[i].move(end_x - current_x, end_y - current_y)
