import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
import pandas as pd
import glob

class TestSavingthings():
  def setup_method(self):
    #firefox_options = Options()
    #service = Service(GeckoDriverManager().install())
    #self.driver =  webdriver.Firefox(service=service, options=firefox_options)
    self.driver = webdriver.Chrome()
  def teardown_method(self):
    self.driver.quit()
  
  def test_savingthings(self):
    self.driver.get("https://www.webofscience.com/wos/woscc/basic-search")
    while True:
      try:
        self.driver.find_element(By.ID, "onetrust-reject-all-handler").click()
        break
      except:
          time.sleep(0.5)
    while True:
      try:
        self.driver.find_element(By.LINK_TEXT, "Advanced search").click()
        break
      except:
          time.sleep(0.5)

    while True:
      try:
        self.driver.find_element(By.ID, "advancedSearchInputArea").click()
        break
      except:
          time.sleep(0.5)
    
    self.driver.find_element(By.ID, "advancedSearchInputArea").send_keys("((TI=(6G) OR AK=(6G)) AND (TI=(spectrum management) OR TI=(network slicing) OR TI=(network management) OR TI=(channel estimation) OR TI=(channel management)  OR TI=(user mobility)  OR TI=(user positioning)  OR TI=(content caching)  OR TI=(computation allocation)  OR TI=(energy efficiency)  OR TI=(traffic management)  OR TI=(resource management) OR AK=(spectrum management) OR AK=(network slicing) OR AK=(network management) OR AK=(channel estimation) OR AK=(channel management)  OR AK=(user mobility)  OR AK=(user positioning)  OR AK=(content caching)  OR AK=(computation allocation)  OR AK=(energy efficiency)  OR AK=(traffic management)  OR AK=(resource management)) AND ( TI=(Machine Learning) OR TI=(Supervised Learning)  OR TI=(Unsupervised Learning)  OR TI=(reinforcement learning)  OR TI=(neural network)  OR TI=(multi-layer perception)  OR TI=(convolutional neural network)  OR TI=(recurrent neural network) OR AK=(Machine Learning) OR AK=(Supervised Learning)  OR AK=(Unsupervised Learning)  OR AK=(reinforcement learning)  OR AK=(neural network)  OR AK=(multi-layer perception)  OR AK=(convolutional neural network)  OR AK=(recurrent neural network) ) NOT (TI=(review) OR TI=(survey) OR TI=(systematic review)))")
    self.driver.find_element(By.CSS_SELECTOR, ".add-timespan-row > .mat-button-wrapper").click()
    while True:
      try:
        self.driver.find_element(By.CSS_SELECTOR, ".timespan-select-holder > .dropdown").click()
        break
      except:
          time.sleep(0.5)

    while True:
      try:
        self.driver.find_element(By.CSS_SELECTOR, ".wrap-mode:nth-child(3) > span").click()
        break
      except:
        time.sleep(0.5)
    while True:
      try:
        self.driver.find_element(By.CSS_SELECTOR, ".query-adv-search-row > .button-row").click()
        break
      except Exception as e:
        print(e)
        time.sleep(0.5)
    element = self.driver.find_element(By.CSS_SELECTOR, ".adv > .search")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".full-record-breadcrumbs-styles > .mat-button-wrapper").click()
    self.driver.find_element(By.ID, "exportToExcelButton").click()
    self.driver.find_element(By.CSS_SELECTOR, "#radio3 .mat-radio-label-content").click()
    self.driver.find_element(By.CSS_SELECTOR, ".mat-flat-button .ng-star-inserted").click()
    while True:
      try:
        self.driver.find_element(By.ID, "mat-checkbox-2").click()
        break
      except Exception as e:
        time.sleep(0.5)
    time.sleep(10)

#test = TestSavingthings()
#test.setup_method()
#try:
#  test.test_savingthings()
#except Exception as e:
#  print(e)
#finally:
#  test.teardown_method()

# Path where your CSV files are located
path = "/home/user/Downloads/savedrecs.xls"  # Replace with your directory path

# Use glob to find all files starting with 'export' and ending with '.csv'
# Read and concatenate all files
dataframe = pd.read_excel(path) 

# Save the concatenated DataFrame to a new CSV file (optional)
dataframe.to_csv("wos_export.csv", index=False)

