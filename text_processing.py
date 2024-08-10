def named_ent_recognition(LLM_model, text, add_prompt=''):
  prompt = ''' 
  Прочитай следующий текст в выдели из него имена людей. \
  Затем перечисли их через запятую в именительном падеже.
  Вот текст:
  '''    
  ans = LLM_model.send_message(prompt=prompt + text + add_prompt)
  characters = [i.strip() for i in ans.split(',')]

  return characters
    
def character_description(LLM_model, text, span=100):

  traits_prompt = '''\
  Выдели особенности внешности и характера персонажа {} из текста и перечисли их через запятую, если \
  не можешь их найти напиши 'нет' и закончи, не выдумывай лишнего. Вот текст:
  '''
  summary_prompt_beg = '''\
  Кратко опиши персонажа исходя из его характеристик, если их нет то напиши что 'описания нет \
  Вот характеристики: 
  '''

  characters = named_ent_recognition(LLM_model=LLM_model, text=text)
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
    characters_info[character].append(LLM_model.send_message(prompt=send))

  # for character in characters_info.keys():
  #    print(characters_info[character])
  # print('----------------------')
  for character in characters:
    summary_prompt = summary_prompt_beg
    for traits in characters_info[character]:
       summary_prompt += traits
    characters_summary[character] = LLM_model.send_message(prompt=summary_prompt)
    # print(characters_summary[character])
     
  return characters_summary
    
    
    