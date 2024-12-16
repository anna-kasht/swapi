import requests
from pathlib import Path


# создаем базовый класс
class APIRequester:

    def __init__(self, base_url):
        self.base_url = base_url

    # метод get() осуществляет запрос к сайту и делает проверку исключений
    def get(self, url):
        try:
            response = requests.get(self.base_url + url)
            response.raise_for_status()  # Проверяет статус ответа
            return response
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')
            return None  # requests.models.Response()


# создаем наследника класса
class SWRequester(APIRequester):

    def __init__(self, base_url='https://swapi.dev/api/'):
        super().__init__(base_url)

    # метод get_sw_categories() выполнять запрос к сайту и возвращать список
    # # доступных категорий
    def get_sw_categories(self):
        response = self.get('/')
        if response is not None:
            categories = response.json().keys()
            return categories
        return []

    # метод get_sw_info() принимает одну из категорий, делает запрос и
    # возвращает ответ в виде строки
    def get_sw_info(self, sw_type):
        url = f'/{sw_type}/'
        response = self.get(url)
        if response is not None:
            return response.text
        return ''


# функция save_sw_data() создает объект класса SWRequester, директорию,
# получает полный список категорий, для каждой категории выполнит запрос к ней
# и сохранит файл
def save_sw_data():
    response_swapi = SWRequester('https://swapi.dev/api')
    categories_swapi = list(response_swapi.get_sw_categories())
    try:
        Path('data').mkdir(exist_ok=True)
    except Exception:
        print('Папка "data" не была создана')
    try:
        for category in categories_swapi:
            path = f'data/{category}.txt'
            with open(path, 'w', encoding='utf-8') as file:
                file.write(response_swapi.get_sw_info(category))
    except Exception:
        print('Ошибка при создании и записи файлов')
