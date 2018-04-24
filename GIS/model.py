from enum import Enum


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
    def __init__(self, name, country, coord_x=0, coord_y=0, times_visited=0, neighbours =[]):

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

        # List of airports connectd to this one
        self.neighbours = neighbours

