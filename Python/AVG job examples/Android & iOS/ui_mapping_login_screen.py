from lib_python import logger, variables
from lib_python.baseObjects.AppiumObject import AppiumObject, SelectorType
from zen2.data.TestData import is_android, is_ios


class LoginScreen:
    """
    LoginScreen class serving purpose of UI Mapping for control over specific screen in ZPR apk.
    """
    # default value for password field
    PASSWORD_PLACEHOLDER = u"Enter password"

    def __init__(self, driver):
        self.driver = driver
        if is_android():
            self.edit_text_email = AppiumObject(driver, "edit_text_email", SelectorType.id)
            self.edit_text_password = AppiumObject(driver, "edit_text_password", SelectorType.id)
            self.error_email_pwd_not_match = AppiumObject(driver, "text_view_difference_email_password", SelectorType.id)
            self.button_create_account = AppiumObject(driver, "button_create_account", SelectorType.id)
            self.button_forgot_password = AppiumObject(driver, "button_forgot_password", SelectorType.id)
            self.button_log_in = AppiumObject(driver, "button_log_in", SelectorType.id)
            self.button_show_password = AppiumObject(driver, "button_show_password", SelectorType.id)
            self.button_clear_email_field = AppiumObject(driver, "button_clear_email", SelectorType.id)
        elif is_ios():
            self.edit_text_email = AppiumObject(driver, "edit_text_email", SelectorType.id)
            # password field when password is hidden by asterix
            self.edit_text_password = AppiumObject(driver, "edit_text_password", SelectorType.id)
            self.error_email_pwd_not_match = AppiumObject(driver, "Email and password don't match. Please try again.", SelectorType.text)
            self.button_create_account = AppiumObject(driver, "button_create_account", SelectorType.id)
            self.button_forgot_password = AppiumObject(driver, "button_forgot_password", SelectorType.id)
            self.button_log_in = AppiumObject(driver, "button_log_in", SelectorType.id)
            self.button_show_password = AppiumObject(driver, "button_show_password", SelectorType.id)
            self.button_clear_email_field = AppiumObject(driver, "UIAButton", SelectorType.class_name, parent_object=self.edit_text_email)
            self.email_image = AppiumObject(driver, "image_email", SelectorType.id)
        else:
            raise Exception("Specified OS is not supported/implemented in this step")

    def wait_for_element(self, selector, timeout=10, period=1, selector_type=SelectorType.text):
        waited_element = AppiumObject(self.driver, selector, selector_type)
        waited_element.wait_for(timeout, period)

    def go_to_register(self):
        self.button_create_account.wait_for(30)
        self.button_create_account.click()

    def send_form(self):
        self.button_log_in.click()

    def fill_form(self, data):
        """
        Accepts a data and fills them in the UI elements
        :param data: Data in the format from zen2.data.LoginData.py
        :return: nothing
        """
        self.edit_text_email.set_text(data["accountName"] if data["accountName"] is not None else "")
        self.edit_text_password.set_text(data["password"] if data["password"] is not None else "")

    def clear_email_field(self):
        """
        Tries to click on a clear button inside email field.
        """
        self.edit_text_email.click()
        self.button_clear_email_field.click()

    def clear_input_fields(self):
        """
        Clears login screen input fields (email and password).
        """
        self.edit_text_email.wait_for(2)
        self.edit_text_email.clear()
        self.clear_password_field()

    def clear_password_field(self):
        """
        Clears Password input field using Appium method Clear()
        """
        if is_android():
            self.__custom_android_clear_password()
        elif is_ios():
            self.__custom_ios_clear_password()
        else:
            raise Exception("Specified OS is not supported/implemented in this step")

    def __custom_android_clear_password(self):
        """
        Clear password input field and make sure it is cleared, this method also checks that deletion was successful
        """
        key_del = 67  # Key code for Backspace key

        self.edit_text_password.clear()

        try:
            AppiumObject(self.driver, "//*[@class='android.widget.EditText'][@password='true']", SelectorType.xpath).get_element()
            self.edit_text_password.click()
            self.button_show_password.click()

        except LookupError:
            logger.info("Password is displayed.")

        while self.edit_text_password.get_text() != self.PASSWORD_PLACEHOLDER:
            variables.driver.press_keycode(key_del)

        logger.info("Password should be gone as a spring snow :)")
        self.button_show_password.click()

    def __custom_ios_clear_password(self):

        if self.edit_text_password.get_text() == self.PASSWORD_PLACEHOLDER:
            logger.info("Password text field is empty!")
            return

        self.edit_text_password.click()

        i = len(self.edit_text_password.get_text())
        while i != 0:
            self.edit_text_password.set_text("\b")
            i -= 1
