"""Mediawiki utils"""
import requests

__base_url = 'http://en.wikipedia.org/w/api.php'


def find_article(pageid):
    """
    :param pageid: integer
    :return: text of article - 1200 chars and its title
    """
    my_atts: dict = {}
    my_atts['action'] = 'query'
    my_atts['prop'] = 'extracts|info'
    my_atts['inprop'] = 'url|talkid'
    my_atts['exintro'] = 1
    my_atts['exchars'] = 1200
    my_atts['explaintext'] = 1
    # my_atts['redirects'] = 1 #
    my_atts['format'] = 'json'
    my_atts['pageids'] = [pageid]
    resp = requests.get(__base_url, params=my_atts)
    data = resp.json()
    article = data['query']['pages'][str(pageid)]
    return article['extract'], article['title'], article['canonicalurl']


def find_articles_list(key_word):
    """
    :param key_word: title of article
    :return: list of (id, title)
    """
    my_atts = {}
    my_atts['action'] = 'query'  # action=query
    my_atts['list'] = 'search'
    my_atts['format'] = 'json'  # format=json
    my_atts['srsearch'] = key_word
    my_atts['srlimit'] = 50 # default 10... for normal people 500, for bots 5000
    resp = requests.get(__base_url, params=my_atts)
    data = resp.json()['query']['search']  # extract from json
    print(resp.url)
    result = [(art['pageid'], art['title']) for art in data[:20]]  # get 20 from beginning
    return result
