import random
from HeuristicRouter import HeuristicRouter, Location, Route
from openrouteservice import client

api_key = '58d904a497c67e00015b45fc1f9700c9ad4d40e1b7e22af323c7dbbe'
start = {'latitude': 52.05, 'longitude': 20.5}
end = {'latitude': 52.4, 'longitude': 21.3}

def main():
    clnt = client.Client(key=api_key)
    router = HeuristicRouter(max_distance=80)


    router.add_location(Location(latitude=start['latitude'],
                                 longitude=start['longitude']))
    for i in range(200):
        router.add_location(Location(latitude=random.randrange(5211, 5231) / 100,
                                     longitude=random.randrange(2084, 2125) / 100))

    router.add_location(Location(latitude=end['latitude'],
                                 longitude=end['longitude']))

    params_route = {'profile': 'driving-car', 'format_out': 'json', 'units': 'km', 'geometry': 'false',
                    'geometry_format': 'geojson', 'instructions': 'false',
                    'coordinates': [[start['longitude'], start['latitude']],
                                   [end['longitude'], end['latitude']]
                                   ]}

    route = clnt.directions(**params_route)
    print(route)


    iterations = router.calculate_routes_for_given_time()
    print('Number of iterations: {iterations}'.format(iterations=iterations))
    print(router.export_route_to_link(-1))


if __name__ == '__main__':
    main()
