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
    airports_to_print = list(configuration.airports.values())
    airports_to_print.sort(key= lambda x: x.times_visited)
    for airport in airports_to_print:
        print('{name}: {times_visited}'.format(name=airport.name, times_visited=airport.times_visited))

    connections_to_print = configuration.connections
    connections_to_print.sort(key=lambda x: x.times_used)
    for connection in connections_to_print:
        print('{beginning} -> {end} : {times_used}'.format(beginning=connection.beginning.name,
                                                           end=connection.end.name,
                                                           times_used=connection.times_used))


if __name__ == '__main__':
    main()
