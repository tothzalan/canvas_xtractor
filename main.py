import os
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


load_dotenv()

url = os.environ.get("URL")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

assert url is not None, "URL is not set"
assert username is not None, "Username is not set"
assert password is not None, "Password is not set"

driver = webdriver.Chrome()

if not (url.endswith("/quizzes") or url.endswith("/quizzes/")):
    if url[-1] == "/":
        url += "quizzes"
    else:
        url += "/quizzes"
driver.get(url)


driver.find_element(By.XPATH, '//b[text()="Belépés Neptun hozzáféréssel"]').click()
driver.find_element(By.XPATH, '//input[@name="username_neptun"]').send_keys(username)
driver.find_element(By.XPATH, '//input[@name="password_neptun"]').send_keys(password)
driver.find_element(By.CLASS_NAME, "submit-button").click()


data: list = []

quiz_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/quizzes/")]')
quiz_links = [
    element.get_attribute("href")
    for element in quiz_elements
    if element.get_attribute("href")
]

for link in quiz_links:
    if link is None:
        continue
    driver.get(link)

    question_texts = [
        element.text.strip()
        for element in driver.find_elements(By.CLASS_NAME, "question_text")
    ]
    selected_answers = [
        element.text.strip()
        for element in driver.find_elements(By.CLASS_NAME, "selected_answer")
    ]

    for question_text, selected_answer in zip(question_texts, selected_answers):
        data.append({"q": question_text, "a": selected_answer})

    driver.get(url)
    sleep(5)


with open("data.json", "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

driver.close()
