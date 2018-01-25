
import os
import requests


def get_top100_list(refresh_html=False):
    """
    실시간 차트 1~100위의 리스트 반환
    파일위치:
        현재 파일(모듈)의 위치를 사용한 상위 디렉토리 경로 (crawler디렉토리):
            os.path.dirname(os.path.abspath(__name__))
        1~50위:   data/chart_realtime_50.html
        51~100위: data/chart_realtime_100.html
    :return:
    """
    # utils가 있는
    path_module = os.path.abspath(__name__)
    print(f'path_module: \n{path_module}')

    # 프로젝트 컨테이너 폴더 경로
    root_dir = os.path.dirname(path_module)
    print(f'root_dir: \n{root_dir}')

    # data/ 폴더 경로
    path_data_dir = os.path.join(root_dir, 'data')
    print(f'path_data_dir: \n{path_data_dir}')

    # 만약에 path_data_dir에 해당하는 폴더가 없을 경우 생성해준다
    os.makedirs(path_data_dir, exist_ok=True)

    # 1~50, 50~100위 웹페이지 주소
    url_chart_realtime_50 = 'https://www.melon.com/chart/index.htm'
    url_chart_realtime_100 = 'https://www.melon.com/chart/index.htm#params%5Bidx%5D=51'

    # 1~50위에 해당하는 웹페이지 HTML을
    # data/chart_realtime_50.html 에 저장
    # 'xt'모드와 try-except를 쓸 경우
    file_path = os.path.join(path_data_dir, 'chart_realtime_50.html')
    try:
        with open(file_path, 'xt') as f:
            response = requests.get(url_chart_realtime_50)
            source = response.text
            f.write(source)
    except FileExistsError:
        print(f'"{file_path}" file is already exists!')

    # 51~100위에 해당하는 웹페이지 HTML을
    # data/chart_realtime_100.html 에 저장
    # 파일이 있는 경우를 검사 후 로직 실행
    file_path = os.path.join(path_data_dir, 'chart_realtime_100.html')
    if not os.path.exists(file_path):
        response = requests.get(url_chart_realtime_100)
        source = response.text
        with open(file_path, 'wt') as f:
            f.write(source)
    else:
        print(f'"{file_path}" file is already exists!')

    # file_path = os.path.join(path_data_dir, 'abc.txt')
    # print(f'file_path: \n{file_path}')

    # result = []
    # for tr in soup.find_all('tr', class_='lst50'):
    #     rank = tr.find('span', class_='rank').text
    #     title = tr.find('div', class_='rank01').find('a').text
    #     artist = tr.find('div', class_='rank02').find('a').text
    #     album = tr.find('div', class_='rank03').find('a').text
    #     url_img_cover = tr.find('a', class_='image_typeAll').find('img').get('src')
    #     # http://cdnimg.melon.co.kr/cm/album/images/101/28/855/10128855_500.jpg/melon/resize/120/quality/80/optimize
    #     # .* -> 임의 문자의 최대 반복
    #     # \. -> '.' 문자
    #     # .*?/ -> '/'이 나오기 전까지의 최소 반복
    #     p = re.compile(r'(.*\..*?)/')
    #     url_img_cover = re.search(p, url_img_cover).group(1)
    #
    #     result.append({
    #         'rank': rank,
    #         'title': title,
    #         'url_img_cover': url_img_cover,
    #         'artist': artist,
    #         'album': album,
    #     })
    #