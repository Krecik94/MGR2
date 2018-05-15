from configuration import *
import random


class Model():
    def __init__(self, configuration):

        self.airplanes = []
        self.days = 0
        self.hours = 0
        self.minutes = 0
        for i in range(configuration.number_of_airplanes):
            self.airplanes.append(Airplane(last_landing=random.choice(list(configuration.airports.values())),
                                           state=AirplaneState.STATIONARY,
                                           distance_traveled=0))

    def step(self, configuration):
        self.minutes += configuration.simulation_tempo * 60
        changed = True
        while changed:
            changed = False
            if self.minutes >= 60:
                changed = True
                self.minutes -= 60
                self.hours += 1
            if self.hours >= 24:
                changed = True
                self.hours -= 24
                self.days += 1
        # Adding distance to planes
        for airplane in self.airplanes:
            if airplane.state is AirplaneState.IN_FLIGHT:
                airplane.distance_traveled += configuration.plane_speed * configuration.simulation_tempo

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
                    # Sorting the list
                    possible_connections.sort(key=lambda x: x.end.times_visited)

                    # Extracting connections with least times visited
                    possible_connections = [x for x in possible_connections if
                                            x.end.times_visited == possible_connections[0].end.times_visited]

                    # Choosing a connections with least times visited at random
                    airplane.connection = random.choice(possible_connections)
                    airplane.connection.times_used +=1
                    airplane.state = AirplaneState.IN_FLIGHT
                    airplane.connection.is_occupied = True
