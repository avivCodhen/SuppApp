#!/bin/python2
import sys
from bs4 import BeautifulSoup
from urllib2 import quote, urlopen
from multiprocessing import Process, Queue # main async html req
#import json # res -> main
argv = sys.argv
reload(sys)  
sys.setdefaultencoding('utf8')

def dict_str(dic):
    'turns a dictionary to a beautiful string'
    s = '{\n'
    for key in dic:
        s = str(s)+'\t{} : {}\n'.format(key,dic[key])
    s += '}'
    return s

def tevabari_parsing(html):
    'parses the html of tevabari to products only'
    parsed_html = BeautifulSoup(html, "html5lib")
    products = parsed_html.find_all('div', attrs={'class':'productItem'})
    url = 'https://www.tevabari.co.il/'
    prods_txt = ""
    for prod in products:
        all_a = prod.find_all('a')
        prod_parsed = dict(title = all_a[0].get('title'),
                           link  = '{}{}'.format(url,all_a[0].get('href')),
                           img   = '{}{}'.format(url,prod.find('img').get('src')),
                           price = int(prod.find('span', attrs={'class':'priceNumber'}).string)
                           )
        prods_txt += dict_str(prod_parsed)+'\n'
    return prods_txt

def getHtml(url):
    'gets html of a url'
    return urlopen(url).read() #urllib2

def get_args():
    'returns the list of args as an (url) encoded string'
    args = reduce(lambda x,y: "{} {}".format(x,y),argv[1:])
    return quote(args.encode('utf8')) #encoding to utf8 - urllib2

def main():
    query = get_args() # ;print query
    
    # a dictionary of all of the sites with their parsing functions
    sites = [('https://www.tevabari.co.il/SearchResults.aspx?search={}', tevabari_parsing)
            ]
    
    # the result list of all of the items
    res = []
#    q = Queue()
    for site,func in sites:
        html = getHtml(site.format(query))
        res.append(func(html))
        '''
        p = Process(target=func, args=html)
        res.append(q.get())
        p.join()
        '''
    for x in res:
        print x

if __name__ == '__main__':
    main()
