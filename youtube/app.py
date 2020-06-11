try:
    from youtube.configuration import *
    from youtube.discover import Discover
except:
    from configuration import *
    from discover import Discover

if PRODUCTION:
    os.environ['http_proxy'] = HTTP_PROXY
    os.environ['https_proxy'] = HTTP_PROXY

if __name__ == '__main__':
    d = Discover(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'init.url')).read().splitlines(),
                 get_data_dir())
    d.start(num_thread=7)
