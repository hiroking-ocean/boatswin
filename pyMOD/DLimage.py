import os
import sys
import shutil
import time
import datetime
import requests
import re
from bs4 import BeautifulSoup


# ユーザーエージェントの指定
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
      'AppleWebKit/537.36 (KHTML, like Gecko) '\
        'Chrome/81.0.4044.129 Safari/537.36'}

# ページのurl
wave =  { 'url' : 'https://weather.yahoo.co.jp/weather/wave/'}
wind =  { 'url' : 'https://weather.yahoo.co.jp/weather/wind/'}
chart = { 'url' : 'https://weather.yahoo.co.jp/weather/chart/'}


#################### ダウンロードモジュールとスクレイピング ##################

def download_image(url_list, file_pass) :
  # url_listにimage_url(画像のダウンロードURL）、file_name（ファイルの名前）を格納
  # file_passにダウンロード先のファイルパスを指定

  default_pass = os.path.join(os.path.dirname(__file__), '../app/assets/images/')
  # defalt_passは保存先のルートパス

  # 保存先のファイルパスを生成し、過去のものを削除する。
  pas = default_pass + file_pass
  shutil.rmtree(pas, True)
  os.makedirs(pas, exist_ok=True)


  for i,url in enumerate(url_list['img_url']):
    cont_img = requests.get(url, headers=ua, allow_redirects=False, timeout=100)
    with open(pas + url_list['file_name'][i] + '.jpg', 'wb') as f:
      f.write(cont_img.content)
      print(url + '\n => ' + pas + url_list['file_name'][i])
      time.sleep(5)


def soup_gen(url, referer=None):
  # beautiful soupを使って、urlからlxmlを生成する。
  req = requests.get(url, headers=ua)
  return BeautifulSoup(req.text, 'lxml')



################## 天気図のスクレイピング #################

def chart_url(url):
  url_list = { 'img_url' : [], 'file_name' : [] }
  req_soup = soup_gen(url['url'])
  img_urls = req_soup.find_all('div', class_='tabView_content')
  now_year = datetime.datetime.now().year
  pre_filename = []
  for i,url in enumerate(img_urls):
    img_url = url.find('img')['src']
    url_list['img_url'].append(img_url)

    # 時間情報がバラバラなので仕方なく作る
    ls = []
    for x in re.findall(r'\d+', url.find('img')['alt']):
      ls.append('{:02}'.format(int(x)))
    a = ''.join(ls)
    if a != '':
      pre_filename.append(datetime.datetime.strptime(a, '%m%d%H').replace(year=now_year))
    else:
      pre_filename.append('')

  delta = datetime.timedelta(hours=12)
  pre_filename[0] = pre_filename[1] - delta
  for n in pre_filename:
    url_list['file_name'].append(n.strftime('%Y%m%d%H'))
    
  return url_list



##################　波高および風力　#######################

# url_list配列に、画像の番号とぺーじURLを入れて返す
def weather_urls(main_url):
  url_list = { 'img_url' : [], 'file_name' : [] }

  #　div_containerに、該当するimgタグを格納する
  main_soup = soup_gen(main_url['url'])
  div_container = main_soup.find('ul', class_='imgList').find_all('img')

  # url_listのimg_urlに画像のURLを格納する。
  for i,div in enumerate(div_container):
    url_list['img_url'].append(div['data-lazyload-src'])

  # urlからファイルネームを格納する
  for url in url_list['img_url'] :
    url_list['file_name'].append(url[80:90])
    print(url[80:90])
  
  return url_list


################ ここから関数呼び出し ########################

download_image(chart_url(chart), 'charts/')
download_image(weather_urls(wave),  'waves/')
download_image(weather_urls(wind),  'winds/')