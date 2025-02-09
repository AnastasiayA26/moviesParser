# Парсер собирает информацию о фильмах - год выпуска, страна, режиссер, название, жанр
###https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту
### Инструкция по работе с парсером
```bash
git clone https://github.com/AnastasiayA26/moviesParser.git
cd moviesParser
pip install scipy
scrapy crawl movies_info -o <имя файла>.csv
