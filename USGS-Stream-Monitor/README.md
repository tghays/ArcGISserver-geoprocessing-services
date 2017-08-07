# USGS Stream Monitoring

This published geoprocessing tool runs a python script that queries the USGS API for stream data for a specified Stream Monitoring Station.  Available stream monitoring stations can be found on the [National Water Information System Mapper](https://maps.waterdata.usgs.gov/mapper/index.html).  This default value for the input field in the geoprocessing tool is 0212414900, which is the site ID for the Stream Monitoring Station at the Mallard Creek Greenway.


## How it works
A request is sent using the URL query with the formatted station ID, obtained from the user using the ArcPy module.
```python
station = arcpy.GetParameterAsText(0)
url = "https://waterservices.usgs.gov/nwis/iv/?format=json&indent=on&sites={0}&parameterCd=00060,00065".format(str(station))
```

A function is defined to make the request, and parse the json that is returned.  Discharge rate, Gage height, time of measurement, and site name are returned.
```python
def getData():
    url = "https://waterservices.usgs.gov/nwis/iv/?format=json&indent=on&sites={0}&parameterCd=00060,00065".format(str(station))
    response = urllib.urlopen(url)
    read_resp = response.read()
    data = json.loads(read_resp)
    discharge = float(data['value']['timeSeries'][0]['values'][0]['value'][0]['value'])
    gageHeight = float(data['value']['timeSeries'][1]['values'][0]['value'][0]['value'])

    state = data['value']['timeSeries'][0]['sourceInfo']['siteName'][-2:]
    titleCase = data['value']['timeSeries'][0]['sourceInfo']['siteName'][:-2].title()
    siteName = titleCase + state

    timeVal = data['value']['timeSeries'][0]['values'][0]['value'][0]['dateTime'][:-6]
    timeObj = datetime.datetime.strptime(timeVal,'%Y-%m-%dT%H:%M:%S.%f')
    timeStr = datetime.datetime.strftime(timeObj, '%Y-%m-%d %I:%M %p')
    return discharge, gageHeight, timeStr, siteName
```

Run the getData() function and assign the return values for each parameter to be returned.
```python
vals = getData()
output1 = '{0}'.format(vals[3])
output2 = '{0} ft3/second'.format(vals[0])
output3 = '{0} ft'.format(vals[1])
output4 = '{0}'.format(vals[2])
```

Print the main output for the geoprocessing tool
```python
mainOutput = 'Site Name: {3} \nDischarge Rate: {0} ft3/second \nGage Height: {1} ft \nMeasured at: {2}'.format(vals[0], vals[1], vals[2], vals[3])
arcpy.SetParameterAsText(1, output1)
arcpy.SetParameterAsText(2, output2)
arcpy.SetParameterAsText(3, output3)
arcpy.SetParameterAsText(4, output4)
```
