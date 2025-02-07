import scrapy
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from movies_parser.items import MoviesParserItem

class MoviesSpider(scrapy.Spider):
    name = "movies"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/Категория:Фильмы_по_алфавиту"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Парсим список фильмов
        films = response.css('div.mw-category-group ul li a')

        for film in films:
            title = film.css('::text').get()
            link = film.css('::attr(href)').get()

            # Полная ссылка на фильм
            full_link = response.urljoin(link)

            # Переход на страницу фильма
            yield scrapy.Request(url=full_link, callback=self.parse_film, meta={'title': title, 'link': full_link})

        current_page = response.meta.get('page', 1)
        next_page = response.css('a:contains("Следующая страница")::attr(href)').get()

        if next_page:
            next_page_url = self.make_next_url(response.urljoin(next_page), current_page)
            yield scrapy.Request(
                url=next_page_url,
                callback=self.parse,
                meta={'page': current_page + 1}
            )

    def make_next_url(self, next_page_url: str, current_page: int) -> str:
        parsed_url = urlparse(next_page_url)
        query = parse_qs(parsed_url.query)
        query['_'] = [str(current_page + 1)]

        unique_url = urlunparse(parsed_url._replace(
            query=urlencode(query, doseq=True)
        ))

        unique_url = unique_url.replace('w/index.php', 'wiki')
        return unique_url

    # def parse_film(self, response):
    #     title = response.meta['title']
    #     infobox = response.css("table.infobox")
    #
    #     def extract_data(label):
    #         return infobox.xpath(f".//th[contains(text(), '{label}')]/following-sibling::td//text()").getall()
    #
    #     director = extract_data("Режиссёр")
    #     country = extract_data("Страна") or extract_data("Страны")
    #     release_year = extract_data("Год") or extract_data("Дата выхода")
    #
    #     genre_row = response.xpath('//th[a[contains(text(), "Жанр") or contains(text(), "Жанры")]]/following-sibling::td')
    #     genres = genre_row.css('a::text').getall()
    #
    #     director = [re.sub(r"\[.*?\]", "", d).strip() for d in director]
    #     director = [d for d in director if not d.startswith(".mw-parser-output")]
    #     director = " ".join(d for d in director if d)
    #
    #     country = [c.replace("\xa0", " ").strip() for c in country]
    #     country = ", ".join(c for c in country if c)
    #
    #     year = None
    #     if release_year:
    #         for text in release_year:
    #             match = re.search(r"\b(\d{4})\b", text)
    #             if match:
    #                 year = match.group(1)
    #                 break
    #
    #     yield {
    #         "title": title,
    #         "genre": ", ".join(g.strip() for g in genres if g.strip()),
    #         "director": director,
    #         "country": "".join(country).strip(),
    #         "year": "".join(year).strip()
    #     }

    def parse_film(self, response):
        item = MoviesParserItem()
        item['title'] = response.meta['title']
        infobox = response.css("table.infobox")

        def extract_data(label):
            return infobox.xpath(f".//th[contains(text(), '{label}')]/following-sibling::td//text()").getall()

        director = extract_data("Режиссёр")
        country = extract_data("Страна") or extract_data("Страны")
        release_year = extract_data("Год") or extract_data("Дата выхода")

        genre_row = response.xpath('//th[a[contains(text(), "Жанр") or contains(text(), "Жанры")]]/following-sibling::td')
        genres = genre_row.css('a::text').getall()

        director = [re.sub(r"\[.*?\]", "", d).strip() for d in director]
        director = [d for d in director if not d.startswith(".mw-parser-output")]
        item['director'] = " ".join(d for d in director if d)

        country = [c.replace("\xa0", " ").strip() for c in country]
        country = ", ".join(c for c in country if c)

        year = None
        if release_year:
            for text in release_year:
                match = re.search(r"\b(\d{4})\b", text)
                if match:
                    year = match.group(1)
                    break

        item['genre'] = ", ".join(g.strip() for g in genres if g.strip())
        item['country'] = "".join(country).strip()
        item['year'] = "".join(year).strip()

        yield item