from enum import Enum


class Configuration:
    def __init__(self):
        self.number_of_airplanes = 14
        self.step = 50
        self.airports = {'A': Airport(name='A', country='1', coord_x=10, coord_y=10),
                         'B': Airport(name='B', country='1', coord_x=100, coord_y=100),
                         'C': Airport(name='C', country='2', coord_x=100, coord_y=200),
                         'D': Airport(name='D', country='3', coord_x=200, coord_y=300),
                         'E': Airport(name='E', country='3', coord_x=200, coord_y=400),
                         'F': Airport(name='F', country='4', coord_x=300, coord_y=100),
                         'G': Airport(name='G', country='5', coord_x=300, coord_y=200),
                         }

        self.connections = [Connection(beginning=self.airports['A'], end=self.airports['B'], distance=7000),
                            Connection(beginning=self.airports['B'], end=self.airports['A'], distance=4000),
                            Connection(beginning=self.airports['A'], end=self.airports['F'], distance=4000),
                            Connection(beginning=self.airports['A'], end=self.airports['D'], distance=5000),
                            Connection(beginning=self.airports['B'], end=self.airports['C'], distance=2000),
                            Connection(beginning=self.airports['C'], end=self.airports['E'], distance=2500),
                            Connection(beginning=self.airports['E'], end=self.airports['G'], distance=5000),
                            Connection(beginning=self.airports['G'], end=self.airports['F'], distance=6000),
                            Connection(beginning=self.airports['F'], end=self.airports['G'], distance=2500),
                            Connection(beginning=self.airports['G'], end=self.airports['B'], distance=3000),
                            Connection(beginning=self.airports['D'], end=self.airports['F'], distance=4000),
                            Connection(beginning=self.airports['F'], end=self.airports['D'], distance=3000),]

        for connection in self.connections:
            self.airports[connection.beginning.name].outgoing_connections.append(connection)


class AirplaneState(Enum):
    STATIONARY = 1
    IN_FLIGHT = 2


class Airplane:
    def __init__(self, last_landing=None, state=AirplaneState.STATIONARY, distance_traveled=0, connection=None):
        # Name of last landing location
        self.last_landing = last_landing

        # If it's flying or not
        self.state = state

        # How far has it already traveled
        self.distance_traveled = distance_traveled

        # Connection on which the plane is flying
        self.connection = connection


class Airport:
    def __init__(self, name, country, coord_x=0, coord_y=0, times_visited=0, possible_destinations=None):

        # Name of airport, also it's ID
        self.name = name

        # Country in which this airport is located
        self.country = country

        # One of coordinates used to visualize the aiport
        self.coord_x = coord_x

        # Other coordinate
        self.coord_y = coord_y

        # How many times this airport has been visited (one airplane landed and took off)
        self.times_visited = times_visited

        # List of airports connected to this one
        if possible_destinations is not None:
            self.outgoing_connections = possible_destinations
        else:
            self.outgoing_connections = []


class Connection:
    def __init__(self, beginning, end, distance):
        # Order of those 2 objects matters, connection has a direction
        self.beginning = beginning
        self.end = end

        # Each connection has it's own length, it can contradict distance calculated from 2 airport coordinates
        self.distance = distance

        # Check if any plane is currently on a given connection
        self.is_occupied = False
