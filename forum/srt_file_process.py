import os
import re
import sys

import pysrt


def log(text):
    sys.stdout.write(text)
    sys.stdout.flush()


dir = "/home/lap60313/data/vpbank/subtitle/film/unzip_dir/"
outdir = "/home/lap60313/data/vpbank/subtitle/film/text_dir/"
if not os.path.exists(outdir):
    os.mkdir(outdir)
for f in os.listdir(dir):
    if f.endswith('.srt') or f.endswith('.SRT'):
        path = os.path.join(dir, f)
        log('Đọc file {}\n'.format(f))
        try:
            subs = pysrt.open(path)
            with open(outdir + f, 'w', encoding='utf8') as fp:
                for sub in subs.data:
                    sub = re.sub('\n', ' ', sub.text_without_tags.strip())
                    sub = re.sub('<[^>]*>', '', sub)
                    fp.write(sub + '\n')
        except:
            pass

print('Done!')
