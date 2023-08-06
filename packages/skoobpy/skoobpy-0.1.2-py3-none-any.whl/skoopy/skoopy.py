import requests
import json
import csv

url_base = 'https://www.skoob.com.br'


def get_all_books(user_id):
    url = f'{url_base}/v1/bookcase/books/{user_id}'
    print(f'request to {url}')

    user = requests.get(url)
    total = user.json().get('paging').get('total')
    total_books = f'{url}/shelf_id:0/page:1/limit:{total}'

    books_json = requests.get(total_books).json().get('response')

    return books_json

def save_desired_csv(books_json, user_id):
    books = []

    header = ['Title', 'Author', 'Published Year', 'Pages', 'Publisher', 'Skoob\'s Website']

    for book in books_json:
        if book['desejado'] == 1:
            ed = book['edicao']

            # if there is a subtitle, it must be concatenate to title
            if ed['subtitulo'] != '':
                book_title = str(ed['titulo']) + ' - '+ str(ed['subtitulo'])
            else:
                book_title = ed['titulo']

            book_url = url_base + ed['url']

            book_data = [book_title, ed['autor'], ed['ano'], ed['paginas'], ed['editora'], book_url]
            books.append(book_data)

    with open(f'books_{user_id}.csv', 'w', encoding='utf-8', newline='') as csvfile:
        data = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        data.writerow(header)

        for book in books:
            data.writerow(book)
    
    return

    



    