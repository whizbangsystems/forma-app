#!/usr/bin/env python
#
# Copyright 2011 Whizbang Systems LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""This module contains a CLI for creating an n-band GeoTIFF from multiple 
layers in a CSV file. It supports creating a single-band GeoTIFF from
multiple periods in a CSV file. It requires GDAL to run."""

import csv
import logging
import optparse
import os
import shlex
import shutil
import subprocess

VRT_TEMPLATE = """<OGRVRTDataSource>
    <OGRVRTLayer name="%(filename)s">
        <SrcDataSource>%(filename)s.csv</SrcDataSource> 
        <GeometryType>wkbPoint</GeometryType> 
        <LayerSRS>WGS84</LayerSRS>
        <GeometryField encoding="PointFromColumns" x="lon" y="lat" z="%(layer)s"/> 
    </OGRVRTLayer>
</OGRVRTDataSource>"""

CMD_TEMPLATE = """gdal_grid -ot Int16 -outsize 7847 5028 -tye -11.57917 30.32083 -txe 89.91154 155.3057 -zfield %(layer)s -a nearest:radius1=.0083333:radius2=.0083333:nodata=255 -of GTiff -l %(filename)s %(filename)s-%(layer)s.vrt %(filename)s-%(layer)s.tiff"""

def _get_options():
    """Creates and returns an new OptionParser with options."""
    parser = optparse.OptionParser()

    parser.add_option(
        '-a',
        type='string',
        dest='action',
        help='Action (n-band | 1-band)')

    parser.add_option(
        '-f', 
        type='string',
        dest='filename',
        help='CSV filename.')

    parser.add_option(
        '-l', 
        type='string',
        dest='layers',
        help='CSV list of layer names.')

    return parser.parse_args()[0]

def gdal_grid(filename, layers):
    """Writes multiple GeoTIFF files, 1 per layer."""
    for layer in layers:
        d = dict(layer=layer, filename=filename)
        f = open("%(filename)s-%(layer)s.vrt" % d, 'w')
        f.write(VRT_TEMPLATE % d)
        f.close()
        cmd = CMD_TEMPLATE % d
        logging.info(cmd)
        p = subprocess.Popen(
            shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error, output = p.communicate()
        logging.info(output)

def filter_row(row):
    # this gets us the period index without having to worry about the date!
    # assumes starts at 200601
    try:
        # TODO(robin): Why is x sometimes null here? Check SE_Asia.csv format.
        probs = sorted([x for x in row.keys() if x and x.startswith('prob')])
    except:
        logging.info(row)

    hval = int(row['hansen'])
    lat = float(row['lat'])
    lon = float(row['lon'])
    
    # default prob index (pidx) is no defor (but not nodata, which is 255)
    pidx = 254

    # hansen runs from 0-400 (0, 100, 200, 300, 400), representing the # of
    # 500m Hansen 'hits' in a given MODIS pixel
    # we assign hansen values to 0 because we don't want to say FORMA
    # detected something Matt already detected between 2000-5.

    if hval != 0:
        pidx = 0
    else:
        # but if he didn't detect anything, FORMA values are fair game
        # we want to store the index of the value
        for i in range(len(probs)):
            # get the value for the period of interest
            val = int(row[probs[i]])
            if val >= 50:
                # zero is reserved for Hansen, per Andrew's request 1/17/12
                pidx = i + 1
                break
    
    return dict(lat=lat, lon=lon, period=pidx)

def bandify(filename):
    logging.info(filename)
    fout = open('%s-bandified.csv' % os.path.splitext(filename)[0], 'w')
    dw = csv.DictWriter(fout, ['lat', 'lon', 'period'])
    dw.writeheader()
    for row in csv.DictReader(open(filename, 'r'), skipinitialspace=True):
      try:
        float(row.values()[0])
      except ValueError:
        print "Skipping mid-file header"
        continue
      dw.writerow(filter_row(row))
  
def _merge_grids(filename):
    # TODO
    pass

def main():
    logging.basicConfig(level=logging.DEBUG)
    options = _get_options()
    action = options.action
    if action == 'n-band':
        filename = os.path.splitext(options.filename)[0]
        layers = [x.strip() for x in options.layers.split(',')]
        gdal_grid(filename, layers)
    elif action == '1-band':
        filename = options.filename
        bandify(filename)
    
if __name__ == '__main__':
    main()
