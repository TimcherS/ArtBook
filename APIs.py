import requests
import json
import uuid
import base64
import io
import time

class GigachatAPI:
    
  def __init__(self, AUTH, style):
      self.scope = 'GIGACHAT_API_PERS'
      self.model = 'GigaChat-Pro'
      self.style = style
      self.AUTH = AUTH
      self.TOKEN = self.get_token(self.AUTH).json()['access_token']

  def get_token(self, auth_token):
      rq_uid = str(uuid.uuid4())
      url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
      headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'RqUID': rq_uid,
          'Authorization': f'Basic {auth_token}'
      }
      payload = {
          'scope': self.scope
      }
      try:
          response = requests.post(url, headers=headers, data=payload, verify=False)
          return response
      except requests.RequestException as e:
          print(f'Ошибка при получении токена: {str(e)}')
          return -1
      
  def get_models(self):
      url = "https://gigachat.devices.sberbank.ru/api/v1/models"
      payload={}
      headers = {
          'Accept': 'application/json',
          'Authorization': f'Bearer {self.TOKEN}'
      }
      response = requests.request("GET", url, headers=headers, data=payload, verify=False)
      return response.json()
        
  def send_message(self, prompt, system_prompt=''):
      url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

      payload = json.dumps({
      "model": f"{self.model}",
      "messages": [
          {
          "role": "system",
          "content": f"{system_prompt}"
          },
          {
          "role": "user",
          "content": f"{prompt}"
          }
      ],
      "n": 1,
      "stream": False,
      "update_interval": 0
      })

      headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': f'Bearer {self.TOKEN}'
      }
      try:
          response = requests.request("POST", url, headers=headers, data=payload, verify=False)
          return response.json()['choices'][-1]['message']['content']    
      except requests.RequestException as e:
          print(f'Ошибка с получением ответа на запрос: {str(e)}')
          return -1
        
  def generate_image(self, prompt, dir, style='KANDINSKY', width=640, height=480):
    gen_url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
      
    payload = json.dumps({
        'model': f'{self.model}',
        'style': f'{style}',
        'width': f'{width}',
        'height': f'{height}',
        'messages': [
        {
            'role': 'user',
            'content': f'{prompt}'
        }
        ],
        'function_call': 'auto'
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {self.TOKEN}'
    }

    response = requests.request("POST", gen_url, headers=headers, data=payload, verify=False)
    img_id = response.json()['choices'][-1]['message']['content']
    img_id = img_id[img_id.find('<img src="') + len('<img src="') : img_id.find('" fuse=')]

    dwnld_url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{img_id}/content"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.TOKEN}'
    }

    response = requests.request("GET", dwnld_url, headers=headers, verify=False)
    with io.open(f'{dir}.jpg', mode='wb') as out_file:
        out_file.write(response.content)

class KandinskyAPI:
    
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS, verify=False)
        data = response.json()
        return data[0]['id']
    
    def get_styles():
        url = 'https://cdn.fusionbrain.ai/static/styles/api'
        response = requests.request('GET', url, verify=False)
        return [model['name'] for model in response.json()]
    
    def generate(self, prompt, model, style, width, height):
        params = {
            'type': 'GENERATE',
            'style': style,
            'width': width,
            'height': height,
            'numImages': 1,
            'negativePromptUnclip': 'текст, кислотность',
            'generateParams': {
                'query': f'{prompt}',
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        try:
            response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data, verify=False)
            data = response.json()
            print(data)
            return data['uuid']
        except requests.RequestException:
            print(f'Unable to generate image from Kandinsky with this prompt: {prompt}')
            print(data)
    
    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS, verify=False)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def generate_image(self, prompt, save_dir, img_name, style, width=1024, height=1024):
      model_id = self.get_model()
      uuid = self.generate(prompt, model_id, style, width, height)
      images = self.check_generation(uuid)    

      image_base64 = images[0]
      image_data = base64.b64decode(image_base64)    

      try:
        with open(f"{save_dir}/{img_name}.jpg", "wb") as file:
            file.write(image_data)
      except Exception:
          print(f'Unable to save image {img_name} to {save_dir}') 
