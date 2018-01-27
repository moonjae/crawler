
import os
import re
import requests
from bs4 import BeautifulSoup, NavigableString

# utils가 있는
PATH_MODULE = os.path.abspath(__file__)

# 프로젝트 컨테이너 폴더 경로
ROOT_DIR = os.path.dirname(os.path.dirname(PATH_MODULE))

# data/ 폴더 경로
DATA_DIR = os.path.join(ROOT_DIR, 'data')

print(PATH_MODULE)
print(ROOT_DIR)
print(DATA_DIR)


class MelonCrawler:
    def search_song(self, q):
        """
        곡 명으로 멜론에서 검색한 결과 리스트를 리턴
        :param q: 검색할 곡 명
        :return: 결과 dict리스트
        """
        """
        1. http://www.melon.com/search/song/index.htm
            에 q={q}, section=song으로 parameter를 준 URL에
            requests를 사용해 요청
        2. response.text를 사용해 BeautifulSoup인스턴스 soup생성
        3. soup에서 적절히 결과를 가공
        4. 결과 1개당 Song인스턴스 한개씩
        5. 전부 리스트에 넣어 반환
        6. 완☆성
        """
        url = 'https://www.melon.com/search/song/index.htm'
        params = {
            'q': q,
            'section': 'song',
        }
        response = requests.get(url, params)
        soup = BeautifulSoup(response.text, 'lxml')
        tr_list = soup.select('form#frm_defaultList table > tbody > tr')
        # tr_list = soup.find('form', id='frm_defaultList').find('table').find('tbody').find_all('tr')

        result = []
        for tr in tr_list:
            # <a href="javascript:searchLog('web_song','SONG','SO','빨간맛','30512671');melon.play.playSong('26020103',30512671);" class="fc_gray" title="빨간 맛 (Red Flavor)">빨간 맛 (Red Flavor)</a>
            # song_id = re.search(r"searchLog\(.*'(\d+)'\)", tr.select_one('td:nth-of-type(3) a.fc_gray').get('href')).group(1)
            song_id = tr.select_one('td:nth-of-type(1) input[type=checkbox]').get('value')
            title = tr.select_one('td:nth-of-type(3) a.fc_gray').get_text(strip=True)
            artist = tr.select_one('td:nth-of-type(4) span.checkEllipsisSongdefaultList').get_text(
                strip=True)
            album = tr.select_one('td:nth-of-type(5) a').get_text(strip=True)

            song = Song(song_id=song_id, title=title, artist=artist, album=album)
            result.append(song)
        return result


    def search_artist(self, q):
        url = ' https://www.melon.com/search/artist/index.htm'
        params = {'q': q }
        response = requests.get(url,params)
        soup = BeautifulSoup(response.text, 'lxml')

        PATTERN_ARTIST_NAME = re.compile('(.*?)\s-')
        PATTERN_ARTIST_ID = re.compile("goArtistDetail\('(.*?)'\)")




        artist_info_list = soup.find_all('div', class_='atist_info')
        for artist_info in artist_info_list:
            artist_name_match = re.search(PATTERN_ARTIST_NAME, artist_info.a['title'])

            artist_name = artist_name_match.group(1)


            artist_id_one = artist_info.a['href']
            artist_id_match = re.search(PATTERN_ARTIST_ID, artist_id_one)
            artist_id = artist_id_match.group(1)


            gen_info = artist_info.find('dd', class_='gubun').text.strip()


            genre_iter = artist_info.find('div', class_='ellipsis fc_strong').contents
            genre_list = []

            for a in genre_iter:
                if a != '\n' and a !=', ':
                    genre_list.append(a.text)
            pass
    """
    아티스트 검색
    http://www.melon.com/search/artist/index.htm?q=%EC%95%84%EC%9D%B4%EC%9C%A0&section=&searchGnbYn=Y&kkoSpl=N&kkoDpType=&ipath=srch_form
    검색 결과를
    def search_artist(q):
        return class Artist의 목록
    아티스트 상세 정보
    http://www.melon.com/artist/detail.htm?artistId=261143
    artist_detail_{artist_id}.html
    Artist의 인스턴스 메서드
        def get_detail(self)
            return 없이 자신의 속성 채우기
    아티스트의 곡
    http://www.melon.com/artist/song.htm?artistId=261143
    Artist의 인스턴스 메서드
        def get_songs(self)
            return Song의 list
    """

class Artist:
    def __init__(self, artist_id, name, genre):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.__debut = ''
        self.__agency = ''
        self.__awards = ''
        self.__solo_or_group = ''
        self.__birthday = ''


    def get_songs(self, refresh_html = False):

        no_songs = 0
        file_path = os.path.join(DATA_DIR, f'artist_songlist_{self.artist_id}.html')
        try:

            file_mode = 'wt' if refresh_html else'xt'
            with open(file_path, file_mode) as f:
                no_songs_url = 'https://www.melon.com/artist/song.htm?' + 'artistId=' + self.artist_id + '#params%5BartistId%5D=' + self.artist_id + '&po=pageObj&startIndex=' + '1'
                no_songs_response = requests.get(no_songs_url)

                no_songs_source = no_songs_response.text
                soup = BeautifulSoup(no_songs_source, 'lxml')
                PATTERN_NO_SONGS = re.compile('\((.*?)\)')
                a = soup.find('div', class_="wrap_sort fl_left").find('a', class_="ico_radio on")
                match_no_songs = re.search(PATTERN_NO_SONGS, str(a))
                no_songs = int(match_no_songs.group(1))


                file_length = f.write(no_songs_source)
                if file_length < 10:
                    raise ValueError('파일이 너무 짧습니다')

        except FileExistsError:
            print(f'"{file_path}" file  already exists!')
        except ValueError:
            # 파일이 너무 짧은 경우
            os.remove(file_path)

        # remainder = no_songs % 50
        # how_many_requests = 0
        # if remainder != 0:
        #     how_many_requests = int(no_songs / 50) + 1
        # else:
        #     how_many_requests = int(no_songs / 50)
        #
        # if how_many_requests >1:
        #
        #     # for a in range(1,how_many_requests):
        #     f = open(file_path, 'at')
        #     # start_index_str = str(50 * a +1)
        #     # url1 = 'https://www.melon.com/artist/song.htm?' + 'artistId=' + self.artist_id + '#params%5BartistId%5D=' + self.artist_id + '&po=pageObj&startIndex=' + '101'
        #     url1 = 'https://www.melon.com/artist/song.htm?artistId=261143#params%5BlistType%5D=A&params%5BorderBy%5D=ISSUE_DATE&params%5BartistId%5D=261143&po=pageObj&startIndex=51'
        #     response1 = requests.get(url1)
        #     source1 = response1.text
        #     print(source1)
        #     f.write(source1)
        #     f.close()


        source = open(file_path, 'rt').read()
        soup = BeautifulSoup(source, 'lxml')

        song_list = []
        tr_list = soup.tbody.find_all('tr')
        for tr in tr_list:
            component = tr.find('a', class_="fc_gray").text
            song_list.append(component)
        return song_list

    def get_detail(self, refresh_html= False):

        file_path = os.path.join(DATA_DIR, f'artist_detail_{self.artist_id}.html')
        try:

            file_mode =  'wt' if refresh_html else'xt'
            with open(file_path, file_mode) as f:
                # url과 parameter구분해서 requests사용
                url = f'https://www.melon.com/artist/detail.htm'
                params = {
                    'artistId': self.artist_id,
                }
                response = requests.get(url, params)

                source = response.text
                # 만약 받은 파일의 길이가 지나치게 짧을 경우 예외를 일으키고
                # 예외 블럭에서 기록한 파일을 삭제하도록 함

                file_length = f.write(source)
                if file_length < 10:
                    raise ValueError('파일이 너무 짧습니다')

        except FileExistsError:
            print(f'"{file_path}" file  already exists!')
        except ValueError:
            # 파일이 너무 짧은 경우
            os.remove(file_path)


        source = open(file_path, 'rt').read()
        soup = BeautifulSoup(source, 'lxml')


        PATTERN_NEW_LINE = re.compile('(.*?)\n')
        info = soup.find('div', class_="dtl_atist clfix").find('dl', class_= "atist_info clfix").text
        info_list = re.findall(PATTERN_NEW_LINE, info)

        info_list_refined = []

        for a in info_list:
            if a != '' and a !='더보기':
                info_list_refined.append(a.strip())

        if int(len(info_list_refined) % 2) != 0:
            info_list_refined[1:3] = [''.join(info_list_refined[1:3])]

        info_dict_original = {}
        range_list = range(len(info_list_refined))
        iterable_list = iter(range_list)

        for  a in range(int(len(info_list_refined)/2)):
            info_dict_original[info_list_refined[next(iterable_list)]] = info_list_refined[next(iterable_list)]
        info_dict_refined = dict((v, k) for k, v in info_dict_original.items())

        self.__debut = info_dict_refined['데뷔']
        self.__birthday = info_dict_refined['생일']
        self.__solo_or_group = info_dict_refined['활동유형']
        self.__agency = info_dict_refined['소속사']
        self.__awards = info_dict_refined['수상이력']


    def __str__(self):
       return f'{self.name} 아티스트 id: {self.artist_id}, 장르: {self.genre}, 데뷔일: {self.__debut}, 소속사 {self.__agency}, 활동유형: {self.__solo_or_group}'













class Song:
    def __init__(self, song_id, title, artist, album):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.album = album

        self._release_date = None
        self._lyrics = None
        self._genre = None
        self._producers = None

    def __str__(self):
        return f'{self.title} (아티스트: {self.artist}, 앨범: {self.album})'

    def get_detail(self, refresh_html=False):
        """
        자신의 _release_date, _lyrics, _genre, _producers를 채운다
        :return:
        """
        # 파일위치는 data/song_detail_{song_id}.html
        file_path = os.path.join(DATA_DIR, f'song_detail_{self.song_id}.html')
        try:
            file_mode = 'wt' if refresh_html else 'xt'
            with open(file_path, file_mode) as f:
                # url과 parameter구분해서 requests사용
                url = f'https://www.melon.com/song/detail.htm'
                params = {
                    'songId': self.song_id,
                }
                response = requests.get(url, params)
                source = response.text
                # 만약 받은 파일의 길이가 지나치게 짧을 경우 예외를 일으키고
                # 예외 블럭에서 기록한 파일을 삭제하도록 함
                file_length = f.write(source)
                if file_length < 10:
                    raise ValueError('파일이 너무 짧습니다')
        except FileExistsError:
            print(f'"{file_path}" file is already exists!')
        except ValueError:
            # 파일이 너무 짧은 경우
            os.remove(file_path)
            return

        source = open(file_path, 'rt').read()
        soup = BeautifulSoup(source, 'lxml')
        # div.song_name의 자식 strong요소의 바로 다음 형제요소의 값을 양쪽 여백을 모두 잘라낸다
        # 아래의 HTML과 같은 구조
        # <div class="song_name">
        #   <strong>곡명</strong>
        #
        #              Heart Shaker
        # </div>
        div_entry = soup.find('div', class_='entry')
        title = div_entry.find('div', class_='song_name').strong.next_sibling.strip()
        artist = div_entry.find('div', class_='artist').get_text(strip=True)
        # 앨범, 발매일, 장르...에 대한 Description list
        dl = div_entry.find('div', class_='meta').find('dl')
        # isinstance(인스턴스, 클래스(타입))
        # items = ['앨범', '앨범명', '발매일', '발매일값', '장르', '장르값']
        items = [item.get_text(strip=True) for item in dl.contents if not isinstance(item, str)]
        it = iter(items)
        description_dict = dict(zip(it, it))

        album = description_dict.get('앨범')
        release_date = description_dict.get('발매일')
        genre = description_dict.get('장르')

        div_lyrics = soup.find('div', id='d_video_summary')

        lyrics_list = []
        for item in div_lyrics:
            if item.name == 'br':
                lyrics_list.append('\n')
            elif type(item) is NavigableString:
                lyrics_list.append(item.strip())
        lyrics = ''.join(lyrics_list)

        # 리턴하지말고 데이터들을 자신의 속성으로 할당
        self.title = title
        self.artist = artist
        self.album = album
        self._release_date = release_date
        self._genre = genre
        self._lyrics = lyrics
        self._producers = {}

    @property
    def lyrics(self):
        # 만약 가지고 있는 가사정보가 없다면
        if not self._lyrics:
            # 받아와서 할당
            self.get_detail()
        # 그리고 가사정보 출력
        return self._lyrics


