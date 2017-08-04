from twitter.api import Api
import sys, arcpy
from textblob import TextBlob
import random
import datetime

#Authentication Credentials
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'

access_token_key = 'access_token_key'
access_token_secret = 'access_token_secret'

#Twitter API Authorization
api = Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token_key,
                  access_token_secret=access_token_secret)


query = arcpy.GetParameterAsText(0)
if len(query) > 1:
    urlQuery = query.replace(' ', '%20')
else:
    urlQuery = query

current_datetime = datetime.datetime.now()
current = current_datetime.strftime('%m-%d-%Y at %I:%M %p')

results = api.GetSearch(raw_query="q={0}&count=300".format(urlQuery))

#try:
temp_tweet_list = []
sentence_sentiments_list = []

# lists for output
date_chart_list = []
tweet_chart_list = []
user_chart_list = []
avg_sentiment_chart_list = []


count = 0

for tweetObj in results:
    temp_tweet_list.append(tweetObj.text)

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

if len(avg_sentiment_chart_list) > 0 :
    overall_sentiment_val = sum(avg_sentiment_chart_list)/float(len(avg_sentiment_chart_list))
    overall_sentiment_val_str = str(overall_sentiment_val)[:4]
    if overall_sentiment_val_str == str(-0.0):
        overall_sentiment_val_str = "0"
    number_tweets = len(tweet_chart_list)

    if .8 < overall_sentiment_val < 1:
        overall_sentiment = 'Near Complete Approval'

    elif .6 < overall_sentiment_val <= .8:
        overall_sentiment = 'Excellent'

    elif .4 < overall_sentiment_val <= .6:
        overall_sentiment = 'Very Good'

    elif .2 < overall_sentiment_val <= .4:
        overall_sentiment = 'Good'

    elif .1 < overall_sentiment_val <= .2:
        overall_sentiment = 'Slightly Good'

    elif -.1 < overall_sentiment_val <= .1:
        overall_sentiment = 'Average'

    elif -.2 < overall_sentiment_val <= -.1:
        overall_sentiment = 'Slightly Bad'

    elif -.4 < overall_sentiment_val <= -.2:
        overall_sentiment = 'Bad'

    elif -.6 < overall_sentiment_val <= -.4:
        overall_sentiment = 'Very Bad'

    elif -.8 < overall_sentiment_val <= -.6:
        overall_sentiment = 'Terrible'

    elif -1 < overall_sentiment_val <= -.8:
        overall_sentiment = 'Near Complete Disapproval'


if len(avg_sentiment_chart_list) > 0 :
    ret_string = '{3} Sentiment is {0} ({1}), based on {2} tweets in the last week.  Sentiment Polarity is on a scale from -1 to +1 and uses the NLTK methodology'.format(overall_sentiment, overall_sentiment_val_str, str(number_tweets), query)
    arcpy.AddMessage(ret_string)
    arcpy.SetParameterAsText(1, ret_string)
    print(ret_string)

    '''
    HTML page creation
    '''
    f = open('C:/inetpub/wwwroot/twitter_verification.html', 'w')

    # set up html, css, and table element
    f.write('<html><style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td{padding: 10px;}</style><body>')

    # create page title
    f.write('<title>Community Sentiment Analysis - Tweet Verifcation</title>')

    # create title heading for chart
    f.write('<h1 style="text-align: center">Charlotte Greenway Information Model - 2017 Intern Project</h1>')
    f.write('<h2 style="text-align: center">Twitter Sentiment Analysis Results for <div style="color: red">"{0}"</div></h2>'.format(query.title()))
    f.write('<h3 style="text-align: center; color:gray">via the Twitter API with NLTK methodology</h1><br><br>')

    f.write('<h3>Link to Twitter with Search Term: "<a href="https://twitter.com/search?q={0}">{0}</a>"</h3>'.format(query))
    f.write('<h3>Search query made at:  <span style="font-weight: normal">{0}</span></h3>'.format(current))
    f.write('<h3>Average Sentiment: <span style="font-weight: normal"> {0} ({1})</span></h3><br>'.format(overall_sentiment_val_str, overall_sentiment))
    # create table and table headings
    f.write('<table style="width:100%"><th>Tweet Date</th><th>Tweet</th><th>Sentiment Polarity</th><th>User Name</th>')

    # write a row for each tweet
    for t,d,u,s in zip(tweet_chart_list, date_chart_list, user_chart_list, avg_sentiment_chart_list):
        row_html = '<tr><td style="text-align: center">{0}</td><td>{1}</td><td style="text-align: center">{2}</td><td style="text-align: center">{3}</td></tr>'.format(d, t, s, u)
        f.write(row_html)

    # add final row
    f.write('<tr><td style="text-align: center; font-weight: bold">Average Sentiment</td><td colspan="3" style="text-align: center; font-weight: bold">{0}</td></tr>'.format(overall_sentiment_val_str))
    f.write('</table></html></body>')
    f.close()

else:
    ret_string = 'There are zero tweets returned in the last week from the query "{0}"'.format(query)
    arcpy.AddMessage(ret_string)
    arcpy.SetParameterAsText(1, ret_string)
