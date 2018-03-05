#!/usr/bin/env python3
# coding:utf8

import sys
import re
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


def searchWord(request, keyword):
    wordURL = 'https://dict.hjenglish.com/jp/jc/' + keyword

    wordPage = requests.get(wordURL, headers=headers, verify=False)
    htmlData = wordPage.text.encode("utf8")

    soup = BeautifulSoup(htmlData.decode("utf-8", "ignore"), "html.parser")

    try:
        wordList = []

        for word in soup.find_all("div", class_="word-details-pane"):

            try:
                chinese = word.find("h2").text.encode("utf8")
            except Exception as e:
                print(e)
                chinese = e

            # print(chinese)

            pronounceArray = word.findAll("span")

            try:
                realKana = pronounceArray[0].text.replace("[", "").replace("]", "").encode("utf8")
            except Exception as e:
                print(e)
                realKana = e

            # print(realKana)

            try:
                toneStr = pronounceArray[2].text
                if toneStr == '':
                    tune = []
                else:
                    tune = toneStr.split(unicode('或', "utf8"))
            except Exception as e:
                print(e)
                tune = []

            # print(tune)

            simpleArray = word.find_all("div", class_="simple")

            meanings = []
            nominal = ""

            for simples in simpleArray:
                try:
                    nominal = simples.find("h2").text.replace("【", "").replace("】", "").replace(" ", "").replace(
                        unicode("词", "utf-8"), "").encode("utf8")
                except Exception as e:
                    print(e)
                    nominal = ""

                pattern = {
                    unicode('形容'): unicode('形'),
                    unicode('形容动'): unicode('形動'),
                    unicode('连'): unicode('連'),
                    unicode('动'): unicode('動'),
                }

                for x in pattern:
                    nominal = re.sub(x, pattern[x], nominal)

                # print(nominal)

                try:
                    meaningUl = simples.find("ul")

                    for meaningLi in meaningUl.findAll("li"):
                        meanings.append(re.sub(r'[0-9]\.', "", meaningLi.text.replace(" ", "").replace("\n", "")))
                except Exception as e:
                    print(e)

                # print(meanings)

            wordList.append(
                {
                    "kana": realKana,
                    "chinese": chinese,
                    "meanings": [x.encode("utf8") for x in meanings],
                    "nominal": nominal,
                    "tune": [x.encode("utf8") for x in tune],
                }
            )

            # print(wordList)

        print(json.dumps(wordList, ensure_ascii=False))

        return HttpResponse(json.dumps(wordList, ensure_ascii=False))
    except Exception as e:
        return HttpResponse(e)
