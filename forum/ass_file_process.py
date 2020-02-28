import os
import re
import sys
import traceback

import pysubs2

def log(text):
    sys.stdout.write(text)
    sys.stdout.flush()


dir = "/home/lap60313/data/vpbank/subtitle/film/unzip_dir/"
outdir = "/home/lap60313/data/vpbank/subtitle/film/text_dir/"
if not os.path.exists(outdir):
    os.mkdir(outdir)
for f in os.listdir(dir):
    if f.endswith('.ass'):
        path = os.path.join(dir, f)
        log('Đọc file {}\n'.format(f))
        try:
            subs = pysubs2.load(path, encoding='utf8')
            with open(outdir + f, 'w', encoding='utf8') as fp:
                for sub in subs.events:
                    sub = re.sub('\n', ' ', sub.plaintext.strip())
                    sub = re.sub('<[^>]*>', '', sub)
                    fp.write(sub + '\n')
        except:
            traceback.print_exc()

print('Done!')