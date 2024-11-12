from time import sleep

from helium import *

if __name__ == "__main__":
    driver = start_chrome('https://www.letras.com.br/top-letras-musicas/funk')
    items = find_all(S('.item-box'))
    links = [item.web_element.get_attribute('href') for item in items]
    rows = []

    for link in links:
        go_to(link)
        sleep(2)
        lyrics = [p.web_element.text for p in find_all(S('.lyrics-section'))]
        lyric = '|'.join(lyrics)

        if lyric and (lyric != 'Ainda não possuímos a letra dessa música =('):
            print(link)
            name = S('.title').web_element.text
            artist = S('.subtitle').web_element.text
            row = '+' + name + '+,+' + artist + '+,+' + lyric + '+'
            rows.append(row)

    kill_browser()

    with open('./dataset.csv', 'a') as dataset:
        dataset.write('\n'.join(rows))

    print(f'{len(rows)} new songs added.')