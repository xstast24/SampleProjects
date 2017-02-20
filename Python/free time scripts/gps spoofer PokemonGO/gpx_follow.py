# noinspection PyPep8Naming
import xml.etree.cElementTree as ET
import random
import os


#####################################################################################################################
#####################################################################################################################
# INPUT & OUTPUT GPX FILES PATHS
INPUT_GPX_PATH = "/Users/filipstastny/Downloads/vlastni_body.gpx"
OUTPUT_GPX_PATH = "/Users/filipstastny/Desktop/GPS/pokemonLocation.gpx"

# MOVEMENT SPEED (1 walk - 6 tram)
SPEED = 9
STEP = 0.00001

# FINAL POSITION TIME
# 25000 ~ 1 MB output gpx file, 50000 ~ 2 MB output gpx file
# the number means how many times the final position will be reported, generally it is like 2-3 positions ~ 1 second
REPEAT_FINAL_LOC_COUNT = 20000
#####################################################################################################################
#####################################################################################################################


# LOAD INPUT GPX DATA from file, or use "filename_last_used.gpx"
# afterwards delete the original gpx file -> old files do not gather in downloads folder
INPUT_GPX_PATH_LAST_USED = INPUT_GPX_PATH.strip('.gpx') + '_last_used.gpx'
content = None
try:
    with open(INPUT_GPX_PATH, 'r+') as input_gpx_file:
        content = input_gpx_file.read()
        with open(INPUT_GPX_PATH_LAST_USED, 'w+') as input_gpx_file_last_used:
            input_gpx_file_last_used.write(content)
    os.remove(INPUT_GPX_PATH)
except IOError:
    try:
        print "\nWARNING: No new GPX file found at path: {0}\nINFO: Loading the last used GPX file: {1}".format(INPUT_GPX_PATH, INPUT_GPX_PATH_LAST_USED)
        with open(INPUT_GPX_PATH_LAST_USED, 'r+') as input_gpx_file:
            content = input_gpx_file.read()
    except IOError:
        print "ERROR:No previously used GPX file found at path: {0}\n\n{1}\n################ EXECUTION FAILED ################\n{1}".format(INPUT_GPX_PATH_LAST_USED, 50*'!')
        exit(1)

# edit input data so ET can parse the file properly
content = content.replace('xmlns="http://www.topografix.com/GPX/1/1" ', '', 1)
input_gpx = ET.fromstring(content)


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


def add_gps_coordinates_between(gpx_root, start_lat, start_lon, final_lat, final_lon, speed, step):
    """
    Add location points between two given locations and write them to the given gpx root of ElementTree.
    :param gpx_root: ElementTree root
    :param start_lat: starting point latitude
    :param start_lon: starting point longitude
    :param final_lat: ending point latitude
    :param final_lon: ending point longitude
    :param speed: speed multiplier - affects how far the next location if from the previous one, 1 = "step" length, 2 = 2*"step" length, 3 = 3*"step" length
    :param step: sets how far the next location is from the previous one if there is no "speed" multiplier
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

        ET.SubElement(gpx_root, "wpt", lat=str(current_lat + random.uniform(0.0, 0.00001)), lon=str(current_lon + random.uniform(0.0, 0.00001)))  # add new location with current coordinates

    ET.SubElement(gpx_root, "wpt", lat=str(final_lat + random.uniform(0.000005, 0.00001)), lon=str(final_lon + random.uniform(0.000005, 0.00001)))  # add new location with final coordinates randomized
    ET.SubElement(gpx_root, "wpt", lat=str(final_lat + random.uniform(0.0, 0.00001)), lon=str(final_lon + random.uniform(0.0, 0.00001)))  # add new location with precise final coordinates


# gpx header
gpx = ET.Element("gpx", version="1.1", creator="Xcode")
# counting GPS points
lat = None
lon = None
prev_lat = None
prev_lon = None
for location in input_gpx.findall('wpt'):
    lat = location.attrib['lat']
    lon = location.attrib['lon']
    # fill gpx root element with wpt lcoations
    if prev_lat:
        add_gps_coordinates_between(gpx, prev_lat, prev_lon, lat, lon, SPEED, STEP)

    prev_lat = lat
    prev_lon = lon

i = 0
while i < REPEAT_FINAL_LOC_COUNT:
    ET.SubElement(gpx, "wpt", lat=str(float(lat)+random.uniform(0.000000, 0.000010)), lon=str(float(lon)+random.uniform(0.000000, 0.000010)))  # add new location with current coordinates
    i += 1

# pretty formatting
indent(gpx)

# write to file
gpx_file = open(OUTPUT_GPX_PATH, "w")
gpx_file.write(ET.tostring(gpx))
gpx_file.close()

print "\n============ LOCATION SAVED SUCCESSFULLY ============"
exit()
