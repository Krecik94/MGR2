import time

from GIS.configuration import Configuration
from GIS.graphics import *
from GIS.view import View
from GIS.model import Model


def main():
    configuration = Configuration()
    for key, value in configuration.airports.items():

        for possible_destination in value.possible_destinations:
            print('{0} -> {1}'.format(value.name, possible_destination.name))

    model = Model()
    view = View(configuration, model)

    point = Point(10, 10)
    point.draw(view.window)
    for i in range(100):
        point.move(5, 0)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
