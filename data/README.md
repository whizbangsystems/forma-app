# Data processing #

This directory contains code for processing FORMA data into formats used by the web app.

## Converting CSV to GeoTIFF ##

The `gdal-grid` script converts CSV to GeoTIFF!
                                                                                         
http://www.gdal.org/gdal_grid.html                                                                                       
                                                                                                                           
For this to work we need to create a Virtual Format header for the CSV file which is described here:
                                                                
http://www.gdal.org/ogr/drv_vrt.html                                                                                       
                                                                                                                           
For example, here's a snippet of the `idn.csv` test data:

```csv
lat,lon,prob201108
1.670833,100.5719,101
1.6625,100.5715,101
1.654167,100.5711,101
```                                                                                 
   
You would then create the following `idn.vrt` file:

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

Note that the radius defines the pixel size.

Here's the output:

![](http://i.imgur.com/ry778.png)
