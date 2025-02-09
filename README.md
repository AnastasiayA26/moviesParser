# Парсер собирает информацию о фильмах - год выпуска, страна, режиссер, название, жанр [Категория:Фильмы по алфавиту]: http://www.reddit.comhttps://ru.wikipedia.org/wiki?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=45+%D0%BB%D0%B5%D1%82#mw-pages


### Инструкция по работе с парсером
```bash
git clone https://github.com/AnastasiayA26/moviesParser.git
cd moviesParser
pip install scipy
scrapy crawl movies_info -o <имя файла>.csv
