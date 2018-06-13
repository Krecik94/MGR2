import random
import folium
import re
from HeuristicRouter import HeuristicRouter, Location, Route
from openrouteservice import client, exceptions
import datetime

api_key = '58d904a497c67e00015b45fc1f9700c9ad4d40e1b7e22af323c7dbbe'
start = {'latitude': 48.864716, 'longitude': 2.349014}
end = {'latitude': 53.893009, 'longitude': 27.567444}


def main():
    clnt = client.Client(key=api_key)
    router = HeuristicRouter(max_distance=3300)
    map1 = folium.Map(location=([start['latitude'], start['longitude']]))

    orig_route = {'profile': 'driving-car', 'format_out': 'geojson', 'units': 'km', 'geometry': 'true',
                  'geometry_format': 'geojson', 'instructions': 'false',
                  'coordinates': [[start['longitude'], start['latitude']],
                                  [end['longitude'], end['latitude']]
                                  ]}

    new_route = {'profile': 'driving-hgv', 'format_out': 'geojson', 'units': 'km', 'geometry': 'true',
                 'geometry_format': 'geojson', 'instructions': 'false',
                 'coordinates': []}

    router.add_location(Location(latitude=start['latitude'],
                                 longitude=start['longitude']))
    # Germany
    for i in range(33):
        router.add_location(Location(latitude=random.uniform(49.83424184, 52.78596815),
                                     longitude=random.uniform(6.40212352, 12.66433055)))

    for i in range(33):
        router.add_location(Location(latitude=random.uniform(50.44856501, 53.33233019),
                                     longitude=random.uniform(19.75875194, 26.57576854)))

    for i in range(33):
        router.add_location(Location(latitude=random.uniform(47.94558119, 51.5427282),
                                     longitude=random.uniform(14.94399364, 22.60146434)))

    router.add_location(Location(latitude=end['latitude'],
                                 longitude=end['longitude']))

    iterations = router.calculate_routes_for_given_time(datetime.timedelta(seconds=30))

    print('Number of iterations: {iterations}'.format(iterations=iterations))
    print(router.export_route_to_link(-1))
    print(len(router.get_route(-1).intermediate_points))

    best_route = router.get_route(-1)
    new_route['coordinates'].append([best_route.start.x, best_route.start.y])
    folium.Marker([best_route.start.y, best_route.start.x], icon=folium.Icon(color='green')).add_to(map1)
    for loc in best_route.intermediate_points:
        new_route['coordinates'].append([loc.x, loc.y])
        folium.Marker([loc.y, loc.x]).add_to(map1)
    new_route['coordinates'].append([best_route.end.x, best_route.end.y])
    folium.Marker([best_route.end.y, best_route.end.x], icon=folium.Icon(color='red')).add_to(map1)

    for loc in router.locations:
        if ((loc.x != start['longitude'] and loc.y != start['latitude'])
                and
                (loc.x != end['longitude'] and loc.y != end['latitude'])):
            folium.Marker([loc.y, loc.x]).add_to(map1)

    route_chunked = list(chunks(new_route['coordinates'], 49))
    mutual_point = []
    distance = 0
    duration = 0
    float_rgx = re.compile('[+-]?[0-9]*\.[0-9]+')
    for chunk in route_chunked:
        new_route['coordinates'] = chunk
        if len(mutual_point) != 0:
            new_route['coordinates'].insert(0, mutual_point)
        route = None
        while route is None:
            try:
                route = clnt.directions(**new_route)
            except exceptions.ApiError as err:
                found = float_rgx.findall(err.args[1]['error']['message'])
                #new_route['coordinates'].pop(new_route['coordinates'].index([float(found[1]),float(found[0])]))
                for coord in new_route['coordinates']:
                    if float(found[1]) == round(coord[0], 6):
                        if float(found[0]) == round(coord[1], 6):
                            new_route['coordinates'].remove(coord)
                            break;
                pass
        folium.features.GeoJson(route).add_to(map1)
        distance = distance + route['features'][0]['properties']['summary'][0]['distance']
        duration = duration + route['features'][0]['properties']['summary'][0]['duration']
        mutual_point = new_route['coordinates'].pop()

    # route = clnt.directions(**orig_route)
    # folium.features.GeoJson(route).add_to(map1)

    map1.save('map.html')
    print("Distance: %s" %distance)
    print("duration: %s" %str(datetime.timedelta(seconds=duration)))


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == '__main__':
    main()
