import time
import io
from PIL import Image
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def removeWords(dictionary, letter, location):
    newDictionary = []
    for word in dictionary:
        if location == None:
            if letter in word:
                continue
        elif len(location) > 1:
            isCorrect = False
            for index in location:
                if word[index] == letter:
                    isCorrect = True
                    break
            if not isCorrect:
                continue
        else:
            if word[location[0]] != letter:
                continue
        newDictionary.append(word)
    return newDictionary

def openWordle():
    s = Service("geckodriver.exe", log_path="NUL")
    browser = Firefox(service=s)
    browser.set_window_rect(0, 0, 500, 800)
    browser.get('https://www.powerlanguage.co.uk/wordle/')

    time.sleep(0.5)
    browser.find_element(By.XPATH, "/html/body").click()
    return browser

    pass

def enterWord(browser, word):
    for letter in word:
        browser.find_element(By.XPATH, "/html/body").send_keys(letter)
        time.sleep(0.2)
    browser.find_element(By.XPATH, "/html/body").send_keys(Keys.ENTER)
    time.sleep(2)
    browser.set_window_rect(0, 0, 500, 800)
    return browser.get_screenshot_as_png()

def checkWebAnswer(guess, screenshot, row):
    letters = {}
    image = Image.open(io.BytesIO(screenshot))
    for column in range(5):
        r, g, b, a = image.getpixel((117 + (column*84), 118 + (row * 85)))

        if r == 83 and b == 78 and g == 141:
            letters[guess[column]] = [column]
        elif r == 181 and b == 59 and g == 159:
            locations = [0,1,2,3,4]
            locations.remove(column)
            letters[guess[column]] = locations
        else:
            letters[guess[column]] = None

    return letters

if __name__ == '__main__':
    browser = openWordle()
    words = []
    validWords = []
    with open("5-letter-words.txt", "r") as f:
        words = f.readlines()
    words = list(map(str.strip, words))

    for word in words:
        if len(word) == 5:
            validWords.append(word)

    for guesses, word in enumerate(["bring", "claps", "sweat", "joked", "tramp"]):
        result = enterWord(browser, word)
        checkWebAnswer(word, result, guesses)
        for letter, value in checkWebAnswer(word, result, guesses).items():
            validWords = removeWords(validWords, letter, value)

        if len(validWords) == 1:
            enterWord(browser, validWords[0])
            break
