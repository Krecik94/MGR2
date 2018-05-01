from GIS.configuration import *
import random


class Model():
    def __init__(self, configuration):

        self.airplanes = []

        for i in range(configuration.number_of_airplanes):
            self.airplanes.append(Airplane(last_landing=random.choice(list(configuration.airports.values())),
                                           state=AirplaneState.STATIONARY,
                                           distance_traveled=0))

    def step(self, configuration):
        # Adding distance to planes
        for airplane in self.airplanes:
            if airplane.state is AirplaneState.IN_FLIGHT:
                airplane.distance_traveled += configuration.step

        # Checking which airplanes landed
        for airplane in self.airplanes:
            if airplane.state == AirplaneState.IN_FLIGHT:
                if airplane.distance_traveled >= airplane.connection.distance:
                    airplane.last_landing = airplane.connection.end
                    airplane.country_history.append(airplane.connection.end.country)
                    airplane.connection.end.times_visited += 1
                    airplane.distance_traveled = 0
                    airplane.connection.is_occupied = False
                    airplane.state = AirplaneState.STATIONARY
                    airplane.connection = None

        # Check if planes can depart
        for airplane in self.airplanes:
            if airplane.state == AirplaneState.STATIONARY:
                possible_connections = []
                for connection in airplane.last_landing.outgoing_connections:
                    if connection.is_occupied is not True:
                        if len(airplane.country_history) < 3 \
                                or len(set(airplane.country_history[-3:])) > 1 \
                                or connection.end.country not in airplane.country_history[-3:]:
                            possible_connections.append(connection)

                if possible_connections:
                    airplane.connection = random.choice(possible_connections)
                    airplane.state = AirplaneState.IN_FLIGHT
                    airplane.connection.is_occupied = True
