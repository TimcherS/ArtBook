import os
import io
def preview_page(text_chunks, dir):
    s = f'<!doctype html> \n\
    <title>Content:</title> \n\
    <head> \n\
    </head> \n\
    <html> \n\
    <body>'

    img_n = len(text_chunks)
    for n, chunk in enumerate(text_chunks):
        s += '<p>' + chunk + '</p>\n'
        s += f'<img src={dir}/{n}.jpg>\n'
    s += '</body> \n\
    </html>'

    # os.makedirs('/html')
    with io.open('html/preview_page.txt', mode='w', encoding='utf-8') as f:
        f.write(s)

