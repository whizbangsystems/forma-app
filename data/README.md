# Data processing #

This directory contains code for processing FORMA data into formats used by the web app.

## Converting CSV to a single band GeoTIFF ##

Instead of dealing with pixel probabilities, we're encoding periods into a single band which scales up to 11 years on a single band. Here's the schema:

```
0: No deforrestation
1-250: Deforrestation period as integer (1 = January 2006, 2 = February 2006, ...)
251-254: Reserved
255: NODATA
```

First we us the `gdal-grid` script to convert CSV to GeoTIFF:
                                                                                         
http://www.gdal.org/gdal_grid.html                                                                                       
                                                                                                                           
For this to work we need to create a Virtual Format header for the CSV file which is described here:
                                                                
http://www.gdal.org/ogr/drv_vrt.html                                                                                       
                                                                                                                           
For example, here's a snippet of the `IDN_riau_201108_nh_100.csv` test data:

```csv
lat,lon,prob201108
1.670833,100.5719,101
1.6625,100.5715,101
1.654167,100.5711,101
```                                                                                 
   
You would then create the following `IDN_riau_201108_nh_100.vrt` file:

```xml                                                                                                                    
<OGRVRTDataSource>
    <OGRVRTLayer name="IDN_riau_201108_nh_100">
        <SrcDataSource>IDN_riau_201108_nh_100.csv</SrcDataSource> 
        <GeometryType>wkbPoint</GeometryType> 
        <LayerSRS>WGS84</LayerSRS>
        <GeometryField encoding="PointFromColumns" x="lon" y="lat" z="prob201108"/> 
    </OGRVRTLayer>
</OGRVRTDataSource>
```
                                                                                                                     
Given the .csv and .vrt files, we run the following command to get the GeoTIFF:

```shell                                                   
gdal_grid -ot Int16 -tye -.82 1.68 -txe 100.57 103.07 -zfield prob201108 -a nearest:radius1=.0083333:radius2=.0083333:nodata=255 -of GTiff -l IDN_riau_201108_nh_100 IDN_riau_201108.vrt IDN_riau_201108_nh_100.tiff
```

Note that the radius is defined in terms of the pixel units (i.e. size), NOT pixels. So the radius for one 1km pixels is .008333333, not 1.

Here's the output:

![](http://i.imgur.com/ry778.png)

All of this is automated in the `gtiffer.py` script.

## Converting CSV into multi-band GeoTIFF ##

First you have to warp GeoTIFFs created above via `gdalwarp` like this:

```shell
gdalwarp IDN_riau_201108-prob201108.tiff IDN_riau_201108-prob201108-warp.tiff
```

And then create a combined VRT (one tiff per band)

```shell
gdalbuildvrt IDN_riau_201108-prob201108-warp.vrt IDN_riau_201108-prob201108-warp.tiff
```

Now `IDN_riau_201108-prob201108-warp.vrt` defines a GeoTIFF with multiple bands. Final move is another call to `gdal_grid` to merge them all into a n-band GeoTIFF.

# By the way - 500m warping

Although the data are actually 1km resolution (0.00833333 deg.), we are very close to having 500m data (0.004166666 deg.). So to facilitate app development we've gdalwarped the file to that higher resolution:

```shell
gdalwarp -tr .0041666666 .0041666666 -overwrite -srcnodata 255 -dstnodata 255 SE_Asia_clean-bandified-period.tiff SE_Asia_500m.tif
```
