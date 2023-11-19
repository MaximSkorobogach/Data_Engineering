import requests

#Запрос на API по получению изображения собаки (формат - статус и ссылка на изображение)
def get_random_dog():
    api_url = 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(api_url)
    dog_data = response.json()
    return dog_data

#Создание HTML файла из полученного JSON ответа
def generate_html():
    dog_data = get_random_dog()

    if dog_data['status'] == 'success':
        image_url = dog_data['message']

        with open('random_dog.html', 'w', encoding='utf-8') as file:
            file.write(f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Случайная собака</title>
                </head>
                <body>
                    <h1>Случайная собака</h1>
                    <img src="{image_url}" alt="Случайная собака">
                </body>
                </html>
            ''')
    else:
        print("Не удалось получить данные о случайной собаке.")

generate_html()
