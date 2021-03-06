## Twitter API only provides the latest 3k statuses
## this script allows us to go deeper into Twitter history by using
## their website

import requests
import bs4
import re
import datetime

from common import *

import time

match_id = '.*/([0-9]+)'

def _collect_ids( username , date ):

    date2 = date + datetime.timedelta( 1 )

    url = 'https://mobile.twitter.com/search?src=typd&q=from:' + username + ' since:' + date.isoformat() + ' until:' + date2.isoformat()

    ret = []

    while True:

        r = requests.get( url )

        page = bs4.BeautifulSoup( r.text )

        count = 0

        if not page.find( class_ ='timeline' ):
	    break

        for tweet in page.find( class_ ='timeline' ).children:

	   if isinstance( tweet , bs4.Tag ):

         	## get tweet ID
                if 'href' in tweet.attrs:
                    href = tweet['href']
                    href = re.search( match_id, href )
                    ret.append( (int)( href.group(1) ) )
                    count += 1

        if count < 20: ## per page, max 20 tweets
            break

        ## move to next page
        url = 'https://mobile.twitter.com/' + page.find( class_ = 'w-button-more' ).find('a')['href']

    print username, date, len( ret )

    return tweets( ret )

def collect_tweets( username, since, until ):

    date = since

    tweets = []

    while date <= until:

        tweets += _collect_ids( username, date )

        date = date + datetime.timedelta( 1 )

    return tweets

if __name__ == '__main__':
    for t in collect_tweets( 'alexstubb', datetime.date( 2011, 4, 16 ), datetime.date( 2011, 4, 29 ) ):
        print t['text'].encode('utf8')
