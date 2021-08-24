from api import PetFriends
from settings import *
# import pytest

pf = PetFriends()

# Позитивные тесты


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Тест для запроса ключа API по почте и паролю"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter_=''):
    """Тест получения списка всех питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter_)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_new_pet_with_valid_key(name='test', animal_type='dog', age=2, pet_photo='images/Screenshot_1.jpg'):
    """Тест добавления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name


def test_delete_first_pet_with_valid_key():
    """Тест удаления первого питомца пользователя"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Katz', 'Cat', 10, 'images/Screenshot_2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_first_pet_with_valid_key(name='test1', animal_type='dog1', age=5):
    """Тест обновления данных первого питомца пользователя"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Katz', 'Cat', 10, 'images/Screenshot_2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name


def test_create_pet_simple_with_valid_key(name='test3', animal_type='dog2', age=6):
    """Тест простого добавления питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name


def test_set_photo_to_pet_with_valid_key(pet_photo='images/Screenshot_2.jpg'):
    """Тест добавления фото для первого питомца пользователя"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, 'Katz', 'Cat', 10)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_photo_to_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['id'] == pet_id

# Негативные тесты


def test_get_api_key_for_not_valid_email(email=not_valid_email, password=valid_password):
    """Тест запроса ключа API с неправильным логином"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result


def test_get_api_key_for_not_valid_password(email=valid_email, password=not_valid_password):
    """Тест запроса ключа API с неправильным паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'Forbidden' in result


def test_get_all_pets_with_not_valid_key(filter_=''):
    """Тест запроса списка питомцев с неправильным ключем API"""
    auth_key = {'key': '1'}
    status, result = pf.get_list_of_pets(auth_key, filter_)
    assert status == 403
    assert 'Forbidden' in result


def test_create_pet_simple_with_not_valid_key(name='test3', animal_type='dog2', age=6):
    """Тест запроса простого добавления питоца с неправильным ключем API"""
    auth_key = {'key': '1'}
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 403
    assert 'Forbidden' in result


def test_create_pet_simple_with_negative_age(name='test3', animal_type='dog2', age=-6):
    """Тест добавления питомца с отрицательным возрастом"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name


def test_create_pet_simple_with_long_name(name='Длиннок'+'o'*10000+'т', animal_type='cat2', age=11):
    """Тест добавления питомца с очень длинным именем"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['age'] == age
    assert result['animal_type'] == animal_type
    assert result['name'] == name


def test_set_photo_to_pet_wrong_format(pet_photo='images/1.txt'):
    """Тест добавления фото питомца не в формте изображения"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, 'Katz', 'Cat', 10)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_photo_to_pet(auth_key, pet_id, pet_photo)
    assert status == 400


def test_post_new_pet_with_no_photo(name='test', animal_type='dog', age=2):
    """Тест добавления питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)
    assert status == 400


def test_create_pet_simple_with_no_name(animal_type='dog2', age=6):
    """Тест простого добавления питомца без имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple_no_name(auth_key, animal_type, age)
    assert status == 400


def test_update_first_pet_with_wrong_pet_id(name='test11', age=51):
    """Тест изменения данных питомца по неправильному ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Katz', 'Cat', 10, 'images/Screenshot_2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = '1'
    status, result = pf.update_pet_info_wrong_id(auth_key, pet_id, name, age)
    assert status == 400
