import time

from loguru import logger
from VK import VKUser, TOKEN
from YD import YaD



if __name__ == '__main__':
    user_ids = int(input('Введите id пользователя: ').strip())
    token_ya = str(input('Введите токен яндекс диска: ').strip())
    vk = VKUser(TOKEN=TOKEN, user_ids=user_ids)
    ya = YaD(token_ya)
    result = vk.upload_l(vk.search_photo())
    time.sleep(1)
    ya.loader(result)
    logger.info('Завершенно!')