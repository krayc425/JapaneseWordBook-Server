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

def searchWord(request, keyword):

    wordURL = 'http://dict.hjenglish.com/jp/jc/' + keyword
    wordPage = requests.get(wordURL, headers=headers)
    htmlData = wordPage.text

    soup = BeautifulSoup(htmlData, "html.parser")

    wordList = []

    try:
        for word in soup.find_all("div", id=re.compile("headword_jp_[0-9]*?")):
            try:
                realKana = re.findall(unicode(r'【(.*?)】', "utf8"), word.find("span", id=re.compile("kana_[0-9]*?")).text)[0]
            except:
                realKana = ''
            # print(realKana)
            try:
                chinese = word.find("span", id=re.compile("jpword_[0-9]*?")).text
            except:
                chinese = realKana
            # print(chinese)

            try:
                toneStr = word.find("span", class_="tone_jp").text
                if toneStr == '':
                    tone = []
                else:
                    tone = toneStr.split(unicode('或', "utf8"))
            except:
                tone = []
            # print(tone)
            try:
                nominal = re.findall(unicode("【?(.*?)】?词", "utf8"), word.find("div", class_="flag big_type tip_content_item").text)[0]
                # pattern = {'形容': '形',
                #            '形容动': '形動',
                #            re.compile('.*?连.*?'): '連',
                #            re.compile('.*?动.*?'): '動',
                #            re.compile('.*?助.*?'): '助'}
                # nominal = [unicode(pattern[x], 'utf8') if unicode(x, 'utf8') in pattern else unicode(x, 'utf8') for x in nominal]
            except:
                nominal = ''
            # print(nominal)
            try:
                meanings = [re.sub(unicode(r'(^（.*?）|（.*?）|。?（.*?）。?$|〔.*?〕)', 'utf8'), "", x.text) for x in word.find("ul", class_="tip_content_item jp_definition_com").find_all("span", class_= re.compile("(jp_explain|word_comment) soundmark_color"))]
            except:
                meanings = []

            try:
                sound = re.findall(r'GetTTSVoice\("(.*?)"\)', word.find("span", class_="jpSound").text)[0]
            except:
                sound = ''

            wordList.append({"kana" : realKana, "chinese" : chinese, "meanings" : meanings, "nominal" : nominal, "tune" : tone, "sound" : sound})

        return HttpResponse(json.dumps(wordList, ensure_ascii=False))
    except:
        return HttpResponse("Fail")