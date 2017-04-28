#!/usr/bin/env python3
#coding:utf-8

import sys
import re
import requests
from bs4 import BeautifulSoup
import json
import random
from django.http import HttpResponse

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

    wordURL = 'http://dict.hjenglish.com/app/jp/sent/' + keyword
    wordPage = requests.get(wordURL, headers=headers)
    htmlData = wordPage.text

    soup = BeautifulSoup(htmlData, "html.parser")

    sentenceList = []
    try:
        tempList = soup.find("div", class_="mian_container").find("ul", class_="search_result").find_all("li")

        for x in tempList:
            sentenceContent = re.sub(unicode("（|）", "utf8"), "", x.find("span", class_="en_sentence").text)
            sentenceSound = r'http://tts.yeshj.com/c/jp/s/?w=' + re.findall(r'getSentenceSound\("jp", "(.*?)"\)', x.text)[0]
            sentenceMeaning = re.sub('\.', unicode("。", "utf8"), x.find("span", class_="big").text)

            sentenceList.append({"content" : sentenceContent, "sound" : sentenceSound, "meaning" : sentenceMeaning})

        return HttpResponse(json.dumps(sentenceList, ensure_ascii=False))
    except:
        print("Fail")
        return HttpResponse("Fail")

# keyword = "自分"
# keyword = sys.argv[1]
# wordSentence(keyword)