# Twitter Sentiment Analysis Geoprocessing Service
![This is where an GIF should be. Sorry you can't see it. Try using Chrome](twitter_sentiment.gif "Application Demo")

<br><br>
## Overview
This geoprocessing tool can be exposed through a Geoprocessing Service on an ArcGIS Server.  As a proof of concept, this module uses the [Text Blob library and methodology](https://textblob.readthedocs.io/en/dev/) for sentiment analysis, but [more advanced](https://cloud.google.com/natural-language/) NLP libraries and methodologies can be used. 
<br>
<br>
The user passes in a string of text to be queried against the Twitter API and each tweet is parsed for analysis with TextBlob.  A <a href="http://tghays.github.io/twitter_verification.html">simple HTML page and table</a> is dynamically created each time the tool is run and displays request meta-data and each tweet with the calculated sentiment polarity.
<br>
<br>
## Usage
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
<br>
Iterate through the returned results objects, then iterate through each sentence by checking if the sentence is longer than 3 words and a sentiment analysis can be justified.  Sentiment polarity is retrieved for each sentence in the tweet, then averaged to obtain sentiment polarity for the tweet as a whole.
<br>

```python
for tweetObj in results:
    blob = TextBlob(tweetObj.text)
    date = tweetObj.created_at
    user = tweetObj.user.name

    temp_sentiment = []
    n = 0

    # iterate through sentences in tweet
    for sentence in blob.sentences:

        #check if sentence is longer than 3 words
        if len(sentence.words) > 3:

            # append sentiment of sentence, used later to average the sentiment for a given tweet, based on sentiment of each sentence
            temp_sentiment.append(sentence.sentiment.polarity)
            sentence_sentiments_list.append(sentence.sentiment.polarity)
            if n == 0:
                tweet_chart_list.append(blob.raw.encode('utf-8'))
                date_chart_list.append(date)
                user_chart_list.append(user.encode('utf-8'))
                n += 1

    # check if there is an average sentiment in each sentence of the tweet, depends on if the sentences in tweet contain more than 3 words
    if temp_sentiment:
        avg_sentiment = sum(temp_sentiment)/float(len(temp_sentiment))
        avg_sentiment_chart_list.append(avg_sentiment)
```
<br>
The average sentiment is calculated from the `avg_sentiment_chart_list` that has average sentiment appended to it for each tweet.  Based on the sentiment polarity value, a sentiment classification is assigned (e.g. "Slightly Good" for 0.1-0.2 polarity).  Using ArcPy, the response is returned as a string by the SetParameterAsText method.  The HTML page is created here as well, looping through zipped lists of the tweet meta-data and inserts this information in a HTML table.
<br>
```python
  if len(avg_sentiment_chart_list) > 0 :
      ret_string = '{3} Sentiment is {0} ({1}), based on {2} tweets in the last week.  Sentiment Polarity is on a scale from -1 to +1 and uses the NLTK methodology'.format(overall_sentiment, overall_sentiment_val_str, str(number_tweets), query)
      arcpy.AddMessage(ret_string)
      arcpy.SetParameterAsText(1, ret_string)
      print(ret_string)

      #HTML Page Created here

  else:
      ret_string = 'There are zero tweets returned in the last week from the query "{0}"'.format(query)
      arcpy.AddMessage(ret_string)
      arcpy.SetParameterAsText(1, ret_string)
```
<br>
