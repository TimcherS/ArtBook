# from body2 import get_token
# import ProjectVariables

# AUTH = ProjectVariables.AuthData
# TOKEN = get_token(AUTH).json()['access_token']

# import requests
# import json

# url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'

# payload = json.dumps({
#     "model": "GigaChat",
#     "messages": [
#     {
#         "role": "user",
#         "content": f"Нарисуй милого и дружелюбного динозавра"
#     }
#     ],
#     "function_call": "auto"
# })

# headers = {
#     'Content-Type': 'application/json',
#     'Accept': 'application/json',
#     'Authorization': f'Bearer {TOKEN}'
# }

# response = requests.request("POST", url, headers=headers, data=payload, verify=False)
# img_id = response.json()['choices'][-1]['message']['content']
# print(img_id)
# # import BeautifulSoup
# # soup = BeautifulSoup(response_img_tag, 'html.parser')
# # img_id = soup.img['src']
# # img_id = img_id[img_id.find('<img src="') + len('<img src="') : img_id.find('" fuse=')]
# print(img_id)

# url2 = f"https://gigachat.devices.sberbank.ru/api/v1/files/{img_id}/content"

# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {TOKEN}'
# }

# response = requests.request("GET", url2, headers=headers, verify=False)
# with open('images/image1.jpg', 'wb') as out_file:
#     out_file.write(response.content)


# from os import makedirs
# makedirs('images/poorfolks')
# with open('images/poorfolks/img1.jpg', 'wb'):
#     print('Hello')

# path = 'C:/ML/Projects/Opus-illustro/books/Бедные люди.txt'
# books_name = path.split('/')[-1]
# print(books_name)

from body2 import generate_image
from body2 import get_models
import requests
from body2 import get_token
import ProjectVariables

AUTH = ProjectVariables.AuthData
TOKEN = get_token(AUTH).json()['access_token']

prompt = 'нарисуй незнайку, на картинке не должно быть текста'
generate_image(TOKEN, prompt, 'images/nezn' )

# imgen_prompt = '''\
# Нарисуй следующую сценку словно это - книжная иллюстрация: {}
# Её действующими лицами могут являться следующие персонажи: \n\
# '''
# print(imgen_prompt.format("Тимофей"))