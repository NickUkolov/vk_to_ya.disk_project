import copy
import json
import sys
import time
import requests
from tqdm import tqdm

user_id = input('Введите ID Вконтакте: \n')
ya_token = input('Введите ЯндексТокен: \n')
vk_token = 'vk1.a.TVXNLbwElky1HEHksF9QzY6bGv7lbNbGOv6stxpM_45fJbjB' \
           '-2F0buyrmf_YcE_e__uWJJv7XsdbDTDOIHl_AwVFkx7ukYYPg5UixTLoQdfBvb6V6kGd' \
           '-w6vUCpNHv_VXVkO5sRwhdER8z2dGQRdieJiLQUMohiHSa5HsnGIgd09p4XI-IqC8DDg7AE6selQ '


class VkUser:
    print(f'Выгружаем фотографии из профиля ВК {user_id} \n')
    time.sleep(2)

    def __init__(self, token, user_id, version='5.131', count=5):
        self.photos_result_list = []
        self.token = vk_token
        self.id = user_id
        self.version = version
        self.params = {
            'access_token': self.token,
            'v': '5.131'
        }
        self.count = input('Введите количество фотографий для сохранения: \n')

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': self.count
        }
        response = requests.get(url=url, params={**self.params, **params}).json()

        if list(response)[0] != 'response':
            print('Введен неверный ID \n')
            sys.exit(0)
        response_status = requests.get(url, params={**self.params, **params}).status_code
        if response_status == 200:
            print('Начало выгрузки фотографий \n')
        elif response_status >= 400:
            print(f'Ошибка {response_status} \n')
        time.sleep(1)

        photos_items = response['response']['items']

        json_list = []
        json_dict = {}
        json_dict_copy = {}
        name_checklist = []

        for photos_data in photos_items:
            name = photos_data['likes']['count']
            photo = photos_data['sizes'][-1]['url']
            if name not in name_checklist:
                json_dict["file_name"] = f"{name}.jpg"
                json_dict['size'] = photos_data['sizes'][-1]['type']
            else:
                json_dict["file_name"] = \
                    f"{name}.jpg, 'date':{photos_data['date']}"
                json_dict['size'] = photos_data['sizes'][-1]['type']
            name_checklist.append(name)
            json_dict_copy = copy.deepcopy(json_dict)
            json_list.append(json_dict_copy)
            with open('data.json', 'w') as write_file:
                json.dump(json_list, write_file)
            self.photos_result_list.append(photo)
        print('Создан json \n')
        time.sleep(1)

        return json_list


class YaDisk:

    def __init__(self, Token):
        self.Token = ya_token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.Token)
        }

    def disk_file_path(self, path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        requests.put(f"{url}?path={path}", headers=headers)
        print('Создана папка на Яндекс Диске \n')
        time.sleep(1)
        return f"{url}?path={path}"

    def upload_to_yandexdisk(self, disk_file_path):
        print('Загрузка фото на Яндекс Диск \n')
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        with open('data.json') as file_object:
            list_name_photos = json.load(file_object)
        for dict_names, photo_url in tqdm(zip(list_name_photos, vk1.photos_result_list)):
            time.sleep(0.5)
            name = dict_names['file_name']
            if len(name) > 12:
                name = name[:14]
            params = {"path": f'Photo_VK/{name}',
                      'url': photo_url}
            response = requests.post(upload_url, headers=headers, params=params)
            time.sleep(1)
        if 200 <= response.status_code < 400:
            print('Фотографии успешно выгружены \n')
        elif response.status_code >= 400:
            print(f'Ошибка {response.status_code}')


if __name__ == '__main__':
    vk1 = VkUser(vk_token, user_id)
    ya1 = YaDisk(ya_token)
    vk1.get_photos()
    ya1.disk_file_path('Photo_VK')
    ya1.upload_to_yandexdisk(disk_file_path='Photo_VK')
