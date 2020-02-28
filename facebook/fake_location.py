import time

from selenium import webdriver

profile = webdriver.FirefoxProfile()
# We set the coordinate of where we want to be.
profile.set_preference("geo.wifi.uri",
                       'data:application/json,{"location": {"lat": 21.022642, "lng":105.778937}, "accuracy": 90.0}')
# This line is necessary to avoid to prompt for geolocation authorization.
profile.set_preference("geo.prompt.testing", True)
my_driver = webdriver.Firefox(profile)
my_driver.get("https://maps.google.com/")
# Let's use code to click the blue button.
time.sleep(20)
my_driver.quit()
