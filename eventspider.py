import json
import urllib.request
from html.parser import HTMLParser
import string
import re

class BoardHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.list = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
           for name, value in attrs:
               if name == "href":
                   self.list.append(value)

class PostHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ''
    def handle_data(self, data):
        self.text += data

billboards = json.load(open('billboards.json'))

for billboard in billboards:
    req = urllib.request.Request(
        url = billboard["boardUrl"],
        data = None, 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    response = urllib.request.urlopen(req)
    data = response.read()
    text = data.decode('utf-8')
    parser = BoardHTMLParser()
    parser.feed(text)
    list2 = [x for x in parser.list if billboard["postUrl1"] in x]
    list3 = []
    for x in list2:
        list3.append(x.replace(billboard["postUrl1"], ''))
    list4 = []
    for x in list3:
        list4.append(x.replace(billboard["postUrl2"], ''))
    list5 = [x for x in list4 if int(x) > billboard["postNum"]]
    list6 = []
    for x in list5:
        list6.append(billboard["postUrl1"] + x + billboard["postUrl2"])
    if list6:
        billboard["postNum"] = int(list5[0])
    print(list6)
    for x in list6:
        req = urllib.request.Request(
            url = x,
            data = None, 
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        response = urllib.request.urlopen(req)
        data = response.read()
        text = data.decode('utf-8')
        parser = PostHTMLParser()
        parser.feed(text)
        RE = re.compile(r'主講人：', re.UNICODE)
        m = re.search(RE, parser.text)
        RE = re.compile(parser.text[m.end(0) : m.end(0)+3] + '*\\n', re.UNICODE)
        #RE = re.compile('\\n')
        #RE = re.compile(parser.text[m.end(0) : m.end(0)+3], re.UNICODE)
        m = re.search(RE, parser.text)
        #print(parser.text[m.end(0)+1 : m.end(0)+3] + '*\\n')
        #print(parser.text[m.end(0)+1 : m.end(0)+4])
        print(m.group(0))

json.dump(billboards, open('billboards.json', 'w+'))
