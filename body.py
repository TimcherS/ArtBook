from body2 import get_token, send_message, generate_image, named_ent_recognition, character_description
from chunker import adj_sent_clust
import html_gen
import os
import shutil
import io
import ProjectVariables

def processing(file, style = 'KANDINSKY'):

    AUTH = ProjectVariables.AuthData
    TOKEN = get_token(AUTH).json()['access_token']

    with io.open(file, mode='r', encoding='utf-8') as f:
        text = f.read()
        cnt = len(text)
        text_chunks = adj_sent_clust(text)

    cnt2 = 0
    for i in text_chunks:
        cnt2 += len(i)

    summary_prompt = '''
    Постарайся составить подробное описание сцены соответствующей следующему тексту в виде картинки:
    '''

    all_summaries = []
    for chunk in text_chunks:
        summary = send_message(TOKEN, '', summary_prompt + chunk)
        all_summaries.append(summary)
    
    print(len(all_summaries))

    pic_pos = []
    pic_pos_ind = 0
    for summary in all_summaries:
        pic_pos_ind += len(summary)
        pic_pos.append(pic_pos_ind)

    imgen_prompt_intro = '''\
    Нарисуй следующую сценку словно это - книжная иллюстрация: {}
    Её действующими лицами могут являться следующие персонажи: \n
    '''

    books_name = file.split('/')[-1].split('.')[0]
    character_descriptions_ = character_description(TOKEN, file)

    if os.path.isdir(f'images/{books_name}'):
        shutil.rmtree(f'images/{books_name}')

    os.makedirs(f'images/{books_name}')
    lost_descriptions = []

    for n, summary in enumerate(all_summaries):
        characters_in_scene = named_ent_recognition(TOKEN, summary, add_prompt=f'Сделай так чтобы одни лица назывались теми же именами \
                                           что и в данном списке: {', '.join(character_descriptions_)}')
        imgen_prompt = imgen_prompt_intro.format(summary)
        for character in characters_in_scene:
            if character not in character_descriptions_.keys():
                lost_descriptions.append(character)
                continue
            imgen_prompt += character + ": " + "".join(character_descriptions_[character]) + "\n"
        dir = f'images/{books_name}/{n}'
        print(imgen_prompt)
        generate_image(TOKEN, imgen_prompt, dir, style=style)
    
    html_gen.preview_page(text_chunks, 'images/neznaika/')

if __name__ == '__main__':
    file = 'C:/ML/Projects/Opus-illustro/books/neznaika.txt'
    processing(file)