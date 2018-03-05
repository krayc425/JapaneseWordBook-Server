#!/usr/bin/env python3
# coding:utf-8

import sys
import requests
from bs4 import BeautifulSoup
import json
import random
from django.http import HttpResponse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

reload(sys)
sys.setdefaultencoding('utf8')

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

agents = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
]

headers = {
    'User-Agent': random.choice(agents)
}


def wordSentence(request, keyword):
    wordURL = 'https://dict.hjenglish.com/jp/jc/' + keyword

    wordPage = requests.get(wordURL, headers=headers, verify=False)
    htmlData = wordPage.text.encode("utf8")

    soup = BeautifulSoup(htmlData.decode("utf-8", "ignore"), "html.parser")

    sentenceList = []
    try:
        fromList = soup.find_all("p", class_="def-sentence-from")
        sentenceContentList = [x.text.strip() for x in fromList]
        sentenceSoundList = [x.span["data-src"] for x in fromList]
        toList = soup.find_all("p", class_="def-sentence-to")
        sentenceMeaningList = [x.text.strip() for x in toList]

        for i in range(len(sentenceContentList)):
            sentenceList.append(
                {"content": sentenceContentList[i], "sound": sentenceSoundList[i], "meaning": sentenceMeaningList[i]})

        print(json.dumps(sentenceList))

        return HttpResponse(
            json.dumps(sentenceList, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(e)
