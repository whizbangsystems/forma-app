# Data processing #

This directory contains code for processing FORMA data into formats used by the web app.

## Converting CSV to GeoTIFF ##

The `gdal-grid` script converts CSV to GeoTIFF:
                                                                                         
http://www.gdal.org/gdal_grid.html                                                                                       
                                                                                                                           
For this to work you need to create a Virtual Format header for the CSV file which is described here:
                                                                
http://www.gdal.org/ogr/drv_vrt.html                                                                                       
                                                                                                                           
For example here's a snippet of the `idn.csv` test data:

```csv
lat,lon,m201108
.7458333,110.6219,1
.7375,110.6217,1
.7291667,110.6215,1
```                                                                                 
   
You would then create the following `idn.vrt` file:

```xml                                                                                                                        
<OGRVRTDataSource>                                                                                                         
    <OGRVRTLayer name="idn">                                                                                               
        <SrcDataSource>idn.csv</SrcDataSource>                                                                             
        <SrcRegion clip="true">BOX(110.62 -3.6875,116.0599 0.9125)</SrcRegion>                                             
        <GeometryType>wkbPoint</GeometryType>                                                                              
        <LayerSRS>WGS84</LayerSRS>                                                                                         
        <GeometryField encoding="PointFromColumns" x="lon" y="lat"/>                                                       
    </OGRVRTLayer>                                                                                                         
</OGRVRTDataSource>                                                                                                        
```
                                                                                                                      
The `<srcregion>` BOX was created by uploading the CSV to CartoDB and running:

```sql                                                     
select pg_extent(the_geom) from table;                                                                                     
```      
                                                                                                                     
After that i ran this command:

```shell                                                   
gdal_grid -a invdist:power=2.0:smoothing=1.0 -txe 85000 89000 -tye 894000 890000 -outsize 400 400 -of GTiff -ot Float64 -l\
 idn idn.vrt idn.tiff 
```