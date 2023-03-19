import socket
import requests
import json
from bs4 import BeautifulSoup
# import app_config
# import utils


url_post = "https://www.tistory.com/apis/post/write"
access_token='44e41f71379970d962ef7e6c89554d4f_964b9d7af376a84cda8a191d75aea4bf'
# &output={output-type}
blogName = "https://alphabot.tistory.com/"
title = "테스트"
content = "테스트"
visibility = 0
category = 1073539
published = ""
slogan = ""
tag = '시스템 트레이딩'
acceptComment = 1
password = ""

headers = {'Content-Type': 'application/json; charset=utf-8'}

params = {
  'access_token': access_token,
  'output': 'json',
  'blogName': blogName,
  'title': title,
  'content': content,
  'visibility': visibility,
  'category': category,
  'published': published,
  'slogan': slogan,
  'tag': tag,
  'acceptComment': acceptComment,
  'password': password
}
data = json.dumps(params)

rw = requests.post(url_post, headers=headers, data=data)
if rw.status_code == 200:
  print('ok')
else:
  print('fail')


#
# import requests
#
# appid = ""
# access_token = ""
# callback_url = ""
# blogName = ""
#
#
# def list_of_Category():
#   url = "https://www.tistory.com/apis/category/list"
#
#   params = {
#     'access_token': '44e41f71379970d962ef7e6c89554d4f_964b9d7af376a84cda8a191d75aea4bf',
#     'output': 'json',  # json, xml 두 가지 형식 지원
#     'blogName': "https://alphabot.tistory.com/"  # ().tistory.com 또는 블로그 주소 전체
#   }
#
#   res = requests.get(url, params=params)
#   print(res.status_code)
#
#   if res.status_code == 200:
#     res_json = res.json()
#     print(res_json)
#
#
# if __name__ == '__main__':
#   list_of_Category()

def blog_upload(blog_name, uploadedfile_path):
  '''
      POST https://www.tistory.com/apis/post/attach?
      access_token={access-token}
      &blogName={blog-name}
      [uploadedfile]
      blogName: Blog Name 입니다.
      uploadedfile: 업로드할 파일 (multipart/form-data)
  '''
  files = {"uploadedfile": open(uploadedfile_path, 'rb')}
  url = 'https://www.tistory.com/apis/post/attach'
  data = {'access_token': access_token, 'blogName': blog_name}
  res = requests.post(url, params=data, files=files)
  print(res.url)
  if res.status_code == 200:
    print(res.text)

    # 업로드된 URL 주소
    soup = BeautifulSoup(res.text, 'lxml')
    url = soup.select_one('url')
    print(url.text)

    write_json_file('blog_upload_' + blog_name + '_' + uploadedfile_path + '.txt', url.text)
  else:
    json_result, json_text = json_parsing(res.text)
    print(json_text)