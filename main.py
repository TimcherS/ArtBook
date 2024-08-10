from APIs import GigachatAPI, KandinskyAPI
from text_processing import named_ent_recognition, character_description
from text_chunker import adj_sent_clust
import html_gen
import os
import shutil
import io
import ProjectVariables

def processing(user_uuid, book_name, style='KANDINSKY'):

    Gigachat = GigachatAPI(AUTH=ProjectVariables.GigachatAuthData, style='KANDINSKY')
    Kandinsky = KandinskyAPI('https://api-key.fusionbrain.ai/', ProjectVariables.KandinskyAPIKey, ProjectVariables.KandinskySecretKey)

    with io.open(f'static/books/{user_uuid}/{book_name}.txt', mode='r', encoding='utf-8') as f:
        text = f.read()
        cnt = len(text)
        character_descriptions_ = character_description(LLM_model=Gigachat, text=text)
        text_chunks = adj_sent_clust(text=text)
    
    # s = 0
    # for chunk in text_chunks:
    #     s += len(chunk)
    #     print(len(chunk))
    # print(len(text_chunks), s / len(text_chunks))

    # cnt2 = 0
    # for i in text_chunks:
    #     cnt2 += len(i)
    # print(cnt, cnt2)

    summary_prompt = '''
    Постарайся составить описание сцены соответствующей следующему тексту:
    '''

    all_summaries = []
    for chunk in text_chunks:
        summary = Gigachat.send_message(prompt=summary_prompt + chunk)
        all_summaries.append(summary)

    imgen_prompt_intro = '''\
    Нарисуй следующую сцену: {}
    '''

    lost_descriptions = []

    for n, summary in enumerate(all_summaries):
        characters_in_scene = named_ent_recognition(LLM_model=Gigachat, text=summary)
        imgen_prompt = imgen_prompt_intro.format(summary)
        if len(characters_in_scene) != 0:
            imgen_prompt += 'Её действующими лицами могут являться следующие персонажи: \n'
        for character in characters_in_scene:
            if character not in character_descriptions_.keys():
                lost_descriptions.append(character)
                continue
            imgen_prompt += character + ": " + "".join(character_descriptions_[character]) + "\n"
        img_dir = f'static/books/{user_uuid}'
        print(imgen_prompt)
        Kandinsky.generate_image(prompt=imgen_prompt, save_dir=img_dir, img_name=f'{n}', style=style) #DONT FORGET

    html_gen.preview_page(text_chunks=text_chunks, book_name=book_name, user_id=user_uuid)
