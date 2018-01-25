import requests
import re
import xlwt

def get_tag_attribute(attribute_name, tag_string):
    REGEX_PATTERN = attribute_name + '=(.*?')>'

    attribute = re.search( REGEX_PATTERN,tag_string)
    attribute_level = attribute.group(1)
    return(attribute_level)

def get_tag_content(tag_string,source):

    PATTERN = tag_string + '>(.*?)</' + tag_string
    tag_content = re.search(PATTERN, source)

data = requests.get('https://www.melon.com/chart/index.htm')
source = data.text

#---------------------------------------------------------------------

#name of the song
# <div class="ellipsis rank01> ~ </div>부분의 텍스트
PATTERN_DIV_RANK01 = re.compile(r'<div class="ellipsis rank01">.*?</div>', re.DOTALL)
# <a href=....>(내용)</a>
PATTERN_A_CONTENT = re.compile(r'<a.*?>(.*?)</a>')

titles = []
# 전체 문서에서 PATTERN_DIV_RANK01에 해당하는 match object목록을 순회
match_list = re.finditer(PATTERN_DIV_RANK01, source)
for match_div_rank01 in match_list:
    # 각 순회에서 매치된 전체 문자열 (<div clas... ~ </div>)부분을 가져옴
    div_rank01_content = match_div_rank01.group()

    # 부분 문자열에서 a태그의 내용을 title변수에 할당
    match_title = re.search(PATTERN_A_CONTENT, div_rank01_content)
    title = match_title.group(1)

    titles.append(title)

#---------------------------------------------------------------------
#rank
PATTERN_RANKING = re.compile(r'<span class="rank ">(.*?)</span>')

ranks=[]

match_ranking_list = re.finditer(PATTERN_RANKING,source)
for match_ranking in match_ranking_list:
    ranking_list = match_ranking.group(1)
    ranks.append(ranking_list)





#---------------------------------------------------------------------
#artist

PATTERN_ARTIST = re.compile(r'<div class="ellipsis rank02">.*?</div>', re.DOTALL)
PATTERN_ARTIST_NAME = re.compile(r'title="(.*?)\s')

names = []

match_artist_list = re.finditer(PATTERN_ARTIST, source)
for match_artist in match_artist_list:
    artist_name = re.search(PATTERN_ARTIST_NAME, match_artist.group())
    name = artist_name.group(1)
    names.append(name)

#------------------------------------------------------------------
#album

PATTERN_ALBUM = re.compile(r'<div class="ellipsis rank03">.*?</div>', re.DOTALL)
PATTERN_ALBUM_NAME = re.compile(r'title="(.*?)-')

albums =[]

match_album_list = re.finditer(PATTERN_ALBUM, source)
for match_album in match_album_list:
    album_name = re.search(PATTERN_ALBUM_NAME, match_album.group())
    album_real_name = album_name.group(1)
    albums.append(album_real_name)


#chart-----------------------------------------------------------------


chart = []


for rank,title,name,album in zip(ranks,titles,names,albums):

    components = {'rank': rank, 'title': title, 'artist': name, 'album': album}
    chart.append(components)



#save in excel-----------------------------------------------------------------


book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Rank")
sheet1.write(0, 1, "Title")
sheet1.write(0, 2, "Artist")
sheet1.write(0, 3, "Album")

for i in range(1,len(ranks)+1):
    sheet1.write(i,0,ranks[i-1])
    sheet1.write(i,1,titles[i-1])
    sheet1.write(i,2,names[i-1])
    sheet1.write(i,3,albums[i-1])


book.save("melonchart.xls")




