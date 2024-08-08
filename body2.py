import requests
import json
import uuid
import io

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    rq_uid = str(uuid.uuid4())
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }
    payload = {
        'scope': scope
    }
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f'Ошибка при получении токена: {str(e)}')
        return -1

def send_message(TOKEN, system_prompt, prompt, model='GigaChat-Pro'):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
      "model": f"{model}",
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
        'Authorization': f'Bearer {TOKEN}'
    }
    try:
      response = requests.request("POST", url, headers=headers, data=payload, verify=False)
      return response.json()['choices'][-1]['message']['content']    
    except requests.RequestException as e:
        print(f'Ошибка с получением ответа на запрос: {str(e)}')
        return -1

def generate_image(TOKEN, prompt, dir, model='GigaChat-Pro', style='KANDINSKY', width=640, height=480):
  gen_url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
    
  payload = json.dumps({
      'model': f'{model}',
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
      'Authorization': f'Bearer {TOKEN}'
  }

  response = requests.request("POST", gen_url, headers=headers, data=payload, verify=False)
  print(response.json())
  img_id = response.json()['choices'][-1]['message']['content']
  img_id = img_id[img_id.find('<img src="') + len('<img src="') : img_id.find('" fuse=')]

  dwnld_url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{img_id}/content"

  headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Bearer {TOKEN}'
  }

  response = requests.request("GET", dwnld_url, headers=headers, verify=False)
  with io.open(f'{dir}.jpg', mode='wb') as out_file:
      out_file.write(response.content)

def current_styles():
   url = 'https://cdn.fusionbrain.ai/static/styles/api'
   response = requests.request('GET', url, verify=False).json()
   return [i['name'] for i in response[:]]

def get_models(TOKEN):
   
  url = "https://gigachat.devices.sberbank.ru/api/v1/models"
  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {TOKEN}'
  }
  response = requests.request("GET", url, headers=headers, data=payload, verify=False)
  return response.json()

def named_ent_recognition(TOKEN, text, add_prompt=''):
  prompt = ''' 
  Прочитай следующий текст в выдели из него имена собственные. Имена собственные должны быть одушевлены - принадлежать живым существам вроде людей в том числе различных 
  профессий или животным.
  Затем перечисли их через запятую.
  Вот текст:
  '''    
  ans = send_message(TOKEN, '', prompt + text + add_prompt)
  characters = [i.strip() for i in ans.split(',')]

  return characters
    
def character_description(TOKEN, text, span=100):

  traits_prompt = '''\
  Выдели особенности внешности и характера персонажа {} из текста и перечисли их через запятую:
  '''
  summary_prompt_beg = '''\
  Кратко опиши персонажа для художника исходя из следующих характеристик:
  '''

  characters = named_ent_recognition(TOKEN, text) #OPTMIZ?
  characters_mention = {character: [] for character in characters}
  characters_info = {character: [] for character in characters}
  characters_summary = {character: [] for character in characters}

  for character in characters:
    start_ind = 0
    appear = []
    while text.find(character, start_ind) != -1:
      appear.append(text.find(character, start_ind))
      start_ind = text.find(character, start_ind) + 1

    for i in range(len(appear)):
      earl_app, late_app = appear[i], appear[i]
      while i + 1 != len(appear) and (appear[i + 1] - appear[i + 1]) < span:
        late_app = appear[i + 1]
        i += 1
      characters_mention[character].append([earl_app - span, late_app + span])

  for character in characters:
    send = traits_prompt.format(character) + "".join([text[i[0] : i[1]] + "\n" for i in characters_mention[character]])
    characters_info[character].append(send_message(TOKEN, '', send))

  for character in characters_info.keys():
     print(characters_info[character])
  print('----------------------')
  for character in characters:
    summary_prompt = summary_prompt_beg
    for traits in characters_info[character]:
       summary_prompt += traits
    characters_summary[character] = send_message(TOKEN, '', summary_prompt)
    print(characters_summary[character])
     
  return characters_summary
    
    
    