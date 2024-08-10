from APIs import KandinskyAPI
import ProjectVariables
api = KandinskyAPI('https://api-key.fusionbrain.ai/', ProjectVariables.KandinskyAPIKey, ProjectVariables.KandinskySecretKey)
# prompt = ''' 
# Нарисуй следующую сцену: Сцена представляет собой просторный зал, в котором собрались коротышки для обсуждения книги Знайки.\
# В центре внимания - профессор Звездочкин, который делает доклад о книге.\
# Он критикует Знайку за научную необоснованность его идей и утверждает,\
# что Луна не может быть пустой внутри, иначе все предметы притянуло бы к центру и они погибли бы.\
# '''
prompt = 'Нарисуй семью котов.'
api.generate_image(prompt=prompt, save_dir='images', img_name='4', style="KANDINSKY")