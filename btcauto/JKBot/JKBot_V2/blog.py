import requests
client_id = "a89a65c5866a1b43e51d107c4fb2ef50"
seckey = "a89a65c5866a1b43e51d107c4fb2ef508bdc5fd7db3db49346ac9e5f9046dbbcd05a7173"
callback_url = "https://alphabot.tistory.com/"
# 등록시 입력 값
code = "6eecb40a28118b38071142673035db18fe9936edd2a6a1d55a8242ca14b64f91545ec96b"
token_url="https://www.tistory.com/oauth/access_token?client_id={0}&client_secret={1}&redirect_uri={2}&code={3}&grant_type=authorization_code".format(client_id, seckey, callback_url, code)
res = requests.get(token_url)
access_token = res.text.split("=")[1]
print(access_token) # 프린트 되는 값이 Acess Token !!