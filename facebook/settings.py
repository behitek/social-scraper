PRODUCTION = False
HEADLESS = True
# Sever deploy, no screen
if PRODUCTION:
    USE_VIRTUAL_DISPLAY = True
    # USE PROXY
    PROXY = 'http://10.30.58.36:81'
    FAKE_LOCATION = True
else:
    FAKE_LOCATION = False
    USE_VIRTUAL_DISPLAY = False
    # USE PROXY
    PROXY = None
# Set random delay time between min and max before call next request
MIN_DELAY_TIME = 1
MAX_DELAY_TIME = 1



