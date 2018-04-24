from GIS.configuration import Configuration


def main():
    configuration = Configuration()
    for key, value in configuration.airports.items():

        for possible_destination in value.possible_destinations:
            print('{0} -> {1}'.format(value.name, possible_destination.name))


if __name__ == '__main__':
    main()
