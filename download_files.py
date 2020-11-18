from pathlib import Path
from urllib.parse import urljoin
import requests
from os import path, getcwd
from pathvalidate import sanitize_filename
from utils import check_response


def download_image(book_url, img_url, folder='images/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    url = urljoin(book_url, img_url)
    response = requests.get(url, verify=False, allow_redirects=False)
    check_response(response)
    filename = img_url.split('/')[-1]
    filepath = path.join(getcwd(), folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_txt(response, title, folder='books/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    title = title[:130]  # # Чтобы ограничить кол-во символов в названии файла и предотвратить OSError.
    filename = sanitize_filename(f'{title}.txt')
    filepath = path.join(getcwd(), folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath
