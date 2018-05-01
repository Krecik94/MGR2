import time

from GIS.configuration import Configuration
from GIS.graphics import *
from GIS.view import View
from GIS.model import Model


def main():
    configuration = Configuration()
    for key, value in configuration.airports.items():
        for outgoing_connection in value.outgoing_connections:
            print('{0} -> {1}'.format(value.name, outgoing_connection.end.name))

    configuration = Configuration()
    model = Model(configuration)
    view = View(configuration, model)

    for i in range(100000):
        model.step(configuration)
        view.update(model)
        time.sleep(0.01)



if __name__ == '__main__':
    main()
