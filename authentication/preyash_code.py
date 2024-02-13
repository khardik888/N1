from pyPMClient_master.pmClient.pmClient import PMClient
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
import sys
import time
import pyotp
import config
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def pm_access_token():
  access_token = None

  if r.get('paytm_money_access_token'):
    access_token = r.get('paytm_money_access_token')
  else:
    pm = PMClient(api_key=config, api_secret=constants.PM_API_SECRET)
    data = pm.generate_session(get_request_token())
    access_token = data.get('access_token')
    r.set('paytm_money_access_token', access_token)
    r.expire('paytm_money_access_token', 75600)

  logging.info(f"Access Token: {access_token}")
  return access_token

def get_request_token():
  driver = Driver(uc=True)
  driver.get(f'https://login.paytmmoney.com/merchant-login?apiKey={constants.PM_API_KEY}')

  login_id = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(by=By.XPATH, value='//input[@type="text"]'))
  login_id.send_keys(constants.PM_USERNAME)

  pwd = WebDriverWait(driver, 10).until(
    lambda x: x.find_element(by=By.XPATH, value='//input[@type="password"]'))
  pwd.send_keys(constants.PM_PASSWORD)

  print(driver.page_source)

  submit = WebDriverWait(driver, 10).until(lambda x: x.find_element(
    by=By.XPATH,
    value="//button[text()='Sign In']"))
  submit.click()

  time.sleep(3)

  totp_fields = WebDriverWait(driver, 10).until(lambda x: x.find_elements(
    by=By.XPATH,
    value='//input[@type="password"]'))

  totp = pyotp.TOTP(constants.PM_TOTP_SECRET).now()

  print(driver.page_source)

  for i, field in enumerate(totp_fields):
    print(totp[i])
    field.send_keys(totp[i])

  otp_submit = WebDriverWait(driver, 10).until(lambda x: x.find_element(
    by=By.XPATH,
    value="//button"))
  otp_submit.click()

  time.sleep(5)

  url = driver.current_url
  print(url)
  initial_token = url.split('requestToken=')[1]
  request_token = initial_token.split('&')[0]
  driver.quit()

  return request_token