# noinspection PyPep8Naming
import xml.etree.cElementTree as ET
import random


#####################################################################################################################
#####################################################################################################################
# OUTPUT GPX FILES PATHS
OUTPUT_GPX_PATH = "/Users/filipstastny/Desktop/GPS/pokemonLocation.gpx"

# MOVEMENT SPEED (1 walk - 6 tram)
# fail safe values, do not change... for custom calculations - http://www.csgnetwork.com/gpsdistcalc.html
# GPS [x,y] to [x+0.00001,y+0.00001] ~ 2.619 m ~ 157 m/min ~ 9.428 km/h
# GPS [x,y] to [x+0.000012,y+0.000012] ~ 3.144 m ~ 189 m/min ~ 11.318 km/h
# GPS [x,y] to [x+0.000013,y+0.000013] ~ 3.405 m ~ 204 m/min ~ 12.258 km/h
SPEED = 1
STEP = 0.000014
STEP_MAX_RANDOM = 0.000003

# CENTER LOCATION (starting, center and final location is the same one)
CENTER_LOCATION = """
49.180759, 16.605574
"""

# DISTANCE
# max allowed distance from the CENTER_LOCATION (in gps coordinates increment), for custom calculations - http://www.csgnetwork.com/gpsdistcalc.html
# GPS [x,y] -> [x+0.004,y+0.004] ~ 1048 m
MAX_GPS_DISTANCE = 0.004
# how many times the CENTER LCOATION location will be crossed
# one crossing equals walked distance 2 * MAX_GPS_DISTANCE (default ~ 2.1 km), possibly less (down to minus 60 seconds of walking, default ~ -180 m)
NUMBER_OF_CROSSINGS = 20
#####################################################################################################################
#####################################################################################################################


def indent(elem, level=0):
    """
    Method for indenting ElementTree.
    :param elem: element or root
    :param level
    """
    ix = "\n" + level*"  "
    jx = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = ix + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = ix
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = jx
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = jx
    return elem


def get_marginal_points(center_lat, center_lon, max_gps_distance, number_of_points, max_rand=0.00001):
    """
    Counts marginal/extreme/side locations, which are allowed as maximum distance from the center location.
    Final GPS values are randomized according to max_rand parameter.
    :param center_lat: starting/center/final location latitude
    :param center_lon: starting/center/final location longitude
    :param max_gps_distance: gps value that is added to both center latitude and center longitude and that makes a marginal point
    :param number_of_points: how many marginal points will be generated
    :param max_rand: maximum random value that can be added to location coordinates
    :return: list of dictionaries with 'lat' and 'lon' values for starting, each marginal and ending point
    """
    center_lat = float(center_lat)
    center_lon = float(center_lon)
    marginal_points = [{'lat': center_lat, 'lon': center_lon}]
    points_count = 0
    while points_count < number_of_points:
        if points_count % 2 == 0:
            point_lat = center_lat + max_gps_distance + random.uniform(0.0, max_rand)
            point_lon = center_lon + max_gps_distance + random.uniform(0.0, max_rand)
        else:
            point_lat = center_lat - max_gps_distance - random.uniform(0.0, max_rand)
            point_lon = center_lon - max_gps_distance - random.uniform(0.0, max_rand)

        marginal_points.append({'lat': point_lat, 'lon': point_lon})
        points_count += 1

    marginal_points.append({'lat': center_lat, 'lon': center_lon})  # append the final center location
    return marginal_points


def add_gps_coordinates_between(gpx_root, start_lat, start_lon, final_lat, final_lon, speed, step, max_rand=0.00001):
    """
    Add location points between two given locations and write them to the given gpx root of ElementTree.
    Final GPS values are randomized according to max_rand parameter.
    :param gpx_root: ElementTree root
    :param start_lat: starting point latitude
    :param start_lon: starting point longitude
    :param final_lat: ending point latitude
    :param final_lon: ending point longitude
    :param speed: speed multiplier - affects how far the next location if from the previous one, 1 = "step" length, 2 = 2*"step" length, 3 = 3*"step" length
    :param step: sets how far the next location is from the previous one if there is no "speed" multiplier
    :param max_rand: maximum random value that can be added to location coordinates
    """
    start_lat = float(start_lat)
    start_lon = float(start_lon)
    final_lat = float(final_lat)
    final_lon = float(final_lon)
    # approximate final position +-30m (0.0001 to 0.0002 gps equals ~18.5 m)
    lat_final = [round(final_lat, 4), round(final_lat + 0.0001, 4), round(final_lat + 0.0002, 4)]
    lon_final = [round(final_lon, 4), round(final_lon + 0.0001, 4), round(final_lon + 0.0002, 4)]
    # coefficient - to set the correct direction
    coef_lat = (final_lat-start_lat) / abs(final_lat-start_lat) if final_lat-start_lat != 0 else 1
    coef_lon = (final_lon-start_lon) / abs(final_lon-start_lon) if final_lon-start_lon != 0 else 1
    # flags to say if the final lcoation has been achieved
    current_lat = start_lat
    current_lon = start_lon
    lat_reached = round(current_lat, 4) in lat_final
    lon_reached = round(current_lon, 4) in lon_final
    # count the coordinates between two locations
    while not lat_reached or not lon_reached:
        if not lat_reached:
            current_lat += coef_lat * speed * step
            lat_reached = round(current_lat, 4) in lat_final
        if not lon_reached:
            current_lon += coef_lon * speed * step
            lon_reached = round(current_lon, 4) in lon_final

        ET.SubElement(gpx_root, "wpt", lat=str(current_lat + random.uniform(0.0, max_rand)), lon=str(current_lon + random.uniform(0.0, max_rand)))  # add new location with current coordinates

    ET.SubElement(gpx_root, "wpt", lat=str(final_lat + random.uniform(0.0, max_rand)), lon=str(final_lon + random.uniform(0.0, max_rand)))  # add new location with final coordinates randomized
    ET.SubElement(gpx_root, "wpt", lat=str(final_lat + random.uniform(0.0, max_rand)), lon=str(final_lon + random.uniform(0.0, max_rand)))  # add new location with precise final coordinates


# gpx header
gpx = ET.Element("gpx", version="1.1", creator="Xcode")
# counting GPS points
lat = None
lon = None
prev_lat = None
prev_lon = None
locations = get_marginal_points(CENTER_LOCATION.split(',')[0].strip(), CENTER_LOCATION.split(',')[1].strip(), max_gps_distance=MAX_GPS_DISTANCE, number_of_points=NUMBER_OF_CROSSINGS)
for location in locations:
    lat = location['lat']
    lon = location['lon']
    # fill gpx root element with wpt lcoations
    if prev_lat:
        add_gps_coordinates_between(gpx, prev_lat, prev_lon, lat, lon, SPEED, STEP, STEP_MAX_RANDOM)

    prev_lat = lat
    prev_lon = lon


# pretty formatting
indent(gpx)

# write to file
gpx_file = open(OUTPUT_GPX_PATH, "w")
gpx_file.write(ET.tostring(gpx))
gpx_file.close()

print "\n============ LET'S WALK ============"
exit()
