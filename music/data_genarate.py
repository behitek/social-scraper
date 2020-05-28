import json
import random
import re

from music.rule import RULES_SONG_OF, RULES_SONG, RULES_ALBUM


def get_para():
    vi_articles = json.load(open('vi_artists_full.prep.json', encoding='utf8'))

    song_names = []
    song_names_of = []

    for artist in vi_articles:
        name = artist.get('name').lower()
        for song in artist.get('song'):
            song_names.append(song)
            song_names_of.append("{}#{}".format(song, name))

    with open('song.list', 'w', encoding='utf8') as fp:
        [fp.write(x + "\n") for x in list(set(song_names))]

    with open('song_of.list', 'w', encoding='utf8') as fp:
        [fp.write(x + "\n") for x in song_names_of]


def gen_song_of():
    paras = open('vi_song_of.txt', encoding='utf8').read().splitlines()
    rs = []
    for para in paras:
        song, author = para.split('#')
        for rule in RULES_SONG_OF:
            text = []
            for ele in rule:
                if type(ele) is list:
                    text.append(random.choice(ele))
                elif ele == 'p.song':
                    text.append(song)
                elif ele == 'p.artist':
                    text.append(author)
            print(re.sub(r'\s+', ' ', ' '.join(text)).strip())


def gen_song():
    paras = open('song.list', encoding='utf8').read().splitlines()
    for song in paras:
        for rule in RULES_SONG:
            text = []
            for ele in rule:
                if type(ele) is list:
                    text.append(random.choice(ele))
                elif ele == 'p.song':
                    text.append(song)
            print(re.sub(r'\s+', ' ', ' '.join(text)).strip())


def gen_album():
    paras = open('album.list', encoding='utf8').read().splitlines()
    for album in paras:
        for rule in RULES_ALBUM:
            text = []
            for ele in rule:
                if type(ele) is list:
                    text.append(random.choice(ele))
                elif ele == 'p.album':
                    text.append(album)
            print(re.sub(r'\s+', ' ', ' '.join(text)).strip())


def gen_lienkhuc():
    for text in open('vi_lienkhuc.list', encoding='utf8').read().splitlines():
        print((random.choice(['tìm', 'tìm kiếm', 'mở', 'chơi', 'hát', 'bật', "nghe", "phát"]) + " " + text).strip())


def gen_genres():
    for text in open('genres.txt', encoding='utf8').read().splitlines():
        print((random.choice(['mở các ca khúc', 'chơi các ca khúc', 'bật các ca khúc', "nghe các ca khúc",
                              "phát các ca khúc", "phát bảng xếp hạng"]) + " " + text).strip())


# gen_song_of()
# gen_song()
# gen_album()
# gen_lienkhuc()
gen_genres()
