import os
import io
def preview_page(text_chunks, book_name, user_id):

    s = f'<!doctype html>\n\
    <title>Content:</title>\n\
    <head>\n\
    </head>\n\
    <html>\n\
    <body>\n\
    <h1>{book_name}</h1>\n'

    for n, chunk in enumerate(text_chunks):
        s += '<p>' + chunk + '</p>\n'
        s += f'<img src="/static/books/{user_id}/{n}.jpg" \
                width="512" \
                height="512">\n'

    s += '</body> \n\
    </html>'

    with io.open(f'static/books/{user_id}/preview_page.html', mode='w') as f:
        f.write(s)

