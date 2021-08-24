import json
import os

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends1.herokuapp.com/'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        с уникальным ключем пользователя с указанной почтой и паролем"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: dict, filter_: str) -> json:
        """Метод делает запрос к API сервера и возвращает список питомцев, совпадающих с фильтром. На данный момент
        фильтр может быть или пустым и возвращать список всех питомцев или иметь значение my_pets и возвращать
        список питомцев указанного пользователя"""
        headers = {'auth_key': auth_key['key']}
        filter_ = {'filter': filter_}
        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter_)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: dict, name: str, animal_type: str, age: int, pet_photo: str) -> json:
        """Метод делает запрос к API и добавляет питомца с указанными параметрами и фото для текущего пользователя"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: dict, pet_id: str) -> json:
        """Метод делает запрос к API сервера и удаляет питомца текущего пользователя по ID"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: dict, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод делает запрос к API сервера и изменяет питомца текущего пользователя по ID"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'animal_type': animal_type,
                'age': age
                }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple(self, auth_key: dict, name: str, animal_type: str, age: int) -> json:
        """Метод делает запрос к API сервера и добавляет питомца без фото"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def set_photo_to_pet(self, auth_key: dict, pet_id: str, pet_photo: str) -> json:
        """Метод делает запрос к API сервера и изменяет фото питомца пользователя по ID"""
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        # result = ''
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    # Функции для негативных тестов API

    def add_new_pet_no_photo(self, auth_key: dict, name: str, animal_type: str, age: int) -> json:
        """Метод делает запрос к API и пытается добавить питомца с указанными параметрами для текущего пользователя"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,

        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def create_pet_simple_no_name(self, auth_key: dict, animal_type: str, age: int) -> json:
        """Метод делает запрос к API сервера и пытается добавляет питомца без имени"""
        data = {
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info_wrong_id(self, auth_key: dict, pet_id: str, name: str, age: int) -> json:
        """Метод делает запрос к API сервера и пытается изменить питомца текущего пользователя по ID
        без типа животного"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name,
                'age': age
                }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.JSONDecodeError:
            result = res.text
        return status, result
