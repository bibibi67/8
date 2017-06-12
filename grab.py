#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
import time
from selenium import webdriver
def get_page(id):
    driver = webdriver.Chrome()
    driver.get('https://create.kahoot.it/#quiz/' + id);
    box = driver.find_element_by_css_selector('#username-input-field__input')
    box.send_keys('peter.a.stenger@gmail.com')
    box2 = driver.find_element_by_css_selector('#password-input-field__input')
    box2.send_keys('NOPASSWDFORU')
    driver.find_element_by_css_selector('.button--cta-play').click()
    time.sleep(2)
    elem = driver.find_element_by_xpath("//*")
    stuff = elem.get_attribute("innerHTML")
    driver.quit()
    return stuff
def start_bot(id,name,answers):
    driver = webdriver.Chrome()
    driver.get("https://kahoot.it/#/")
    time.sleep(0.25)
    box = driver.find_element_by_css_selector('#inputSession')
    box.send_keys(id)
    driver.find_element_by_css_selector('.btn-greyscale').click()
    time.sleep(1)
    box = driver.find_element_by_css_selector('#username')
    box.send_keys(name)
    driver.find_element_by_css_selector('.btn-greyscale').click()
    input("game start")
    bot_answer(driver,answers)


def bot_answer(driver,answers):
    lookuptable = {"0":"#answerA", "1":"#answerB","2":"#answerC","3":"#answerD"}
    for i in range(len(answers)):
        while True:
            try:
                driver.find_element_by_css_selector("#answer-screen")
                driver.find_element_by_css_selector(lookuptable[answers[i]]).click()
                break
            except selenium.common.exceptions.NoSuchElementException:
                pass
                #lol
            sleep(0.01)
    driver.quit()

def getQuestions(soup):
    questions = []
    stuff = soup.findAll("td", {"class":'question-title'})
    for qt in stuff:
        question = qt.find("div").get_text()
        questions.append(question.strip()[:-45])
    return questions

def getAnswers(soup,hascolor=True):

    stuff = soup.findAll("li", {"class":'answers-list__item'})
    colors = []
    answers = []
    for answer in stuff:
        if answer.find("div", {"class":'answer-label__correct-icon'}) != None:
            num = dict(answer.find("div",{"class":'answer-label'}).attrs)["class"][1][-1]
            if hascolor:
                lookuptable = {"0":"red", "1":"blue","2":"yellow","3":"green"}
                color = lookuptable[num]
                answers.append(answer.get_text().strip())
                colors.append(color)
            else:
                colors.append(num)

    return colors, answers
def printAnswers(url):
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    questions = getQuestions(soup)
    colors, answers = getAnswers(soup)
    for i in range(len(questions)):
        print("\n" + questions[i])
        print(answers[i] + "  " + colors[i])
def scrape(url):
    html = get_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    answers, _ = getAnswers(soup,hascolor=False)
    return answers
