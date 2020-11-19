import logging
import os
from random import random

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    netid = os.getenv("netid")
    password = os.getenv("password")
    config = webdriver.ChromeOptions()
    config.headless = True
    driver = webdriver.Chrome(config)
    driver.get("http://jkrb.xjtu.edu.cn/EIP/user/index.htm")
    wait = WebDriverWait(driver=driver, timeout=10)
    wait.until((EC.url_contains("org.xjtu.edu.cn")))
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/input[1]'))
    )
    elem.send_keys(netid)
    elem = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="form1"]/input[2]'))
    )
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)
    wait.until(EC.url_contains("jkrb.xjtu.edu.cn"))
    logger.info("Successful Login")

    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload2()']")
    driver.switch_to.frame(iframe)

    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload1()']")
    driver.switch_to.frame(iframe)
    elem = driver.find_element_by_xpath("//div[@title='本科生每日健康状况填报']")
    elem.click()

    driver.implicitly_wait(1)
    driver.switch_to.default_content()
    driver.implicitly_wait(1)
    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload3()']")
    driver.switch_to.frame(iframe)
    elem = driver.find_element_by_xpath("//li[@data-blname='每日健康填报']")
    elem.click()
    driver.implicitly_wait(1)
    driver.switch_to.default_content()
    driver.implicitly_wait(1)
    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload4()']")
    driver.switch_to.frame(iframe)
    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload1()']")
    driver.switch_to.frame(iframe)

    driver.find_element_by_xpath("//input[@value='绿色']").click()
    driver.find_element_by_xpath("//input[@id='mini-4$ck$0']").click()
    driver.find_element_by_xpath("//input[@placeholder='请准确填写体温，格式如:36.5']").send_keys(
        str(round(36 + random(), 1))
    )

    driver.switch_to.default_content()
    driver.implicitly_wait(1)
    iframe = driver.find_element_by_xpath("//iframe[@onload='__iframe_onload4()']")
    driver.switch_to.frame(iframe)
    submit_btn = driver.find_element_by_xpath("//a[@id='sendBtn']")
    submit_btn.click()
    driver.find_element_by_xpath("//*[@id='mini-17']").click()
    logger.info("Successful submit!")


if __name__ == "__main__":
    main()