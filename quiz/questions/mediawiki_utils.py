"""Mediawiki utils"""
import requests

__base_url = 'http://en.wikipedia.org/w/api.php'
__pageviews_url = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/'


def find_article(pageid):
    """
    :param pageid: integer
    :return: text of article - 1200 chars and its title
    """
    my_atts: dict = {'action': 'query',
                     'prop': 'extracts|info',
                     'inprop': 'url|talkid',
                     'exintro': 1,
                     'exchars': 1200,
                     'explaintext': 1,
                     'format': 'json',
                     'pageids': [pageid]}
    # my_atts['redirects'] = 1 #
    resp = requests.get(__base_url, params=my_atts)
    data = resp.json()
    article = data['query']['pages'][str(pageid)]
    return article['extract'], article['title'], article['canonicalurl']


def find_articles_list(key_word):
    """
    :param key_word: title of article
    :return: list of (id, title)
    """
    my_atts = {'action': 'query',  # action=query
               'list': 'search',
               'format': 'json',  # format=json
               'srsearch': key_word,
               'srlimit': 50  # default 10... for normal people 500, for bots 5000
               }
    resp = requests.get(__base_url, params=my_atts)
    data = resp.json()['query']['search']  # extract from json
    result = [(art['pageid'], art['title']) for art in data[:20]]  # get 20 from beginning
    return result


def get_article_and_views(pageid, year, month):
    """Find views per month of given article"""
    _, title, source_url = find_article(pageid)
    request_url = __pageviews_url + "per-article/en.wikipedia/all-access/all-agents/" \
                  + title + "/monthly/" + str(year) + str(month).zfill(2) + "0100/" \
                  + str(year) + str(month + 1).zfill(2) + "0100"
    resp = requests.get(request_url)
    data = resp.json()['items'][0]
    return title, data['views'], source_url
