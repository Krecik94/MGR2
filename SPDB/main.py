import random
from HeuristicRouter import HeuristicRouter, Location, Route

def main():
    router = HeuristicRouter(max_distance=80)

    router.add_location(Location(latitude=52.05,
                                 longitude=20.5))
    for i in range(200):
        router.add_location(Location(latitude=random.randrange(5211, 5231) / 100,
                                     longitude=random.randrange(2084, 2125) / 100))

    router.add_location(Location(latitude=52.4,
                                 longitude=21.3))


    iterations = router.calculate_routes_for_given_time()
    print('Number of iterations: {iterations}'.format(iterations=iterations))
    print(router.export_route_to_link(-1))


if __name__ == '__main__':
    main()
