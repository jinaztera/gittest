import json
import requests

# with open("kakao_code.json", "r") as fp:
#     tokens = json.load(fp)


# url = "https://kapi.kakao.com/v1/api/talk/friends"  # 친구 목록 가져오기
# headers = {"Authorization": 'Bearer ' + "yW-NyTotXDaiLrFcBUWO3XWnoB7xHZoVX6_EuQo9c5sAAAF-OeWFrQ"}
#
# result = json.loads(requests.get(url, headers=headers).text)
# print(result.get("elements"))
# friends_list = result.get("elements")
def talk(message):

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    text = "코딩으로 카톡 메세지 보내기 프로젝트 성공"

    headers = {
        "authorization": "Bearer " + "X2o2vuhG69ts9XwBfIR985i9merTWuHP0_xnAwo9dVsAAAF-Rh6nRA"#tokens['access_token']
    }
    data = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": message,
            "link": {
                # "web_url": 'https://m.naver.com'
            }
        })
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)


#
# def talklist():
#
#     url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
#
#
#     headers = {
#         "authorization": "Bearer " + "trCyFy7nG-Ux-aVffnvncxxq1n_HgE-Q34qMjwopcJ8AAAF-OggQMg"#tokens['access_token']
#     }
#     template = {
#         "object_type": "list",
#         "header_title": "test header1",
#         "header_link":{
#             "web_url": "www.naver.com",
#             "mobile_web_url": "www.naver.com"
#         },
#         "contents": [
#             {
#                 "title": "TEST TITLE1",
#                 "description": "TEST DESC1",
#                 "link": {}
#              },
#             {
#                 "title": "TEST TITLE1",
#                 "description": "TEST DESC1",
#                 "link": {}
#             }
#
#         ]
#         }
#
#     response = requests.post(url, headers=headers, data=template)
#     print(response.status_code)
#
# talklist()