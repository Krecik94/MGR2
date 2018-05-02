import time

from GIS.configuration import Configuration
from GIS.graphics import *
from GIS.view import View
from GIS.model import Model


def main():
    configuration = Configuration()
    model = Model(configuration)
    view = View(configuration, model)

    while model.days <= configuration.simulation_length:
        for i in range (100):
            model.step(configuration)
        view.update(model)
        time.sleep(0.01)

    # Print statistics
    for airport in list(configuration.airports.values()):
        print('{name}: {times_visited}'.format(name=airport.name, times_visited=airport.times_visited))

    for connection in configuration.connections:
        print('{beginning} -> {end} : {times_used}'.format(beginning=connection.beginning.name,
                                                           end=connection.end.name,
                                                           times_used=connection.times_used))


if __name__ == '__main__':
    main()
