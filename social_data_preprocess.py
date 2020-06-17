import sys

import emoji
import regex as re
from nlp_utils import convert_window1252_to_utf8

BREAK_LINE = "---END_COMMENT---"

teencode_dict = {}

for line in open('resources/teencode').read().splitlines():
    parts = line.split('\t')
    if len(parts) == 2:
        if parts[0] in teencode_dict:
            print('WARN: Found duplicate key {}'.format(parts[0]))
        teencode_dict[parts[0]] = parts[1]


def preprocess_sentence(sentence):
    # convert to utf8 encoding
    sentence = convert_window1252_to_utf8(sentence)
    # remove inside () and brackets
    sentence = re.sub(r'\([^\)]*\)', '', sentence)
    # teencode
    sentence = replace_teencode(sentence)
    sentence = re.sub(r'^\p{P}+', '', re.sub(r'\p{P}+$', '', sentence))
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence


def replace_teencode(sentence):
    # NOTE: keep punct position
    words = sentence.split()
    for iw, word in enumerate(words):
        word_parts = re.split('#{3}', re.sub(r'^(\p{P}*)', r'\1###', re.sub(r'(\p{P}*)$', r'###\1', word)))
        if word_parts[1] in teencode_dict:
            word_parts[1] = teencode_dict.get(word_parts[1])
        words[iw] = ''.join(word_parts)
    return ' '.join(words)


def replace_special_char(text):
    text = text.replace('ð', 'đ')
    text = text.replace(' ?& ?', ' và ')
    text = re.sub(r'[“”"\'\)\(\[\]\{\}]', '', text)
    text = re.sub(r'<U\+200B>', ' ', text)
    # remove zero width space
    text = re.sub('​', ' ', text)
    return text


def preprocess_text(text):
    text = replace_special_char(text)
    text = re.sub('\n+', '\n', text)
    text = remove_emoij(text)
    # remove url, email
    text = re.sub(r'https?://[^ ]+', '<url>', text)
    text = re.sub(r'[a-zA-Z][\w.]+@[A-Za-z0-9]+\.[^ ]+', '<email>', text)
    # ...
    text = re.sub(r'(\p{L}+)\.{3} ?', r'\1 ', text)
    text = re.sub(r'… ?', r' ', text)
    return text


def remove_emoij(text):
    allchars = [char for char in text]
    emoji_list = [char for char in allchars if char in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([word for word in text.split() if not any(char in word for char in emoji_list)])
    return clean_text


def to_sentences(text):
    text = preprocess_text(text)
    # split
    text = re.sub(r'(\n|[\.!?;] )', r'\1 <newline>', text)
    return [x.strip() for x in re.split(r' <newline>', text) if x.strip()]


if __name__ == '__main__':
    inp = sys.argv[1]
    out = inp + ".out"
    print('INP: {}\nOUT: {}'.format(inp, out))
    text = ""
    current_line = 0
    with open(out, 'w') as fp:
        for line in open(inp):
            if line.startswith(BREAK_LINE):
                current_line += 1
                if current_line % 1000 == 0:
                    print('INFO Current line is {}'.format(current_line))
                sentences = to_sentences(text)
                text = ""
                for sentence in sentences:
                    sentence = preprocess_sentence(sentence)
                    if len(sentence) > 10:
                        fp.write(sentence + '\n')
            else:
                text += line
    print('Done.')
