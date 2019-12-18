import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

class AutomatedChromeBrowser (unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver_wait = WebDriverWait(self.driver, 10)
        self.all_models_in_list = []
        self.damage_type_list = []
        self.unique_model_set = []
        self.unique_model_dict = {}
        self.damage_type_dict = {'REAR END': 0, 'FRONT END': 0, 'MINOR DENT/SCRATCHES': 0, 'UNDERCARRIAGE': 0, 'MISC': 0}

    def wait_for_spinner(self):
        # created since there a couple functions that need to wait for loading spinner to disappear before continuing
        self.driver_wait.until(
            expected_conditions.invisibility_of_element((By.XPATH, '//img[@src="/images/icons/loader.gif"]')))

    def perform_make_search(self):
        self.driver.get("https://www.copart.com")

        search_field = self.driver.find_element(By.XPATH, "//input[@id='input-search']")
        search_field.send_keys("porsche")

        submit_btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_btn.click()

    def change_list_size(self):
        self.driver_wait.until(expected_conditions.visibility_of_element_located(
            (By.XPATH, '//table[@id="serverSideDataTable"]//span[@data-uname="lotsearchLotmodel"]')))

        search_result_table_length = self.driver.find_element(By.XPATH, "//select[@name='serverSideDataTable_length']")
        search_result_table_length.click()

        self.wait_for_spinner()

        search_result_table_length_100_option = self.driver.find_element(By.XPATH, "//option[@value='100']")
        search_result_table_length_100_option.click()

        search_result_table_length.click()

    def get_model_list(self):
        self.all_models_in_list = self.driver.find_elements(By.XPATH,
                                                            "//table[@id='serverSideDataTable']//span[@data-uname='lotsearchLotmodel']")

    def get_damage_list(self):
        self.damage_type_list = self.driver.find_elements(By.XPATH,
                                                          '//*[@id="serverSideDataTable"]//span[@data-uname="lotsearchLotdamagedescription"]')

    def  create_model_dict_from_list(self):
        model_text_list = []
        for model in self.all_models_in_list:
            model = model.text
            model_text_list.append(model)

        self.unique_model_set = set(model_text_list)
        self.unique_model_dict = {str(list(self.unique_model_set)[0]): 0}

        for unique_model in self.unique_model_set:
            self.unique_model_dict.update({unique_model: 0})

        for unique_model in self.unique_model_set:
            for model in model_text_list:
                if model == unique_model:
                    self.unique_model_dict[unique_model] += 1

    def sort_damage_types(self):
        for damage_type in self.damage_type_list:
            damage = damage_type.get_attribute('textContent')
            if damage == 'REAR END':
                self.damage_type_dict['REAR END'] += 1
            elif damage == 'FRONT END':
                self.damage_type_dict['FRONT END'] += 1
            elif damage == 'MINOR DENT/SCRATCHES':
                self.damage_type_dict['MINOR DENT/SCRATCHES'] += 1
            elif damage == 'UNDERCARRIAGE':
                self.damage_type_dict['UNDERCARRIAGE'] += 1
            else:
                self.damage_type_dict['MISC'] += 1

    def print_model_and_damage_count(self):
        for key in self.unique_model_dict.keys():
            print("{}: {}".format(key, self.unique_model_dict[key]))

        print("")

        for key in self.damage_type_dict.keys():
            print("{}: {}".format(key, self.damage_type_dict[key]))

    def test_searchForModel(self):
        self.perform_make_search()
        self.change_list_size()
        self.wait_for_spinner()
        self.get_model_list()
        self.get_damage_list()
        self.create_model_dict_from_list()
        self.sort_damage_types()
        self.print_model_and_damage_count()

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
