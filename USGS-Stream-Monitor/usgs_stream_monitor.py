import urllib, json, time, datetime, arcpy

station = arcpy.GetParameterAsText(0)
url = "https://waterservices.usgs.gov/nwis/iv/?format=json&indent=on&sites={0}&parameterCd=00060,00065".format(str(station))

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

vals = getData()
output1 = '{0}'.format(vals[3])
output2 = '{0} ft3/second'.format(vals[0])
output3 = '{0} ft'.format(vals[1])
output4 = '{0}'.format(vals[2])

mainOutput = 'Site Name: {3} \nDischarge Rate: {0} ft3/second \nGage Height: {1} ft \nMeasured at: {2}'.format(vals[0], vals[1], vals[2], vals[3])

arcpy.SetParameterAsText(1, output1)
arcpy.SetParameterAsText(2, output2)
arcpy.SetParameterAsText(3, output3)
arcpy.SetParameterAsText(4, output4)
