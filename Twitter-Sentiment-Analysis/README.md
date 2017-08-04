<img style="align:center" src="twitter_sentiment.gif"></img>


<br><br>
## Usage
This geoprocessing tool can be exposed through a Geoprocessing Service on an ArcGIS Server.  The user passes in a string of text to the input field and a the python script is run on the ArcGIS Server machine.  As a proof of concepthis module uses the <a href="https://textblob.readthedocs.io/en/dev/">TextBlob library and methodology</a> for sentiment analysis.

The user first authenticates themself with the Twitter API using the <a href="https://github.com/bear/python-twitter">Python-Twitter library</a>:

```python
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'

access_token_key = 'access_token_key'
access_token_secret = 'access_token_secret'

api = Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)
```
<br>
The <a href="https://github.com/Esri/developer-support/tree/master/python/arcpy-python">ArcPy module</a> is used to retrieve input from the user and construct a URL query to be passed into the Twitter Search API:

```python
query = arcpy.GetParameterAsText(0)
if len(query) > 1:
    urlQuery = query.replace(' ', '%20')
else:
    urlQuery = query

results = api.GetSearch(raw_query="q={0}&count=300".format(urlQuery))
```
