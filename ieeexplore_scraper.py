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
    firefox_options = Options()
    service = Service(GeckoDriverManager().install())
    self.driver =  webdriver.Firefox(service=service, options=firefox_options)
  
  def teardown_method(self):
    self.driver.quit()
  
  def test_savingthings(self):
    self.driver.get("https://ieeexplore.ieee.org//Xplore/home.jsp")
    
    self.driver.find_element(By.CSS_SELECTOR, ".advanced-search-div span").click()
    WebDriverWait(self.driver, 100).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Command Search"))
    )
    self.driver.find_element(By.LINK_TEXT, "Command Search").click()
    WebDriverWait(self.driver, 100).until(
        EC.presence_of_element_located((By.ID, "cmdTextArea"))
    )
    while True:
      try:
        element = self.driver.find_element(By.ID, "cmdTextArea")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        break
      except:
        time.sleep(0.5)
    element.click()
    self.driver.find_element(By.ID, "cmdTextArea").send_keys('(("Document Title":"6G" OR  "Index Terms":"6G") AND ("Document Title":"Channel management" OR "Document Title":"Spectrum Management" OR "Document Title":"Network Slicing" OR "Document Title":"Network Magement" OR "Document Title":"Channel Estimation" OR "Document Title":"Channel Management" OR "Document Title":"User Mobility" OR "Document Title":"User Positioning" OR "Document Title":"Content Caching" OR "Document Title":"Computation Allocation" OR "Document Title":"Energy efficiency" OR "Document Title":"Resource Management" OR "Document Title":"Traffic Management" OR "Index Terms":"Channel management" OR "Index Terms":"Spectrum Management" OR "Index Terms":"Network Slicing" OR "Index Terms":"Network Magement" OR "Index Terms":"Channel Estimation" OR "Index Terms":"Channel Management" OR "Index Terms":"User Mobility" OR "Index Terms":"User Positioning" OR "Index Terms":"Content Caching" OR "Index Terms":"Computation Allocation" OR "Index Terms":"Energy efficiency" OR "Index Terms":"Resource Management" OR "Index Terms":"Traffic Management" ) AND ("Document Title":"Machine Learning" OR "Document Title":"Artificial Intelligence" OR "Document Title":"Supervised Learning" OR "Document Title":"Unsupervised Learning" OR "Document Title":"Reinforcement Learning" OR "Document Title":"Neural Network" OR "Document Title":"Multi-Layer Perceptron" OR "Document Title":"Convolutional neural network" OR "Document Title":"recurrent neural network" OR "Index Terms":"Machine Learning" OR "Index Terms":"Artificial Intelligence" OR "Index Terms":"Supervised Learning" OR "Index Terms":"Unsupervised Learning" OR "Index Terms":"Reinforcement Learning" OR "Index Terms":"Neural Network" OR "Index Terms":"Multi-Layer Perceptron" OR "Index Terms":"Convolutional neural network" OR "Index Terms":"recurrent neural network") NOT ("Document Title":"survey" OR "Document Title":"Systematic Review" OR "Document Title":"Review"))')
    self.driver.find_element(By.CSS_SELECTOR, ".stats-Adv_Command_search").click()
    while True:
      try:
        self.driver.find_element(By.ID, "dropdownPerPageLabel").click()
        break
      except:
        time.sleep(0.5)
    self.driver.find_element(By.CSS_SELECTOR, ".show > .dropdown-item:nth-child(5)").click()
    
    #Filter by year and download
    for year in ["2020", "2021", "2022", "2023", "2024", "2025"]:
      while True:
        try:
          element = self.driver.find_element(By.CSS_SELECTOR, ".col-6:nth-child(1) .text-normal-md")
          self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
          element.click()
          break
        except:
          time.sleep(0.5)
      actions = ActionChains(self.driver)
      actions.double_click(element).perform()
      element.send_keys(year)
      element = self.driver.find_element(By.CSS_SELECTOR, ".col-6:nth-child(2) .text-normal-md")
      element.click()
      actions = ActionChains(self.driver)
      actions.double_click(element).perform()
      element.send_keys(year)
      self.driver.find_element(By.ID, "Year-apply-btn").click()
      i= 2
      pages_left = True
      while pages_left:
        while True:
          try:
            element = self.driver.find_element(By.CSS_SELECTOR, ".results-actions-selectall-checkbox")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            break
          except:
            time.sleep(0.5)
        element = self.driver.find_element(By.CSS_SELECTOR, "xpl-export-search-results > .xpl-btn-primary")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        self.driver.find_element(By.CSS_SELECTOR, ".stats-SearchResults_Download").click()
        tries = 0
        while True:
          if tries > 100:
            pages_left = False
            break
          try:
            element = self.driver.find_element(By.CSS_SELECTOR, f".stats-Pagination_arrow_next_{i}")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
            break
          except:
            tries += 1
            time.sleep(0.5)
        i += 1
      element = self.driver.find_element(By.CSS_SELECTOR, ".xpl-btn-text:nth-child(1)")
      self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
      element.click()
    
test = TestSavingthings()
test.setup_method()
try:
  test.test_savingthings()
except Exception as e:
  print(e)
finally:
  test.teardown_method()

# Path where your CSV files are located
path = "/home/user/Downloads"  # Replace with your directory path

# Use glob to find all files starting with 'export' and ending with '.csv'
csv_files = glob.glob(f"{path}/export*.csv")

# Read and concatenate all files
dataframes = [pd.read_csv(file) for file in csv_files]
concatenated_df = pd.concat(dataframes, ignore_index=True)

# Save the concatenated DataFrame to a new CSV file (optional)
concatenated_df.to_csv("ieeexplore_export.csv", index=False)

print("Files concatenated successfully!")