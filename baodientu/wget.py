import argparse
import os
import sys


def wget_download(download_url, resources_file):
    os.system("wget \"{}\" -O {}".format(download_url, resources_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download video tools')
    parser.add_argument('--input', default=None, required=True, help='Video URL File')
    parser.add_argument('--output', default=None, help='Save video dir')

    try:
        options = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    SAVE_PATH = options.output
    if SAVE_PATH is None:
        SAVE_PATH = options.input[:-4]

    print('OUTPUT_DIR:', SAVE_PATH)

    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    for url in open(options.input, encoding='utf8').readlines():
        url = url.strip()
        file_name = os.path.join(SAVE_PATH, url.split("/")[-1])
        if os.path.exists(file_name):
            continue
        wget_download(url, file_name)
