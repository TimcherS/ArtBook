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

# from body2 import generate_image
# from body2 import get_models
# import requests
# from body2 import get_token
# import ProjectVariables

# AUTH = ProjectVariables.AuthData
# TOKEN = get_token(AUTH).json()['access_token']

# prompt = 'нарисуй незнайку, на картинке не должно быть текста'
# generate_image(TOKEN, prompt, 'images/nezn' )

# imgen_prompt = '''\
# Нарисуй следующую сценку словно это - книжная иллюстрация: {}
# Её действующими лицами могут являться следующие персонажи: \n\
# '''
# print(imgen_prompt.format("Тимофей"))

# from body2 import current_styles
# st = current_styles()
# print(st)

import json
import time
import base64
import os
import requests
from random import randint

# class Text2ImageAPI:

#     def __init__(self, url, api_key, secret_key):
#         self.URL = url
#         self.AUTH_HEADERS = {
#             'X-Key': f'Key {api_key}',
#             'X-Secret': f'Secret {secret_key}',
#         }

#     def get_model(self):
#         response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
#         data = response.json()
#         return data[0]['id']

#     def generate(self, prompt, model, images=1, width=1024, height=1024):
#         params = {
#             "type": "GENERATE",
#             "numImages": images,
#             "width": width,
#             "height": height,
#             "generateParams": {
#                 "query": f"{prompt}"
#             }
#         }

#         data = {
#             'model_id': (None, model),
#             'params': (None, json.dumps(params), 'application/json')
#         }
#         try:
#             response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
#             data = response.json()
#             return data['uuid']
#         except requests.RequestException:
#             print('Unable to generate image from Kandinsky from ')

#     def check_generation(self, request_id, attempts=10, delay=10):
#         while attempts > 0:
#             response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
#             data = response.json()
#             if data['status'] == 'DONE':
#                 return data['images']

#             attempts -= 1
#             time.sleep(delay)

# def gen(prom, dirr = "res"):
#     api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '7AD209E3ADF41E7F7BDDA514A0965FCF', 'A556531C4D652E569260D66F32436512')
#     model_id = api.get_model()
#     uuid = api.generate(prom, model_id)
#     images = api.check_generation(uuid)    

#     # Здесь image_base64 - это строка с данными изображения в формате base64
#     image_base64 = images[0]

#     # Декодируем строку base64 в бинарные данные
#     image_data = base64.b64decode(image_base64)

#     # Открываем файл для записи бинарных данных изображения
#     try:
#         with open(f"{dirr}/{prom.split('.')[0]} _ {randint(0, 100000)}.jpg", "wb") as file:
#             file.write(image_data)
#     except:
#         with open(f"{dirr}/{prom.split('.')[0]} _ {randint(0, 100000)}.jpg", "w+") as file:
#             file.write(image_data)

# while 1:
#     i = input("prompt: ")
    
#     try:
#         os.mkdir(os.getcwd().replace("\\", "/") + f'/' + i.replace("\n", " ").split(".")[0])
#     except FileExistsError:
#         print('exist')
            
#     for j in range(4):
#         gen(i.replace("\n", " "), i.replace("\n", " ").split(".")[0])
#         print(f"сделано {j+1}")

    
#     print("завершено")

from APIs import KandinskyAPI
import ProjectVariables

url = 'https://api-key.fusionbrain.ai/'
api = KandinskyAPI(url, ProjectVariables.KandinskyAPIKey, ProjectVariables.KandinskySecretKey)
api.generate_image('Нарисуй лунных котов', 'images', '1')

