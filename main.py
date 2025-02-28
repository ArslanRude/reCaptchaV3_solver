import os
import time
import urllib
from groq import Groq
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

def reCaptcha_solver(query):
    options = webdriver.ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument("--incognito")
    options.add_argument(f'--user-agent={user_agent}')
    # options.add_argument('--headless')
    options.add_argument("--window-size=1420,980")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()
    driver.switch_to.default_content()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@title, 'recaptcha challenge')]")))
    audio_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-audio-button")))
    audio_button.click()
    time.sleep(1)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@id, ':2')]")))
    button.click()


    src = driver.find_element(By.ID , "audio-source").get_attribute("src")
    print(f"[INFO] Audio src: {src}")

    path_to_mp3 = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))
    path_to_wav = os.path.normpath(os.path.join(os.getcwd(), "sample.wav"))

    urllib.request.urlretrieve(src, path_to_mp3)

    client = Groq(api_key="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")
    filename = os.path.normpath(os.path.join(os.getcwd(), "sample.mp3"))

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()), # Required audio file
        model="whisper-large-v3-turbo", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        response_format="json",  # Optional
        language="en",  # Optional
        temperature=0.0  # Optional
        )
    key = transcription.text

    driver.find_element(By.ID, "audio-response").send_keys(key.lower())
    driver.find_element(By.ID, "audio-response").send_keys(Keys.ENTER)
    time.sleep(5)
    driver.switch_to.default_content()
    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    try:
        q = input("Enter Query : ")
        reCaptcha_solver(q)
    except:
        print("Error Occure.")