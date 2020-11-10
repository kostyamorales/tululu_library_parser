import argparse
from utils import get_last_page, get_books_url, get_html, get_response_book
from book import get_book
from os import chdir
from pathlib import Path
import json


def arg_parse():
    parser = argparse.ArgumentParser(
        description='Программа скачивает коллекцию книг фантастического жанра'
    )
    parser.add_argument('--start_page', type=int, help='с какой страницы скачать', default=1)
    parser.add_argument('--end_page', type=int, help='до какой страницы скачать, не включая её',
                        default=get_last_page() + 1)
    parser.add_argument('--dest_folder', help='путь к каталогу с результатами парсинга: картинкам, книгам, JSON')
    parser.add_argument('--skip_imgs', help='не скачивать картинки', action="store_true")
    parser.add_argument('--skip_txt', help='не скачивать txt', action="store_true")
    parser.add_argument('--json_path', help='указать свой путь к *.json файлу с результатами')
    args = parser.parse_args()
    return args


def main():
    args = arg_parse()
    start_page = args.start_page
    end_page = args.end_page
    books_url = get_books_url(start_page, end_page)
    books = []
    if args.dest_folder:
        Path(args.dest_folder).mkdir(parents=True, exist_ok=True)
        chdir(args.dest_folder)
    for book_url in books_url:
        num_book = book_url.split('b')[-1]
        response, url = get_response_book(num_book)
        if response.url != url:
            continue
        book_html = get_html(book_url)
        book = get_book(book_html, response, args.skip_txt, args.skip_imgs)
        books.append(book)
    if args.json_path:
        Path(args.json_path).mkdir(parents=True, exist_ok=True)
        chdir(args.json_path)
    with open(f'books.json', 'a', encoding='utf8') as file:
        json.dump(books, file, ensure_ascii=False)


if __name__ == '__main__':
    main()