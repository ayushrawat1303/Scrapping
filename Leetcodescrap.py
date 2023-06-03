from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By as by

siteUrl = "https://leetcode.com/problems/"
pagetitle= "Problems - LeetCode"

body_class = ".px-5.pt-4"
heading_class = ".mr-2.text-label-1"

questionNameList = []
questionUrlList = []
questionDifficultyList = []

index_num = 1
def writeToFile():
    file = open('questionsLink.txt','w')
    for x in range(questionUrlList.__len__()):
        file.write(questionUrlList[x]+"\n")
    file.close()

# using selenium for opening browser(basically selenium is used for doing automated tasks related to browser)
def openBrowser(url):
    print("     -----------> Opening Browser")
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--incognito')
    options.add_argument('--headless')

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # headless browser(headless browser means that browser won't open the browser externally but use it internally)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              options=options)

    driver.get(url)
    driver.maximize_window()
    return driver

def closeBrowser(driver):
    print("     -----------> Closing Browser")
    driver.quit()

# fetching data using Beautiful soup
def fetchPageData(pageUrl):
    sleepTime = 3

    # print("Page URL: ", pageUrl)
    browser = openBrowser(pageUrl)
    time.sleep(sleepTime)
    pageSource = browser.page_source
    print(browser.title)
    WebDriverWait(browser, 10).until(EC.title_contains(pagetitle))
    # print(f"title is: {browser.title}")

    soup = BeautifulSoup(pageSource, 'html.parser')
    if (browser.title == pagetitle):
        print(
            "\n\n                     ------------------- Parsing data -------------------\n\n"
        )
        newSoup = BeautifulSoup(pageSource, 'html.parser')
        questionBlock = newSoup.find('div', role='rowgroup')
        questionList = questionBlock.find_all('div', role='row')
        # print(f"Total {questionList.len()} data fetched ")

        for question in questionList:
            row = question.find_all('div', role='cell')
            questionName = row[1].find('a').text
            questionUrl = row[1].find('a')['href']
            questionUrl = 'https://leetcode.com' + questionUrl
            questionDifficulty = row[4].find('span').text
            questionNameList.append(questionName)
            questionUrlList.append(questionUrl)
            questionDifficultyList.append(questionDifficulty)
            # print(questionName, questionUrl, questionDifficulty)
        print("     -----------> Done")
        closeBrowser(browser)

    else:
        print("Page does not exist o connection Failed, status code: ",
              soup.status_code)
    return


def getData():

    try:
        browser = openBrowser(siteUrl)
        time.sleep(2)
        pageSource = browser.page_source
        print(browser.title)    
        WebDriverWait(browser, 10).until(EC.title_contains(pagetitle))
        soup = BeautifulSoup(pageSource, 'html.parser')

        if (browser.title == pagetitle):
            # Fetching total number of pages
            totalQuestions = soup.find('nav', role="navigation" ,class_="mb-6 md:mb-0 flex flex-nowrap items-center space-x-2")
            index = totalQuestions.__len__() - 2
            totalPages = int(totalQuestions.contents[index].text)
            print("Total Pages : ", totalPages)
            closeBrowser(browser)
            # Fetching data from each page
            for page in range(1, totalPages + 1):
                print(
                    f"\n\n                     ------------------- Fetching Page {page} -------------------\n\n"
                )
                pageUrl = siteUrl + '?page=' + str(page)
                fetchPageData(pageUrl)

            print("     -----------> Done all pages ")
            print(f"Total {questionNameList.__len__()} questions fetched")
            writeToFile()
        else:
            print("Connection Failed")
            return

    except Exception as e:
        print("Some error occured, error: ", e)
        return


if __name__ =="__main__":
    getData()