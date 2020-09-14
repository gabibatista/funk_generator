import scrapy, re

class FunkSpider(scrapy.Spider):
    name = 'funk_spider'
    start_urls = ['https://www.letras.com.br/top-letras-musicas/funk']
    songs = ''
    song_cnt = 0

    def parse(self, response):
        ## Check current URL
        if response.url == self.start_urls[0]:
            ## Catching all songs
            ITEM_SELECTOR = '.item-box'
            items = response.css(ITEM_SELECTOR)

            self.song_cnt = len(items)

            for item in items:
                ## Get song link
                URL_SELECTOR = 'a ::attr(href)'
                url = item.css(URL_SELECTOR).extract_first()

                if url:
                    ## Go to song page
                    yield scrapy.FormRequest(url=url, callback=self.parse)

        else:
            ## Get song title and artist
            NAME_SELECTOR = '.title ::text'
            ARTIST_SELECTOR = '.subtitle ::text'

            name = response.css(NAME_SELECTOR).get()
            self.songs += "+%s+," % name
            artist = response.css(ARTIST_SELECTOR).get()
            self.songs += "+%s+," % artist

            ## Get lyrics
            LYRICS_SELECTOR = '.lyrics-section'
            lyrics = response.css(LYRICS_SELECTOR)

            self.songs += "+"
            LINE_SELECTOR = 'p ::text'
            for line in lyrics.css(LINE_SELECTOR):
                self.songs += re.sub('\r', '', "%s|" % line.get())
            self.songs += "+" + "\n"

        with open('dataset.csv', 'w') as dataset:
            dataset.write("name,artist,lyric" + "\n")
            dataset.write(self.songs)
