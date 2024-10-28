import requests
from bs4 import BeautifulSoup

url = 'https://ru.wikipedia.org/wiki/Python'

response = requests.get(url)

if response.status_code == 200:
    print("Страница успешно загружена!")
else:
    print("Ошибка загрузки страницы:", response.status_code)
soup = BeautifulSoup(response.text, 'lxml')

h3_tags = soup.find_all('h3')
h3_tags_text = [tag.get_text()+'\n' for tag in h3_tags]
with open('13.txt', 'w') as f:
    f.writelines(h3_tags_text)
    print("Теги сохранены в файл 13.txt")