
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import glob
import pandas as pd

class TestSearch():
  def setup_method(self):
    #self.driver = webdriver.Firefox()
    self.driver = webdriver.Chrome()

    self.vars = {}
  
  def teardown_method(self):
    self.driver.quit()
  
  def test_search(self):
    self.driver.get("https://www.scopus.com/search/form.uri?display=basic")
    time.sleep(10)
    #self.driver.set_window_size(1920, 1056)
    while True:
      try:
        self.driver.find_element(By.CSS_SELECTOR, ".Stack-module__tT3r4:nth-child(2) > .Stack-module__tT3r4 > .Stack-module__tT3r4 > .Button-module__f8gtt > .Typography-module__lVnit").click()
        break
      except:
        time.sleep(0.5)
    element = self.driver.find_element(By.ID, "searchfield")
    self.driver.execute_script("if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'TITLE ( 6g ) AND ( TITLE ( channel AND management ) OR TITLE ( spectrum AND management ) OR TITLE ( network AND slicing ) OR TITLE ( network AND management ) OR TITLE ( channel AND estimation ) OR TITLE ( user AND mobility ) OR TITLE ( user AND positioning ) OR TITLE ( content AND caching ) OR TITLE ( computation AND allocation ) OR TITLE ( energy AND efficiency ) OR TITLE ( resource AND management ) OR TITLE ( traffic AND management ) OR KEY ( channel AND management ) OR KEY ( spectrum AND management ) OR KEY ( network AND slicing ) OR KEY ( network AND management ) OR KEY ( channel AND estimation ) OR KEY ( user AND mobility ) OR KEY ( user AND positioning ) OR KEY ( content AND caching ) OR KEY ( computation AND allocation ) OR KEY ( energy AND efficiency ) OR KEY ( resource AND management ) OR KEY ( traffic AND management ) ) AND ( TITLE ( machine AND learning ) OR TITLE ( supervised AND learning ) OR TITLE ( unsupervised AND learning ) OR TITLE ( reinforcement AND learning ) OR TITLE ( neural AND network ) OR TITLE ( multi-layer AND perceptron ) OR TITLE ( convolutional AND neural AND network ) OR TITLE ( recurrent AND neural AND network ) OR KEY ( machine AND learning ) OR KEY ( supervised AND learning ) OR KEY ( unsupervised AND learning ) OR KEY ( reinforcement AND learning ) OR KEY ( neural AND network ) OR KEY ( multi-layer AND perceptron ) OR KEY ( convolutional AND neural AND network ) OR KEY ( recurrent AND neural AND network ) ) AND NOT ( TITLE ( survey ) OR TITLE ( systematic AND review ) OR TITLE ( review ) )'}", element)
    self.driver.find_element(By.CSS_SELECTOR, "#advSearch > .btnText").click()
    for i in range(1,7):
        while True:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, ".RadioButton-module__f86bj:nth-child(2)")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                element.click()
                break
            except Exception as e:
                time.sleep(0.5)
        
        while True:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".FacetItems-module__gD1qd .Button-module__nc6_8 > .Typography-module__lVnit").click()
                break
            except:
                time.sleep(0.5)
        while True:
            try:
                self.driver.find_element(By.CSS_SELECTOR, f".show-all-checkbox-facet .Checkbox-module__jE3jb:nth-child({i})").click()
                break
            except:
                time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, ".Button-module__LfG4O:nth-child(2) > .Typography-module__lVnit").click()
        self.driver.execute_script("window.scrollTo(0,958)")
        while True:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, ".SearchResultsHeader-module__Qq2ZF > div > .Typography-module__lVnit")
                break
            except:
                time.sleep(0.5)
        time.sleep(5)
        limit = int(element.text.split(" ")[0].replace(",", ""))
        self.driver.find_element(By.CSS_SELECTOR, ".export-dropdown .Typography-module__lVnit").click()
        while True:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".Stack-module___CTfk:nth-child(1) > .Button-module__MlsfC:nth-child(2) > .Typography-module__lVnit").click()
                break
            except:
                time.sleep(0.5)
        self.driver.find_element(By.ID, "field_group_authors").click()
        self.driver.find_element(By.ID, "field_group_eid").click()
        self.driver.find_element(By.ID, "field_group_sourceTitle").click()
        self.driver.find_element(By.ID, "field_group_volumeIssuePages").click()
        self.driver.find_element(By.ID, "field_group_citedBy").click()
        self.driver.find_element(By.ID, "field_group_publicationStage").click()
        self.driver.find_element(By.ID, "field_group_openAccess").click()
        self.driver.find_element(By.ID, "field_group_serialIdentifiers").click()
        self.driver.find_element(By.ID, "select-range").click()
        while True:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, ".Stack-module__tT3r4:nth-child(2) > .Stack-module__tT3r4 > .styleguide-input-module__VN7hv:nth-child(1) .styleguide-input-module__SOgqZ")
                break
            except:
                time.sleep(0.5)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        element.send_keys(1)
        element = self.driver.find_element(By.CSS_SELECTOR, ".Stack-module__tT3r4:nth-child(2) > .Stack-module__tT3r4 > .styleguide-input-module__VN7hv:nth-child(2) .styleguide-input-module__SOgqZ")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        element.send_keys(limit)

        while True:
            try:
                self.driver.find_element(By.CSS_SELECTOR, ".Typography-module__lVnit > .Stack-module__tT3r4").click()
                break
            except:
                time.sleep(0.5)
        element = self.driver.find_element(By.CSS_SELECTOR, ".Toastify-module__N66qt > div > div")
        while element.text != "Your CSV file was successfully exported.":
            time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, ".Toastify__close-button > svg").click()
        self.driver.find_element(By.CSS_SELECTOR, ".PageLayout-module__dHBFX > div > .Button-module__nc6_8 > .Typography-module__lVnit").click()
        

#test = TestSearch()
#test.setup_method()
#try:
#  test.test_search()
#except Exception as e:
#  print(e)
#finally:
#  test.teardown_method()

# Path where your CSV files are located
path = "/home/user/Downloads"  # Replace with your directory path

# Use glob to find all files starting with 'export' and ending with '.csv'
csv_files = glob.glob(f"{path}/scopus*.csv")

# Read and concatenate all files
dataframes = [pd.read_csv(file) for file in csv_files]
concatenated_df = pd.concat(dataframes, ignore_index=True)

# Save the concatenated DataFrame to a new CSV file (optional)
concatenated_df.to_csv("scopus_export.csv", index=False)

print("Files concatenated successfully!")