import time

import requests
from tqdm import trange
from loguru import logger

class YaD:
    url = 'https://cloud-api.yandex.net/'
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def loader(self, data_list):
        name= input('Название папки: ')
        url_new = self.url + 'v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {'path': name}
        response = requests.put(url=url_new, headers=headers, params=params)
        if response.status_code == 201:
            logger.info(f'Создана папка {name}')
        else:
            logger.info('Папка с таким названием уже существут')

        upload_url = self.url + 'v1/disk/resources/upload'
        headers = self.get_headers()
        logger.info('Загрузка данных...')
        for i in trange(len(data_list)):
            file_name = data_list[i]['file_name']
            size = data_list[i]['size']
            url = data_list[i]['url']
            params = {'path': f'{name}/{file_name}', 'url': self.url, 'disable_redirects': False}
            response = requests.post(url=upload_url, headers=headers, params=params)
            time.sleep(1)
            response.raise_for_status()
            if response.status_code == 201:
                print('Загруженно')

