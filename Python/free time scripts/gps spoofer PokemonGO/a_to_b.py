# noinspection PyPep8Naming
import xml.etree.cElementTree as ET
import random


# PATH TO GPX FILE
GPX_PATH = "/Users/filipstastny/Desktop/GPS/pokemonLocation.gpx"

# MOVEMENT SPEED (1 walk - 6 tram)
SPEED = 3
STEP = 0.00001

####################################################
# AVG kancl                     49.180759, 16.605574
# 2-spot Spielberk cafe         49.181735, 16.605746
# 3-spot Kometa pres reku       49.184484, 16.598937
# 3-spot Spilberk               49.194616, 16.600766
# 4-spot Kamenny Vrch           49.174033, 16.555623
# GYM Svitici podchod           49.182899, 16.604097
# GYM Kometa                    49.185020, 16.602104
# GYM Barok. sal Milosrdnych    49.185081, 16.595378
# GYM Textilacka                49.188251, 16.588237
# GYM Sprava koleji a menz MU   49.191925, 16.582132
# GYM Vez u pavilonuG           49.189730, 16.578227
# GYM BVV Brno                  49.188741, 16.572970
# GYM M-palac                   49.177361, 16.604132
# GYM Spilberk                  49.193778, 16.600106
####################################################
STARTING_LOCATION = """
49.194423, 16.597516
"""
FINAL_LOCATION = """
49.194616, 16.600766
"""


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


# gpx header
gpx = ET.Element("gpx", version="1.1", creator="Xcode")

lat = float(STARTING_LOCATION.strip().split(',')[0].strip())
lon = float(STARTING_LOCATION.strip().split(',')[1].strip())
lat_final_precise = float(FINAL_LOCATION.strip().split(',')[0].strip())
lon_final_precise = float(FINAL_LOCATION.strip().split(',')[1].strip())

# approximate final position +-35m (0.0001 to 0.0002 gps equals ~18.5 m)
lat_final = [round(lat_final_precise, 4), round(lat_final_precise+0.0001, 4)]
lon_final = [round(lon_final_precise, 4), round(lon_final_precise+0.0001, 4)]

# coefficient - to set the correct direction
coef_lat = (lat_final_precise-lat) / abs(lat_final_precise-lat) if lat_final_precise-lat != 0 else 1
coef_lon = (lon_final_precise-lon) / abs(lon_final_precise-lon) if lon_final_precise-lon != 0 else 1

lat_reached = round(lat, 4) in lat_final
lon_reached = round(lon, 4) in lon_final
counter = 0
while not lat_reached or not lon_reached:
    counter += 1
    if not lat_reached:
        lat += coef_lat * SPEED * STEP
        lat_reached = round(lat, 4) in lat_final

    if not lon_reached:
        lon += coef_lon * SPEED * STEP
        lon_reached = round(lon, 4) in lon_final

    ET.SubElement(gpx, "wpt", lat=str(lat+random.uniform(0.0, 0.00001)), lon=str(lon+random.uniform(0.0, 0.00001)))  # add new location with current coordinates

i = 0
# the number means how many times the final position will be reported, generally it is like 2-3 positions ~ 1 second
while i < 15000:
    ET.SubElement(gpx, "wpt", lat=str(lat_final_precise+random.uniform(0.000000, 0.000010)), lon=str(lon_final_precise+random.uniform(0.000000, 0.000010)))  # add new location with current coordinates
    i += 1

# pretty formatting
indent(gpx)

# write to file
gpx_file = open(GPX_PATH, "w")
gpx_file.write(ET.tostring(gpx))
gpx_file.close()

print "\n{0}X to Y generated GPX file{0}".format('\n'+15*'='+'\n')
