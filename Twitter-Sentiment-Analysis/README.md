<img style="align:center" src'></img>





Within this script, the user first authenticates themself with the Twitter API using the <a href="https://github.com/bear/python-twitter">Python-Twitter library</a>:

```
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'

access_token_key = 'access_token_key'
access_token_secret = 'access_token_secret'

api = Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)
```

The <a href="https://github.com/Esri/developer-support/tree/master/python/arcpy-python">ArcPy module</a> is used to retrieve input from the user and construct a URL query to be passed into the Twitter Search API:

```
query = arcpy.GetParameterAsText(0)
if len(query) > 1:
    urlQuery = query.replace(' ', '%20')
else:
    urlQuery = query

results = api.GetSearch(raw_query="q={0}&count=300".format(urlQuery))
```
