from GIS.configuration import *
import random






class Model():
    def __init__(self):
        configuration = Configuration()
        self.airplanes = []

        for i in range(configuration.number_of_airplanes):
            self.airplanes.append(Airplane(origin=random.choice(list(configuration.airports.values())),
                                           destination=None,
                                           state=AirplaneState.STATIONARY,
                                           distance_traveled=0))

    def step(self):
        print('TODO')