from math import sin, cos, sqrt, atan2, radians, degrees
from geopy import distance
import random
import datetime


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


class RoutingDatapoint(Location):
    def __init__(self, location, longitude, latitude, xml_data=None, node_id=0):
        super().__init__(longitude, latitude, xml_data, node_id)
        self.corresponding_location = location
        self.distances = {}

        self.current_distance = 0
        self.distance_weight = 0

        self.current_angle = 0
        self.bearing_weight = 0

        self.clump_score = 0
        self.clump_weight = 0

        self.random_value = 0

        self.total_weight = 0

    def recalculate_total_weight(self, distance_multiplier=1, bearing_multiplier=1, clump_multiplier=1,
                                 random_multiplier=1):
        self.total_weight = self.distance_weight * distance_multiplier + self.bearing_weight * bearing_multiplier + self.clump_weight * clump_multiplier + self.random_value * random_multiplier


def fast_distance_calculation(lat, lng, lat0, lng0):
    deglen = 110.25
    x = lat - lat0
    y = (lng - lng0) * cos(lat0)
    return deglen * sqrt(x * x + y * y)


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
    def __init__(self, initial_locations=None, max_distance=100):
        if initial_locations is not None:
            self.locations = initial_locations
        else:
            self.locations = []
        self.routes = []
        self.max_distance = max_distance
        self.only_distance_route = None
        self.only_bearing_route = None
        self.distance_map = {}
        self.bearing_map = {}

    def add_location(self, location):
        self.locations.append(location)

    def perform_initial_calculations(self):
        for location_1 in self.locations:
            for location_2 in self.locations:
                distance_to_add = fast_distance_calculation(location_1.y,
                                                            location_1.x,
                                                            location_2.y,
                                                            location_2.x)
                self.distance_map[(location_1, location_2)] = distance_to_add
                self.distance_map[(location_2, location_1)] = distance_to_add

                bearing_to_add = calculate_initial_compass_bearing((location_1.y, location_1.x),
                                                                   (location_2.y, location_2.x))

                self.bearing_map[(location_1, location_2)] = bearing_to_add
                self.bearing_map[(location_2, location_1)] = bearing_to_add

    def _calculate_route(self,
                         distance_multiplier=1,
                         bearing_multiplier=1,
                         clump_multiplier=1,
                         random_multiplier=1,
                         clump_number=4):
        if clump_number < 2:
            clump_number = 2

        if len(self.locations) < 2:
            raise Exception('Not enough locations')
        elif len(self.locations) == 2:
            self.routes.append(Route(start=self.locations[0],
                                     end=self.locations[-1]))
        else:
            # extracting every point except start and end
            intermediate_points = [location for i, location in enumerate(self.locations) if
                                   i not in [0, len(self.locations) - 1]]
            datapoints = []
            for point in intermediate_points:
                datapoints.append(RoutingDatapoint(location=point, longitude=point.x, latitude=point.y))

            for datapoint in datapoints:
                for distance_to in self.locations:
                    datapoint.distances[distance_to] = self.distance_map[
                        (datapoint.corresponding_location, distance_to)]
                    # datapoint.distances[distance_to] = fast_distance_calculation(datapoint.y,
                    #                                                              datapoint.x,
                    #                                                              distance_to.y,
                    #                                                              distance_to.x)

            # first loop, get distance from start
            for datapoint in datapoints:
                datapoint.current_distance = datapoint.distances[self.locations[0]]

            # first loop, bearing difference between start/end and start/point
            for datapoint in datapoints:
                datapoint.current_angle = calculate_bearing_difference(
                    self.bearing_map[(self.locations[0], self.locations[-1])],
                    self.bearing_map[(self.locations[0], datapoint.corresponding_location)])

            for datapoint in datapoints:
                sorted_distances = sorted(list(datapoint.distances.values()))
                NUMBER_OF_POINTS_CALCULATED_INTO_CLUMP = clump_number
                datapoint.clump_score = sum(sorted_distances[0:NUMBER_OF_POINTS_CALCULATED_INTO_CLUMP])

            for datapoint in datapoints:
                datapoint.random_value = random.randrange(0, 100)

            # calculating weights
            datapoints = sorted(datapoints, key=lambda datapoint: datapoint.current_distance)
            for i in range(len(datapoints)):
                min_max_difference = datapoints[-1].current_distance - datapoints[0].current_distance
                datapoints[i].distance_weight = 100 - (100 / min_max_difference) * (
                        datapoints[i].current_distance - datapoints[0].current_distance)

            datapoints = sorted(datapoints, key=lambda datapoint: datapoint.current_angle)
            for i in range(len(datapoints)):
                min_max_difference = datapoints[-1].current_angle - datapoints[0].current_angle
                datapoints[i].bearing_weight = 100 - (100 / min_max_difference) * (
                        datapoints[i].current_angle - datapoints[0].current_angle)

            datapoints = sorted(datapoints, key=lambda datapoint: datapoint.clump_score)
            for i in range(len(datapoints)):
                min_max_difference = datapoints[-1].clump_score - datapoints[0].clump_score
                datapoints[i].clump_weight = 100 - (100 / min_max_difference) * (
                        datapoints[i].clump_score - datapoints[0].clump_score)

            for i in range(len(datapoints)):
                datapoints[i].recalculate_total_weight(distance_multiplier, bearing_multiplier, clump_multiplier,
                                                       random_multiplier)

            datapoints = sorted(datapoints, key=lambda datapoint: datapoint.total_weight, reverse=True)

            accumulated_distance = 0
            constructed_route = []

            constructed_route.append(datapoints.pop(0))
            accumulated_distance += constructed_route[0].distances[self.locations[0]]

            while len(datapoints) > 2:
                constructed_route.append(datapoints.pop(0))
                accumulated_distance += constructed_route[-1].distances[constructed_route[-2].corresponding_location]
                if accumulated_distance + constructed_route[-1].distances[self.locations[-1]] > self.max_distance:
                    constructed_route.pop()
                    break

                for datapoint in datapoints:
                    datapoint.current_distance = datapoint.distances[constructed_route[-1].corresponding_location]

                datapoints = sorted(datapoints, key=lambda datapoint: datapoint.current_distance)
                for i in range(len(datapoints)):
                    min_max_difference = datapoints[-1].current_distance - datapoints[0].current_distance
                    datapoints[i].distance_weight = 100 - (100 / min_max_difference) * (
                            datapoints[i].current_distance - datapoints[0].current_distance)

                for datapoint in datapoints:
                    datapoint.current_angle = calculate_bearing_difference(
                        self.bearing_map[(constructed_route[-1].corresponding_location, self.locations[-1])],
                        self.bearing_map[(
                            constructed_route[-1].corresponding_location, datapoint.corresponding_location)])
                    # datapoint.current_angle = calculate_bearing_difference(
                    #     calculate_initial_compass_bearing((constructed_route[-1].y, constructed_route[-1].x),
                    #                                       (self.locations[-1].y, self.locations[-1].x)),
                    #     calculate_initial_compass_bearing((constructed_route[-1].y, constructed_route[-1].x),
                    #                                       (datapoint.y, datapoint.x)))

                datapoints = sorted(datapoints, key=lambda datapoint: datapoint.current_angle)
                for i in range(len(datapoints)):
                    min_max_difference = datapoints[-1].current_angle - datapoints[0].current_angle
                    datapoints[i].bearing_weight = 100 - (100 / min_max_difference) * (
                        datapoints[i].current_angle - datapoints[0].current_angle)

                for i in range(len(datapoints)):
                    datapoints[i].recalculate_total_weight(distance_multiplier, bearing_multiplier,
                                                           clump_multiplier,
                                                           random_multiplier)

                datapoints = sorted(datapoints, key=lambda datapoint: datapoint.total_weight, reverse=True)

            print(len(constructed_route))
            if distance_multiplier == 0 and bearing_multiplier == 1 and random_multiplier == 0 and clump_multiplier == 0:
                self.only_bearing_route = (Route(start=self.locations[0],
                                                 end=self.locations[-1],
                                                 intermediate_points=[route_point.corresponding_location for
                                                                      route_point
                                                                      in
                                                                      constructed_route]))
            if distance_multiplier == 1 and bearing_multiplier == 0 and random_multiplier == 0 and clump_multiplier == 0:
                self.only_distance_route = (Route(start=self.locations[0],
                                                  end=self.locations[-1],
                                                  intermediate_points=[route_point.corresponding_location for
                                                                       route_point in
                                                                       constructed_route]))
            if len(self.routes) == 0 or len(self.routes[-1].intermediate_points) < len(constructed_route):
                print('found_better')
                self.routes.append(Route(start=self.locations[0],
                                         end=self.locations[-1],
                                         intermediate_points=[route_point.corresponding_location for route_point in
                                                              constructed_route]))
                return True
            return False

    def calculate_number_of_routes(self, number_of_routes):
        # Call calculate_route a number_of_routes, either sequentially or using threads
        for i in range(number_of_routes):
            self._calculate_route()

    def calculate_routes_for_given_time(self, time_for_calculations=datetime.timedelta(seconds=5)):
        current_time = datetime.datetime.now()
        self.perform_initial_calculations()
        end_time = datetime.datetime.now() + time_for_calculations

        # Only distance
        self._calculate_route(1, 0, 0, 0)
        current_time = datetime.datetime.now()
        if current_time > end_time:
            return 0

        # Only bearing
        self._calculate_route(0, 1, 0, 0)
        current_time = datetime.datetime.now()
        if current_time > end_time:
            return 0

        # Only clump score
        self._calculate_route(0, 0, 1, 0)
        current_time = datetime.datetime.now()
        if current_time > end_time:
            return 0

        self._calculate_route(1, 1, 0, 0)
        current_time = datetime.datetime.now()
        if current_time > end_time:
            return 0

        self._calculate_route(1, 1.5, 0, 0)
        current_time = datetime.datetime.now()
        if current_time > end_time:
            return 0

        self._calculate_route(1, 0.5, 0, 0)
        current_time = datetime.datetime.now()
        if current_time > end_time:
            return 0

        iterations = 0
        was_better = False
        was_not_better_counter = 99999
        best_distance_multiplier = 1 + random.randrange(0, 1000) / 1000
        best_bearing_multiplier = random.randrange(0, 1000) / 1000
        best_clump_multiplier = random.randrange(0, 500) / 1000
        best_random_multiplier = random.randrange(0, 500) / 1000
        best_clump_number = random.randrange(3, 5)
        distance_multiplier = best_distance_multiplier
        bearing_multiplier = best_bearing_multiplier
        clump_multiplier = best_clump_multiplier
        random_multiplier = best_random_multiplier
        clump_number = best_clump_number

        while current_time < end_time:
            print('Time remaining: {time}'.format(time=end_time - current_time))
            iterations += 1
            if was_better:
                was_not_better_counter = 0
                best_distance_multiplier = distance_multiplier
                best_bearing_multiplier = bearing_multiplier
                best_clump_multiplier = clump_multiplier
                best_random_multiplier = random_multiplier
                best_clump_number = clump_number
            else:
                was_not_better_counter += 1
                if was_not_better_counter > 15:
                    which_to_change = random.randrange(0, 4)
                    if which_to_change == 0:
                        distance_multiplier = best_distance_multiplier + (random.randrange(0, 100) - 50) / 1000
                    if which_to_change == 1:
                        bearing_multiplier = best_bearing_multiplier + (random.randrange(0, 100) - 50) / 1000
                    if which_to_change == 2:
                        clump_multiplier = best_clump_multiplier + (random.randrange(0, 50) - 25) / 1000
                    if which_to_change == 3:
                        random_multiplier = best_random_multiplier + (random.randrange(0, 50) - 25) / 1000
                    if which_to_change == 4:
                        clump_number = best_clump_number + random.randrange(1, 3) - 2
                if was_not_better_counter > 50:
                    print('Resetting')
                    distance_multiplier = 1 + random.randrange(0, 1000) / 1000
                    bearing_multiplier = random.randrange(0, 1000) / 1000
                    clump_multiplier = random.randrange(0, 500) / 1000
                    random_multiplier = random.randrange(0, 500) / 1000
                    clump_number = random.randrange(3, 5)
            print('distance: {distance} ; bearing: {bearing} ; clump: {clump} ; random: {random}'.format(
                distance=distance_multiplier,
                bearing=bearing_multiplier,
                clump=clump_multiplier,
                random=random_multiplier))
            was_better = self._calculate_route(distance_multiplier=distance_multiplier,
                                               bearing_multiplier=bearing_multiplier,
                                               clump_multiplier=clump_multiplier,
                                               random_multiplier=random_multiplier,
                                               clump_number=clump_number)
            current_time = datetime.datetime.now()

        return iterations

    def get_route(self, route_index):
        return self.routes[route_index]

    def export_route_to_link(self, route_index):
        all_points_link = ''
        all_points_link += 'https://maps.openrouteservice.org/directions?n1={y_start}&n2={x_start}&n3=12&a={y_start},{x_start}'.format(
            x_start=self.locations[0].x,
            y_start=self.locations[0].y)
        for point in [location for i, location in enumerate(self.locations) if
                      i not in [0, len(self.locations) - 1]]:
            all_points_link += ',{y_point},{x_point}'.format(x_point=point.x,
                                                             y_point=point.y)

        all_points_link += ',{y_end},{x_end}&b=0&c=0&k1=en-US&k2=km'.format(
            x_end=self.locations[-1].x,
            y_end=self.locations[-1].y)
        print('All points: {link}'.format(link=all_points_link))

        if route_index > len(self.routes):
            return 'Index out of bounds'
        else:
            # DEBUG PRINTS START
            print('Intermediate points: {intermediate_points}'.format(
                intermediate_points=len(self.routes[route_index].intermediate_points)))
            # DEBUG PRINTS END

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
