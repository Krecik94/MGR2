from math import sin, cos, sqrt, atan2, radians, degrees
from geopy import distance
import copy


class Route:
    def __init__(self, start, end, intermediate_points=None):
        self.start = start
        self.end = end
        if intermediate_points is not None:
            self.intermediate_points = intermediate_points
        else:
            self.intermediate_points = []


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
    return distance.distance((input_latitude_1, input_longitide_1), (input_latitude_2, input_longitide_2)).km


def calculate_bearing_difference(b1, b2):
    angle = abs(b2 - b1)
    angle = min(360 - angle, angle)
    return angle


def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[0])
    lat2 = radians(pointB[0])

    diffLong = radians(pointB[1] - pointA[1])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
                                 * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)

    return initial_bearing


class HeuristicRouter:
    def __init__(self, initial_locations=None):
        if initial_locations is not None:
            self.locations = initial_locations
        else:
            self.locations = []
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

            # TODO: ROUTE CALCULATOR GOES HERE
            locations = copy.deepcopy(self.locations)

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
            bearing_1 = calculate_initial_compass_bearing(
                (self.routes[route_index].start.y, self.routes[route_index].start.x),
                (self.routes[route_index].end.y, self.routes[route_index].end.x))
            print(bearing_1)
            bearing_2 = calculate_initial_compass_bearing(
                (self.routes[route_index].start.y, self.routes[route_index].start.x),
                (self.routes[route_index].intermediate_points[0].y,
                 self.routes[route_index].intermediate_points[0].x))
            print(bearing_2)
            print(calculate_bearing_difference(bearing_1,bearing_2))
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

                return_string += ',{y_end},{x_end}&b=0&c=0&k1=en-US&k2=km'.format(
                    x_end=self.routes[route_index].end.x,
                    y_end=self.routes[route_index].end.y)

                return return_string
