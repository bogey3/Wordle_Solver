import random
import time
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
    browser.get('https://www.nytimes.com/games/wordle/index.html')

    time.sleep(1)
    browser.find_element(By.XPATH, "//button[@aria-label=\"Close\"]").click()
    time.sleep(0.5)
    try:
        browser.execute_script("document.getElementById(\"top\").remove()")
    except:
        pass
    return browser

    pass

def enterWord(browser, word):
    for letter in word:
        browser.find_element(By.XPATH, "/html/body").send_keys(letter)
        time.sleep(0.2)
    browser.find_element(By.XPATH, "/html/body").send_keys(Keys.ENTER)
    time.sleep(2)
    return

def checkWebAnswer(guess, row):

    lettersData = browser.find_elements(By.XPATH, "//div[@aria-label=\"Row {}\"]//div[@aria-roledescription=\"tile\"]".format(row+1))
    letters = {}

    for column, letter in enumerate(lettersData):
        value = letter.get_attribute("data-state")
        if value == "correct":
            letters[guess[column]] = [column]
        elif value == "present":
            locations = [0,1,2,3,4]
            locations.remove(column)
            letters[guess[column]] = locations
        else:
            letters[guess[column]] = None

    return letters

def countFoundLetters(letters):
    found = 0
    for letter, locations in letters.items():
        if locations != None:
            found += 1
    return found

if __name__ == '__main__':
    browser = openWordle()
    words = []
    validWords = []
    letters = {}
    with open("5-letter-words.txt", "r") as f:
        words = f.readlines()
    words = list(map(str.strip, words))
    validWords = words


    for guesses, word in enumerate(["train", "chose", "drums", "felty", "kapow"]):
        if countFoundLetters(letters) == 5:
            word = random.choice(validWords)
        enterWord(browser, word)
        newLetters = checkWebAnswer(word, guesses)
        for letter, value in newLetters.items():
            if value == None or len(value) == 1 or letter not in letters:
                letters[letter] = value
            elif value != letters[letter]:
                    oldLocations = letters[letter]
                    letters[letter] = []
                    for location in value:
                        if location in oldLocations:
                            letters[letter].append(location)

        for letter in newLetters.keys():
            validWords = removeWords(validWords, letter, letters[letter])

        if len(validWords) == 1:
            enterWord(browser, validWords[0])
            break
    if len(validWords) > 1:
        browser.execute_script("alert('I was not able to find the word, here are the possible words:\\n" + "\\n".join(validWords) + "')")

