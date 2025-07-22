from app.api import PetFriends
from app.settings import valid_email, valid_password
import os
pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images\cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    # Затем проверяем, что имя питомца совпадает с ожидаемым
    if isinstance(result, dict):
        assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурз', animal_type='Кот', age='15'): #
    """Проверяем возможность обновления информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Рекс", "собака", "2")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на обновление информации
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name

def test_set_pet_photo(): #
    """ Устанавливаем фотографию питомцу """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Рекс", "собака", "2")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/cat1.jpg')
    status, result = pf.set_pet_photo(auth_key, pet_id, pet_photo)
    assert status == 200


def test_create_pet_without_photo():
    """ Проверяем возможность создать питомца без фотографии """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, "Рекс", "собака", "2")
    assert status == 200
    assert result['name'] == "Рекс"

def test_get_pets_with_filter(): #
    """ Проверяем получение питомцев с указанием конкретного фильтра """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert len(result['pets']) >= 0

def test_get_api_key_for_user(email='elex@mail', password='123456'): #
    """ Проверяем что запрос api ключа возвращает статус 403 при некорректных логине и пароле"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_negative_wrong_email():
    """ Неправильный email при попытке залогиниться """
    status, result = pf.get_api_key("bad_email@gmail.com", valid_password)
    assert status == 403

def test_negative_no_token():
    """ Запрос без аутентификационного токена """
    status, result = pf.get_list_of_pets({}, "my_pets")
    assert status == 403  # ожидается ошибка, поскольку токен отсутствует

def test_negative_bad_pet_id():
    """ Пытаемся получить питомца с несуществующим ID """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, "not_existing_id")
    assert status == 500

def test_negative_large_age():
    """ Создаем питомца с недопустимым значением поля возраст """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, "Барсик", "кот", "-5")
    assert status == 400

def test_negative_empty_fields():
    """ Попробуем создать питомца с пустыми обязательными полями """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, "", "", "")
    assert status == 400

def test_update_pet_info_incorrect_data(name='%&(', animal_type='525', age='kjj'):
    """ Изменим информацию о питомце на некорректные данные """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pf.create_pet_simple(auth_key, "Рекс", "собака", "2")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    assert status == 400

def test_delete_nonexistent_pet():
    """Попытка удалить несуществующего питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = 'bjj8retcrte'
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Проверяем что статус ответа равен 400
    assert status == 400
    assert pet_id not in my_pets.values()