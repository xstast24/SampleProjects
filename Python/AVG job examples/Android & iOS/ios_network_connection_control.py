from appium.webdriver.connectiontype import ConnectionType
from lib_python import logger
from lib_python.baseObjects.AppiumObject import AppiumObject, SelectorType
from zen2.data.iOSData import auto_accept_alerts
from zen2.InputParameterConvertor import InputParameterConvertor


class ControlCenter:
    """
    This class serves to handle iOS Control Center (= the menu that you can bring by swiping from the bottom of the screen).
    iOS 8.x simulator NOT supported! There is no swiping automation in 8.x simulators - apple not supporting.
    """
    def __init__(self, driver):
        self._driver = driver

        self._button_airplane_mode = AppiumObject(self._driver, "Airplane Mode", SelectorType.text)
        self._button_wifi = AppiumObject(self._driver, "Wi-Fi", SelectorType.text)
        self._auto_accept_alerts = InputParameterConvertor.convert_to_bool(auto_accept_alerts)  # if autoaccepting alerts, there is no need to dismiss "no SIM card" alert when turning airplane off
        if not self._auto_accept_alerts:
            self._missing_sim_card_alert = AppiumObject(self._driver, 'No SIM Card Installed', SelectorType.text)

        screen_size = self._driver.get_window_size()
        self._horizontal_center = screen_size['width']/2
        self._screen_bottom = screen_size['height']-1
        self._screen_top = 1

    def _open_control_center(self):
        """
        Opens up iOS Control Center by swiping from the bottom to the top of the screen.
        """
        self._driver.swipe(start_x=self._horizontal_center, start_y=self._screen_bottom, end_x=self._horizontal_center, end_y=self._screen_top, duration=500)
        self._button_airplane_mode.wait_for(5)
        logger.info("iOS Control Center has been opened.")

    def _close_control_center(self):
        """
        Closes iOS Control Center by tapping on iOS status bar (the bar on the top of the screen).
        """
        self._driver.execute_script("mobile: tap", {"tapCount": 1, "touchCount": 1, "duration": 0.2, "x": self._horizontal_center, "y": self._screen_top})
        logger.info("iOS Control Center has been closed.")

    def _airplane_mode_turn_on(self):
        if InputParameterConvertor.convert_to_int(self._button_airplane_mode.get_attribute('value')) == 1:
            logger.warning("Trying to turn Airplane Mode ON, but Airplane Mode is already ON!")
        else:
            self._button_airplane_mode.click()

        logger.info("Airplane Mode state: ON")

    def _airplane_mode_turn_off(self):
        if InputParameterConvertor.convert_to_int(self._button_airplane_mode.get_attribute('value')) == 0:
            logger.warning("Trying to turn Airplane Mode OFF, but Airplane Mode is already OFF!")
        else:
            self._button_airplane_mode.click()
            if not self._auto_accept_alerts:
                try:  # no SIM card > alert displayed > dismiss
                    self._missing_sim_card_alert.wait_for(10)
                    self._driver.switch_to.alert.accept()
                    logger.info("\"No SIM Card Installed\" alert dismissed.")
                except AssertionError:  # SIM card present > no alert displayed > no action taken
                    logger.info("\"No SIM Card Installed\" alert not detected, the test is running on a device with SIM card installed, or there was an error dismissing alert.")

        logger.info("Airplane Mode state: OFF")

    def airplane_mode_turn_on(self):
        self._open_control_center()
        self._airplane_mode_turn_on()
        self._close_control_center()

    def airplane_mode_turn_off(self):
        self._open_control_center()
        self._airplane_mode_turn_off()
        self._close_control_center()

    def _wifi_turn_on(self):
        if InputParameterConvertor.convert_to_int(self._button_wifi.get_attribute('value')) == 1:
            logger.warning("Trying to turn Wi-Fi ON, but Wi-Fi is already ON!")
        else:
            self._button_wifi.click()

        logger.info("Wi-Fi state: ON")

    def _wifi_turn_off(self):
        if InputParameterConvertor.convert_to_int(self._button_wifi.get_attribute('value')) == 0:
            logger.warning("Trying to turn Wi-Fi OFF, but Wi-Fi is already OFF!")
        else:
            self._button_wifi.click()

        logger.info("Wi-Fi state: OFF")

    def wifi_turn_on(self):
        self._open_control_center()
        self._wifi_turn_on()
        self._close_control_center()

    def wifi_turn_off(self):
        self._open_control_center()
        self._wifi_turn_off()
        self._close_control_center()

    def set_network_connection(self, connection_type):
        """
        Set network connection to desired type:
        :param connection_type: int or enum from appium/webdriver/connectiontype > ConnectionType
            Value              | Data | Wifi
            0 (None)           | 0    | 0
            1 (Airplane Mode)  | 0    | 0
            2 (Wifi only)      | 0    | 1
            4 (Data only)      | 1    | 0
            6 (All network on) | 1    | 1
        """
        if connection_type == ConnectionType.NO_CONNECTION or connection_type == ConnectionType.AIRPLANE_MODE:
            self._open_control_center()
            self._airplane_mode_turn_on()
            self._wifi_turn_off()
            self._close_control_center()
        elif connection_type == ConnectionType.WIFI_ONLY:
            self._open_control_center()
            self._airplane_mode_turn_on()
            self._wifi_turn_on()
            self._close_control_center()
        elif connection_type == ConnectionType.DATA_ONLY:
            self._open_control_center()
            self._airplane_mode_turn_off()
            self._wifi_turn_off()
            self._close_control_center()
        elif connection_type == ConnectionType.ALL_NETWORK_ON:
            self._open_control_center()
            self._airplane_mode_turn_off()
            self._wifi_turn_on()
            self._close_control_center()
        else:
            raise Exception("Can not set network connection - unknown connection type!")
