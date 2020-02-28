import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel/{}/videos"
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v={}"
RE_VIDEO_ID = re.compile("\"/watch\?v=(.{11})\"")


class GetAllVideoID:
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=options)

    def get_all_video(self, channel_id):
        self.driver.get(YOUTUBE_CHANNEL_URL.format(channel_id))
        num_video = 0
        body = self.driver.find_element_by_css_selector('body')
        while True:
            # Scroll down to the bottom.
            for i in range(5):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            new_num_video = len(self.driver.find_elements_by_css_selector("#items > ytd-grid-video-renderer"))
            # print(str(num_video), str(new_num_video))
            if num_video == new_num_video:
                break
            num_video = new_num_video
        ids = set(re.findall(RE_VIDEO_ID, self.driver.page_source))
        return list(ids)


if __name__ == '__main__':
    USAGE = """
    ###############################################
        # Cách chạy: 
            python3 GetAllVideoIDFromChannel.py <channel_id> <output_file_path>
        # Cách tìm VIDEO_ID: 
            https://www.youtube.com/channel/UCXZmbAtoaB3tpnXsuQ5Lj8w/videos 
            => Video ID: UCXZmbAtoaB3tpnXsuQ5Lj8w
        # Ví dụ: 
            python3 GetAllVideoIDFromChannel.py UCXZmbAtoaB3tpnXsuQ5Lj8w output.txt
    ###############################################
    """
    channel_id = ''
    output_file = ''
    getAllVideo = GetAllVideoID()
    if len(sys.argv) < 3:
        print(USAGE)
        sys.exit(1)
    try:
        channel_id = sys.argv[1]
        output_file = sys.argv[2]
        ids = getAllVideo.get_all_video(channel_id)
        with open(output_file, 'w', encoding='utf8') as fp:
            for id in ids:
                fp.write(YOUTUBE_VIDEO_URL.format(id) + "\n")
    except:
        sys.exit(2)
    finally:
        getAllVideo.driver.close()
