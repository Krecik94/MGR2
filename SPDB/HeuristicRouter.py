from math import sin, cos, sqrt, atan2, radians
from geopy import distance

class Route:
    def __init__(self, start, end, intermediate_points=[]):
        self.start = start
        self.end = end
        self.intermediate_points = intermediate_points


class Location:
    def __init__(self, longitude, latitude, xml_data=None, node_id=0):
        self.x = longitude
        self.y = latitude
        self.xml_data = xml_data
        self.node_id = node_id


def calculate_distance(input_longitide_1,
                       input_latitude_1,
                       input_longitide_2,
                       input_latitude_2):
    # approximate radius of earth in km
    # R = 6373.0
    #
    # longitude_1 = radians(input_longitide_1)
    # latitude_1 = radians(input_latitude_1)
    # longitude_2 = radians(input_longitide_2)
    # latitude_2 = radians(input_latitude_2)
    #
    # longitude_difference = longitude_2 - longitude_1
    # latitude_difference = latitude_2 - latitude_1
    #
    # a = sin(latitude_difference / 2) ** 2 + cos(input_latitude_1) * cos(input_latitude_2) * sin(longitude_difference / 2) ** 2
    # c = 2 * atan2(sqrt(a), sqrt(1 - a))
    #
    # return R * c
    return distance.distance((input_latitude_1,input_longitide_1),(input_latitude_2,input_longitide_2))


class HeuristicRouter:
    def __init__(self, initial_locations=[]):
        self.locations = initial_locations
        self.routes = []

    def add_location(self, location):
        self.locations.append(location)

    def _calculate_route(self):
        if len(self.locations) < 2:
            raise Exception('Not enough locations')
        else:
            self.routes.append(Route(start=self.locations[0],
                                     end=self.locations[-1],
                                     intermediate_points=[location for i, location in enumerate(self.locations) if
                                                          i not in [0, len(self.locations) - 1]]))

    def calculate_number_of_routes(self, number_of_routes):
        # Call calculate_route a number_of_routes, either sequentially or using threads
        for i in range(number_of_routes):
            self._calculate_route()

    def export_route_to_link(self, route_index):
        if route_index > len(self.routes):
            return 'Index out of bounds'
        else:
            print(calculate_distance(self.routes[route_index].start.x,
                                     self.routes[route_index].start.y,
                                     self.routes[route_index].end.x,
                                     self.routes[route_index].end.y))
            if len(self.routes[route_index].intermediate_points) == 0:
                return 'https://maps.openrouteservice.org/directions?n1={y_start}&n2={x_start}&n3=12&a={y_start},{x_start},{y_end},{x_end}&b=0&c=0&k1=en-US&k2=km'.format(
                    x_start=self.routes[route_index].start.x,
                    y_start=self.routes[route_index].start.y,
                    x_end=self.routes[route_index].end.x,
                    y_end=self.routes[route_index].end.y)
            else:
                return_string = ''
                return_string += 'https://maps.openrouteservice.org/directions?n1={y_start}&n2={x_start}&n3=12&a={y_start},{x_start}'.format(
                    x_start=self.routes[route_index].start.x,
                    y_start=self.routes[route_index].start.y)
                for point in self.routes[route_index].intermediate_points:
                    return_string += ',{y_point},{x_point}'.format(x_point=point.x,
                                                                   y_point=point.y)

                return_string += ',{x_end},{y_end}&b=0&c=0&k1=en-US&k2=km'.format(
                    x_end=self.routes[route_index].end.x,
                    y_end=self.routes[route_index].end.y)

                return return_string
