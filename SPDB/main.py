import random
from HeuristicRouter import HeuristicRouter, Location, Route

def main():
    router = HeuristicRouter()

    for i in range(10):
        router.add_location(Location(longitude=random.randrange(5211,5231)/100,
                                     latitude=random.randrange(2084,2125)/100))

    router.calculate_number_of_routes(1)
    print(router.export_route_to_link(0))


if __name__ == '__main__':
    main()

