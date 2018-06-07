import random
from HeuristicRouter import HeuristicRouter, Location, Route
from openrouteservice import client
import datetime

api_key = '58d904a497c67e00015b45fc1f9700c9ad4d40e1b7e22af323c7dbbe'
start = {'latitude': 48.864716, 'longitude': 2.349014}
end = {'latitude': 53.893009, 'longitude': 27.567444}


def main():
    clnt = client.Client(key=api_key)
    router = HeuristicRouter(max_distance=4000)

    router.add_location(Location(latitude=start['latitude'],
                                 longitude=start['longitude']))
    # Germany
    for i in range(666):
        router.add_location(Location(latitude=random.uniform(49.8342418433, 52.7859681528),
                                     longitude=random.uniform(6.4021235239, 12.6643305552)))

    for i in range(666):
        router.add_location(Location(latitude=random.uniform(50.4485650153, 53.3323301908),
                                     longitude=random.uniform(19.7587519419, 26.5757685435)))

    for i in range(666):
        router.add_location(Location(latitude=random.uniform(47.9455811959, 51.542728235),
                                     longitude=random.uniform(14.9439936411, 22.6014643443)))

    router.add_location(Location(latitude=end['latitude'],
                                 longitude=end['longitude']))

    params_route = {'profile': 'driving-car', 'format_out': 'json', 'units': 'km', 'geometry': 'false',
                    'geometry_format': 'geojson', 'instructions': 'false',
                    'coordinates': [[start['longitude'], start['latitude']],
                                    [end['longitude'], end['latitude']]
                                    ]}

    route = clnt.directions(**params_route)
    print(route)

    iterations = router.calculate_routes_for_given_time(datetime.timedelta(seconds=20))
    print('Number of iterations: {iterations}'.format(iterations=iterations))
    print(router.export_route_to_link(-1))
    print(len(router.get_route(-1).intermediate_points))


if __name__ == '__main__':
    main()
