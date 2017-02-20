# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class Login(unittest.TestCase):
    def setUp(self):
        try:
            if not self.first_case:
                self.first_case = False
        except AttributeError:
            self.first_case = False
            self.last_case = False

            # self.driver = webdriver.Firefox()
            self.driver = webdriver.Remote(
                command_executor='http://mys01.fit.vutbr.cz:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.FIREFOX)
            self.driver.implicitly_wait(1)
            self.base_url = "https://www.artin.cz"

        self.verificationErrors = []
        self.accept_next_alert = True

    def test_add_client(self):
        driver = self.driver
        driver.get(self.base_url + "/tmtest/public/login")

        for i in range(15):
            if i == 14:
                self.fail("Login page did not load.")
            try:
                driver.find_element_by_name("j_username").clear()
                break
            except:
                time.sleep(1)

        driver.find_element_by_name("j_username").send_keys("jmeno2.prijmeni2")
        driver.find_element_by_name("j_password").clear()
        driver.find_element_by_name("j_password").send_keys("artinthebest")
        driver.find_element_by_css_selector("input.flatbutton").click()

        for i in range(15):
            if i == 14:
                self.fail("Time Mission system did not load.")
            try:
                driver.find_element_by_link_text("Konfigurace").click()
                break
            except:
                time.sleep(1)

        for i in range(15):
            if i == 14:
                self.fail("Can not get to client configuration page.")
            try:
                driver.find_element_by_xpath("(//a[contains(text(),'Klienti')])[2]").click()
                break
            except:
                time.sleep(1)

        time.sleep(2)
        #driver.save_screenshot("logged_in.png")

        # ADD A CLIENT
        for i in range(15):
            if i ==14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"Nový klient").click()
                break
            except:
                time.sleep(1)

        for i in range(15):
            if i == 14:
                self.fail("Create new client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("//input[@type='text']").clear()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@type='text']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@type='text']").send_keys(u"0client_odberatel")
        driver.find_element_by_name("ico").click()
        driver.find_element_by_name("ico").clear()
        driver.find_element_by_name("ico").send_keys("94445869")
        driver.find_element_by_name("dic").clear()
        driver.find_element_by_name("dic").send_keys("CZ94445869")
        driver.find_element_by_xpath("(//input[@type='text'])[4]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[4]").send_keys("777599695")
        driver.find_element_by_xpath("(//input[@type='text'])[5]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[5]").send_keys("client@mail.mail")
        driver.find_element_by_xpath("(//input[@type='text'])[14]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[14]").send_keys(u"Klientská 42")
        driver.find_element_by_xpath("(//input[@type='text'])[17]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[17]").send_keys("63623")
        driver.find_element_by_xpath("(//input[@type='text'])[18]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[18]").send_keys("Klient")
        driver.find_element_by_xpath("(//input[@type='text'])[19]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[19]").send_keys(u"Česká Republika")
        driver.find_element_by_xpath("(//input[@type='text'])[19]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[19]").send_keys(u"Česká republika")
        driver.find_element_by_xpath("(//input[@type='text'])[20]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[20]").send_keys("Fakturacni 42")
        driver.find_element_by_xpath("(//input[@type='text'])[23]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[23]").send_keys("63623")
        driver.find_element_by_xpath("(//input[@type='text'])[24]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[24]").send_keys("Klient")
        driver.find_element_by_xpath("(//input[@type='text'])[25]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[25]").send_keys(u"Česká republika")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()

        for i in range(15):
            if i == 14:
                self.fail("Adding a new client failed.")
            try:
                if self.is_element_present(By.LINK_TEXT, u"0client_odberatel"):
                    break
            except:
                time.sleep(1)

    def test_invalid_client(self):
        driver = self.driver
        driver.find_element_by_link_text(u"Nový klient").click()
        for i in range(15):
            if i == 14:
                self.fail("Create new client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("(//input[@type='text'])[14]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[14]").send_keys("Klientova 15")
        driver.find_element_by_xpath("(//input[@type='text'])[17]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[17]").send_keys("44444")
        driver.find_element_by_xpath("(//input[@type='text'])[18]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[18]").send_keys("Klienta")
        driver.find_element_by_xpath("(//input[@type='text'])[20]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[20]").send_keys("Fakturacni 15")
        driver.find_element_by_xpath("(//input[@type='text'])[23]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[23]").send_keys("22222")
        driver.find_element_by_xpath("(//input[@type='text'])[24]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[24]").send_keys("Faktura")
        driver.find_element_by_xpath("//input[@type='text']").click()

        for i in range(15):
            if i == 14:
                self.fail("Invalid client error message is not displayed.")
            try:
                if self.is_element_present(By.NAME, u"Toto pole je povinné"):
                    break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("(//button[@type='button'])[9]").click()

    def test_edit_client(self):
        driver = self.driver
        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"Nový klient").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_link_text("0client_odberatel").click()
        for i in range(15):
            if i == 14:
                self.fail("Create new client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("(//input[@type='text'])[26]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[26]").send_keys("contact_person_does_exist_with_long_name")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"Nový klient").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_link_text("0client_odberatel").click()
        for i in range(15):
            if i == 14:
                self.fail("Client info has not been changed correctly.")
            try:
                driver.find_element_by_name("contact_person_does_exist_with_long_name").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("(//button[@type='button'])[9]").click()

    def test_search_client(self):
        driver = self.driver
        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"Nový klient").click()
                break
            except:
                time.sleep(1)

        for i in range(15):
            if i == 14:
                self.fail("Create new client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("clientXX")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"Nový klient").click()
                break
            except:
                time.sleep(1)

        for i in range(15):
            if i == 14:
                self.fail("Create new client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("clientYY")
        driver.find_element_by_css_selector("button.btn.btn-primary").click()
        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"Nový klient")
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("clientXX")

        for i in range(15):
            if i == 14:
                self.fail("Client X is not displayed.")
            try:
                if self.is_element_present(By.LINK_TEXT, u"clientXX"):
                    break
            except:
                time.sleep(1)

        for i in range(5):
            try:
                if self.is_element_present(By.LINK_TEXT, u"clientYY"):
                    self.fail("Client Y is displayed.")
            except:
                time.sleep(1)

        driver.find_element_by_xpath("//input[@type='text']").clear()
        time.sleep(4)

    def test_delete_client(self):
        driver = self.driver
        self.last_case = True
        "Opravdu chcete smazat klienta 0client_odberatel?"
        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"0client_odberatel").click()
                break
            except:
                time.sleep(1)

        for i in range(15):
            if i == 14:
                self.fail("Edit client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_css_selector("button-with-dialog.ng-isolate-scope.ng-scope > button.btn-danger").click()
        for i in range(15):
            if i == 14:
                self.fail("Can not delete a client.")
            try:
                driver.find_element_by_name(u"Opravdu chcete smazat klienta 0client_odberatel?")
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        time.sleep(2)
        driver.find_element_by_xpath("(//button[@type='button'])[9]").click()

        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"clientXX").click()
                break
            except:
                time.sleep(1)

        for i in range(15):
            if i == 14:
                self.fail("Edit client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_css_selector("button-with-dialog.ng-isolate-scope.ng-scope > button.btn-danger").click()
        for i in range(15):
            if i == 14:
                self.fail("Can not delete a client.")
            try:
                driver.find_element_by_name(u"Opravdu chcete smazat klienta clientXX?")
                break
            except:
                time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        time.sleep(2)
        driver.find_element_by_xpath("(//button[@type='button'])[9]").click()

        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"clientYY").click()
                break
            except:
                time.sleep(1)

        for i in range(15):
            if i == 14:
                self.fail("Edit client - page did not load in time.")
            try:
                driver.find_element_by_xpath("//div/input").click()
                break
            except:
                time.sleep(1)

        driver.find_element_by_css_selector("button-with-dialog.ng-isolate-scope.ng-scope > button.btn-danger").click()
        for i in range(15):
            if i == 14:
                self.fail("Can not delete a client.")
            try:
                driver.find_element_by_name(u"Opravdu chcete smazat klienta clientYY?")
                break
            except:
                time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click()
        time.sleep(2)
        driver.find_element_by_xpath("(//button[@type='button'])[9]").click()

        # check if element is present
        for i in range(15):
            if i == 14:
                self.fail("Page did not load in time.")
            try:
                driver.find_element_by_link_text(u"Nový klient")
                break
            except:
                time.sleep(1)

        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("clientYY")
        for i in range(5):
            try:
                if self.is_element_present(By.LINK_TEXT, u"clientYY"):
                    self.fail("Client Y is displayed.")
            except:
                time.sleep(1)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False

        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        if self.last_case:
            self.driver.quit()
            self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
