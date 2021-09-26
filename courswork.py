import requests
import json
from tqdm import trange
import time
from loguru import logger

with open('/Users/dmitrijsazin/Desktop/pythonProject/ Token_VK/Token_Vk.txt', 'r') as file:
    TOKEN = file.read().strip()


class VKUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, TOKEN, user_ids):
        self.params = {
            'access_token': TOKEN,
            'v': '5.131',
            'owner_id': user_ids
        }

    def search_photo(self, extended=1, album_id='profile'):
        url_photo = self.url + 'photos.get'
        params_photo = {
            'extended': extended,
            'album_id': album_id
        }
        result = requests.get(url_photo, params={**params_photo, **self.params})
        res = result.json()
        data = {}
        with open('foto.json', 'w') as f:
            json.dump(res, f)
        data.update(res)
        data_list = []
        my_list = []
        logger.info('Выгружаю данные...')
        for i in trange(len(data['response']['items'])):
            time.sleep(0.5)
            name = data['response']['items'][i]['likes']['count']
            size = data['response']['items'][i]['sizes'][-1]['type']
            url = data['response']['items'][i]['sizes'][-1]['url']
            data_dict = ({'file_name': str(name) + '.jpg', 'size': size})
            my_dict = ({'file_name': str(name) + '.jpg', 'size': size, 'url': url})
            data_list.append(data_dict)
            my_list.append(my_dict)
        return my_list


class YaD:
    url = 'https://cloud-api.yandex.net/'
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _path(self):
        url_new = self.url + 'v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        params = {'path': f'Photo id {str(id)}'}
        response = requests.put(url=url_new, headers=headers, params=params)
        if response.status_code == 201:
            print('Created')
        return f'Photo id {str(id)}'

    def loader(self, data_list):
        upload_url = self.url + 'v1/disk/resources/upload'
        headers = self.get_headers()
        logger.info('Загрузка данных...')
        for i in trange(len(data_list)):
            file_name = data_list[i]['file_name']
            size = data_list[i]['size']
            url = data_list[i]['url']
            params = {'path': f'{path}/{file_name}', 'url': url, 'disable_redirects': False}
            response = requests.post(url=upload_url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 201:
                print('Загруженно')




if __name__ == '__main__':
    user_ids = int(input('Введите id пользователя: ').strip())
    token_ya = str(input('Введите токен яндекс диска: ').strip())
    vk = VKUser(TOKEN=TOKEN, user_ids=user_ids)
    ya = YaD(token_ya)
    result = vk.search_photo()
    path = ya._path()
    ya.loader(result)
    logger.info('Завершенно!')
