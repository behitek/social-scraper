import json
from builtins import enumerate

import regex as re

from music.norm_module import text_norm

normzlizer = text_norm.TextNorm()


def preprocess(song_name):
    song_name = song_name.lower()
    song_name = re.sub(r'\s*\(beat\)$', ' beat', song_name)
    song_name = re.sub(r'\s*\(remix\)$', ' remix', song_name)
    song_name = re.sub(r'\s*\([^)]*\)\s*', ' ', song_name)
    song_name = re.sub(r'[^\p{L}\d\s]+', ' ', song_name)
    song_name = normzlizer.norm(song_name, False, -1)
    if re.match('.*[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ].*', song_name):
        return song_name
    return song_name


def process_json():
    vi_articles = json.load(open('vi_artists_full.json', encoding='utf8'))
    for idx, artist in enumerate(vi_articles):
        process_song = set()
        for song in artist.get('song'):
            song = preprocess(song)
            process_song.add(song)
        vi_articles[idx]['song'] = list(process_song)
    with open('vi_artists_full.prep.json', 'w', encoding='utf8') as fp:
        json.dump(vi_articles, fp, ensure_ascii=False)


def process_file(filename):
    songs = []
    for song in open(filename, encoding='utf8').read().splitlines():
        songs.append(preprocess(song))
    with open(filename[:-4] + '.list', 'w', encoding='utf8') as fp:
        for song in songs:
            fp.write(song + '\n')


process_file('album_dance.txt')
process_file('album_nhactre.txt')
process_file('album_nhactrinh.txt')
process_file('album_rock.txt')
process_file('album_thieunhi.txt')
process_file('album_trutinh.txt')
