"""This module contains a CLI for creating an n-band GeoTIFF from multiple 
layers in a CSV file. It requires GDAL to run."""

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

CMD_TEMPLATE = """gdal_grid -ot Int16 -tye -.82 1.68 -txe 100.57 103.07 -zfield %(layer)s -a nearest:radius1=.0083333:radius2=.0083333:nodata=255 -of GTiff -l %(filename)s %(filename)s-%(layer)s.vrt %(filename)s-%(layer)s.tiff"""

def _get_options():
    """Creates and returns an new OptionParser with options."""
    parser = optparse.OptionParser()

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

def _gdal_grid(filename, layers):
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

def _merge_grids(filename):
    # TODO
    pass

def main():
    logging.basicConfig(level=logging.DEBUG)
    options = _get_options()

    filename = os.path.splitext(options.filename)[0]
    layers = [x.strip() for x in options.layers.split(',')]
    
    _gdal_grid(filename, layers)
    
if __name__ == '__main__':
    main()
