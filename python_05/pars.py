import scrapy

class MoviesSpider(scrapy.Spider):
    name = "movies"
    start_urls = [
        "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"
    ]

    def parse(self, response):
        # Выделяем часть страницы с нужным контентом
        films = response.css("#mw-pages")

        # Находим ссылки на статьи о фильмах
        for link in films.css(".mw-category a::attr(href)").getall():
            yield response.follow(link, self.parse_movie)

        # Переходим на следующую страницу, если она есть
        next_page = films.css("a:contains('Следующая страница')::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_movie(self, response):
        infobox = response.css(".infobox")

        title = infobox.css(".infobox-above ::text").get()

        # Ищем значения по заголовкам в первой колонке
        def get_value(label):
            return infobox.xpath(f".//tr[th[contains(text(), '{label}')]]/td//text()").getAll().join(';').strip()

        genre = get_value("Жанр")
        director = get_value("Режиссёр")
        country = get_value("Страна")
        year = get_value("Год")

        res = {
            'Название': title,
            'Жанр': genre,
            'Режиссер': director,
            'Страна': country,
            'Год': year,
        }
        print(res)
        yield res
