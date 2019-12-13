import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AutomatedChromeBrowser (unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')

    def test_checkForMake(self):
        self.driver.get("https://www.copart.com")
        self.driver.find_element(By.XPATH, "//input[@id='input-search']").send_keys("porsche")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

        self.driver.implicitly_wait(5)

        self.driver.find_element(By.XPATH, "//select[@name='serverSideDataTable_length']").click()
        self.driver.implicitly_wait(1)
        self.driver.find_element(By.XPATH, "//option[@value='100']").click()

        all_models_in_list = self.driver.find_elements(By.XPATH,
                                                       "//table[@id='serverSideDataTable']//span[@data-uname='lotsearchLotmodel']")

        model_text_list = []
        for model in all_models_in_list:
            model = model.text
            model_text_list.append(model)

        unique_model_set = set(model_text_list)
        unique_model_dict = {str(list(unique_model_set)[0]): 0}
        print(unique_model_dict)

        for unique_model in unique_model_set:
            unique_model_dict.update({unique_model: 0})

        for unique_model in unique_model_set:
            for model in model_text_list:
                if model == unique_model:
                    unique_model_dict[unique_model] += 1

        print(unique_model_dict)


    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
