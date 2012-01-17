"""
Get bounding box and height/width for a given csv file where the first 2 columns are lat and lon, respectively.
"""
import sys

f = open(sys.argv[1], "r")

max_lat = -90
min_lat = 90
max_lon = -180
min_lon = 180

n = 0
for line in f:
    try:
        lat, lon = [float(i) for i in line.split(",")[:2]]
        if lat > max_lat:
            max_lat = lat
        if lat < min_lat:
            min_lat = lat
        if lon > max_lon:
            max_lon = lon
        if lon < min_lon:
            min_lon = lon
    except ValueError:
        print "Skipping mid-file header"
    n += 1
print
print "min_lat: %.6f\nmax_lat: %.6f\nmin_lon: %.6f\nmax_lon:%.6f" % (min_lat, max_lat, min_lon, max_lon)
print
print "height", (max_lat - min_lat)/.008333333
print "width", (max_lon - min_lon)/.008333333