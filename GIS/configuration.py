from enum import Enum
class Configuration:
    def __init__(self):
        self.number_of_airplanes = 3
        self.airports = {'A': Airport(name='A', country='1', coord_x=10, coord_y=10),
                         'B': Airport(name='B', country='1', coord_x=100, coord_y=100),
                         'C': Airport(name='C', country='2', coord_x=100, coord_y=200),
                         'D': Airport(name='D', country='3', coord_x=200, coord_y=300),
                         'E': Airport(name='E', country='3', coord_x=200, coord_y=400),
                         'F': Airport(name='F', country='4', coord_x=300, coord_y=100),
                         'G': Airport(name='G', country='5', coord_x=300, coord_y=200),
                         }

        self.connections = [Connection(beginning=self.airports['A'], end=self.airports['B'], distance=1),
                            Connection(beginning=self.airports['A'], end=self.airports['F'], distance=2),
                            Connection(beginning=self.airports['A'], end=self.airports['D'], distance=4),
                            Connection(beginning=self.airports['B'], end=self.airports['C'], distance=3),
                            Connection(beginning=self.airports['C'], end=self.airports['E'], distance=2),
                            Connection(beginning=self.airports['E'], end=self.airports['G'], distance=1),
                            Connection(beginning=self.airports['G'], end=self.airports['F'], distance=2),
                            Connection(beginning=self.airports['F'], end=self.airports['G'], distance=2)]

        for connection in self.connections:
            self.airports[connection.beginning.name].possible_destinations.append(connection.end)


class AirplaneState(Enum):
    STATIONARY = 1
    IN_FLIGHT = 2


class Airplane:
    def __init__(self, origin=None, destination=None, state=AirplaneState.STATIONARY, distance_traveled=0):
        # Where it's flying from
        self.origin = origin

        # Where it's flying to
        self.destination = destination

        # If it's flying or not
        self.state = state

        # How far has it already traveled
        self.distance_traveled = distance_traveled


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
            self.possible_destinations = possible_destinations
        else:
            self.possible_destinations = []


class Connection:
    def __init__(self, beginning, end, distance):
        # Order of those 2 objects matters, connection has a direction
        self.beginning = beginning
        self.end = end

        # Each connection has it's own length, it can contradict distance calculated from 2 airport coordinates
        self.distance = distance

        # Check if any plane is currently on a given connection
        self.is_occupied = False

