from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from fblogin import email_address,password
from selenium.webdriver.firefox.options import Options
import pandas as pd

def shazam_():
    options = Options()
    options.headless = True
    url = "https://www.shazam.com"
    print ("Fetching data from Shazam")
    driver = webdriver.Firefox(executable_path="path/geckodriver",options= options)
    driver.get(url)

    #click library
    sleep(2)
    driver.find_element_by_xpath("/html/body/div[3]/header/div/div[2]/div/div/div[2]/nav/ul/li[1]/a").click()
    driver.find_element_by_xpath("/html/body/div[3]/div/main/div/div/div[2]/div[2]/a[1]").click()
    #switch window fb login
    sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    email = driver.find_element_by_xpath('//*[@id="email"]')
    email.send_keys(email_address)
    pass_ = driver.find_element_by_xpath('//*[@id="pass"]')
    pass_.send_keys(password)
    driver.find_element_by_xpath('//*[@id="u_0_0"]').click()
    sleep(10)
    #back to shazam
    driver.switch_to.window(driver.window_handles[0])

    #Fetch song names and artist names
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    sleep(1.5)
    song_names = [song.text for song in  driver.find_elements_by_class_name("title")]
    artist_names = [artist.text for artist in driver.find_elements_by_class_name("artist")]
    song_names = list(filter(None, song_names))
    driver.close()
    data = pd.DataFrame({
        "SongName": song_names,
        "ArtistName": artist_names,
    })

    data.to_csv("songartist.csv")

    return "Done"

