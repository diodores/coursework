import requests
import json
from tqdm import trange
import time
from loguru import logger

TOKEN = ' '   #Ввести токен VK


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

    def upload_l(self, my_list):
        upload_list = []
        for file in my_list[-1:-6:-1]:
            upload_list.append(file)
        logger.info('Отобаны фото для загузки')
        return upload_list
