import requests
import re

data = requests.get('https://www.melon.com/chart/index.htm')
source = data.text


PATTERN_IMAGE = re.compile('<td.*?>.*?</td>', re.DOTALL)

td_list = re.findall(PATTERN_IMAGE, source,)

for a in td_list:
    td_strip = re.sub(r'[\n\t]+', '', a)
    print(td_strip)


td_title_author = td_list[5]
PATTERN_IMG = re.compile(r'<img.*?src="(.*?)".*?>',re.DOTALL)
PATTERN_A_CONTENT = re.compile(r)