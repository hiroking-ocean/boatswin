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
wave =  { 'url' : 'https://weather.yahoo.co.jp/weather/wave/', 'preffix' : 'https://weather.yahoo.co.jp/weather/wave/?m=height&c=' }
wind =  { 'url' : 'https://weather.yahoo.co.jp/weather/wind/', 'preffix' : 'https://weather.yahoo.co.jp/weather/wind/?m=ground&c=' }
chart = { 'url' : 'https://weather.yahoo.co.jp/weather/chart/'}


#################### ダウンロードモジュールとスクレイピング ##################

def download_image(url_list, file_pass) :

  default_pass = os.path.join(os.path.dirname(__file__), '../app/assets/images/')

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

def get_image_url(pages_and_names):
  url_list = { 'img_url' : [], 'file_name' : [] }
  url_list['file_name'] = pages_and_names['file_name']
  for i,url in enumerate(pages_and_names['page_urls']):
    res = soup_gen(url)
    img_tag = res.find('td', class_='mainImg')
    url_list['img_url'].append(img_tag.find('img')['src'])
    time.sleep(1)
  return url_list

def page_urls(main_url):
  pages_and_names = { 'page_urls' : [], 'file_name' : [] }

  #　main_urlから個別の番号をを抽出する
  main_soup = soup_gen(main_url['url'])
  div_container = main_soup.find('div', class_='wavebg').find_all('option')
  for i,div in enumerate(div_container):
    pages_and_names['file_name'].append(div['value'])

  # url番号からページのurlを生成する
  for suffix in pages_and_names['file_name'] :
    pages_and_names['page_urls'].append(main_url['preffix'] + suffix)
  
  return pages_and_names

def wind_and_wave(urls):
  return get_image_url(page_urls(urls))



################ ここから関数呼び出し ########################

download_image(chart_url(chart), 'charts/')
download_image(wind_and_wave(wave),  'waves/')
download_image(wind_and_wave(wind),  'winds/')