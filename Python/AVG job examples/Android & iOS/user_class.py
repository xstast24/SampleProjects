import os
import json
import random
import binascii
from enum import Enum
from lib_python import logger
from zen2.data.TestData import is_android, is_ios
from zen2.data.UsersData import UsersData, generate_random_user


class AndroidDeviceType(Enum):
    galaxys3 = 1
    galaxys7 = 2
    htc10 = 3
    nexus6p = 4

# ===========================================================================================
# ===========================================================================================


class IosDeviceType(Enum):
    iphone4s = 1
    iphone5s = 2
    iphone6 = 3
    iphone6s = 4
    iphone6plus = 5
    iphone6splus = 6
    iphonese = 7

# ===========================================================================================
# ===========================================================================================


class UserRole(Enum):
    admin = 1
    user = 2

# ===========================================================================================
# ===========================================================================================


class PasswordStrength(Enum):
    empty = 0
    weak = 1
    ok = 2
    strong = 3


class User:
    """
    User class is used to store all data about our test user during testing. In instance of this are all personal or cloud data regarding user
    which are needed during test. Class also solves any dependencies these data might have.
    """
    def __init__(self, user_name=None, devices=None, current_device=None, password=PasswordStrength.ok, zones=None):
        """
        Either use provided data to create a functional User class or generate random user with random devices if no data available.

        :param user_name: - string name of user eq. to name of user's json file, in case parameter is left empty user will be randomly generated
        :param devices: - list of devices owned by user in case parameter is left empty device is picked randomly based on DTT_TYPE
                        - must be of enum type AndroidDeviceType/IosDeviceType or list of items of enum type AndroidDeviceType/IosDeviceType
        :param current_device: - current device, in case parameter is left empty current device is picked randomly from list of devices (must be AndroidDeviceType or IosDeviceType)
        :type password PasswordStrength
        :param password: - password (must be PasswordStrength type)
        :param zones: - array of user's zones (one must be primary) [{"role": "admin" / "user", "type": "primary" / "secondary", "zoneId": "string as zone identifier"}]
        """

        # If no user name is defined, pick a random one
        if user_name is None:
            generate_random_user(True)
            user_name = "random"

        # Getting user data from json file
        user_data = UsersData.data_for_user(user_name)

        # Personal properties of user
        self._name = user_data["name"]
        self._surname = user_data["surname"]
        self._account_name = user_data["accountName"]
        self._devices_list = {}
        self._current_device = None
        self._password = None

        # Cloud properties of user
        self._account_id = binascii.hexlify(os.urandom(16))
        logger.info(u"User: {0} {1} - Temporary Account ID generated and set".format(self._name, self._surname))
        self._relations = []
        self._zones = user_data['zones'] if zones is None else zones
        self._zaapas_authorization_token = None
        self._zaapas_untrusted_token = None
        self._ua_token = None

        # If no devices are defined, pick a random one
        if devices is None:
            if is_android():
                devices = [random.choice(list(AndroidDeviceType))]
            elif is_ios():
                devices = [random.choice(list(IosDeviceType))]
            else:
                raise EnvironmentError("Specified OS is not supported/implemented")

        # Setting user password based on input parameter password
        self.set_password(password)
        self.add_devices(devices)

        # If no current device is set, pick a random one from self._devices_list
        if current_device is None:
            logger.info(u"User: {0} {1} - No current device was set".format(self._name, self._surname))
        else:
            self.set_current_device(self._get_devices_info_from_files(self._process_input_device_type(current_device)).keys()[0])

        # User should have exactly one primary zone
        primary_zones_count = 0
        for zone in self._zones:
            if zone['type'] == "primary":
                primary_zones_count += 1
        if primary_zones_count != 1:
            raise TypeError(u"Exactly one zone must be primary! Given zones has {} primary zones".format(primary_zones_count))

    # ===========================================================================================
    # Get all information there is about User with one get
    # ===========================================================================================

    def get_properties(self):
        return {
            "name": self._name,
            "surname": self._surname,
            "relations": self._relations,
            "zones": self._zones,
            "accountName": self._account_name,
            "password": self._password,
            "devices": [self.get_device_info(item) for item in self._devices_list],
            "current_device": self.get_device_info(self._current_device) if self._current_device is not None else "None",
            "accountId": self._account_id,
            "ua_token": self._ua_token,
            "zaapas_authorization_token": self._zaapas_authorization_token,
            "zaapas_untrusted_token": self._zaapas_untrusted_token
        }

    def get_serialized_data(self):
        return json.dumps(self.get_properties())

    # ===========================================================================================
    # Methods regarding personal user properties
    # ===========================================================================================
    def get_name(self):
        return self._name

    def get_surname(self):
        return self._surname

    def get_account_name(self):
        return self._account_name

    def get_password(self):
        return self._password

    def get_devices(self):
        return self._devices_list.keys()

    def get_device_info(self, device):
        if device in self._devices_list:
            return self._devices_list[device]
        else:
            raise KeyError(u"User: {0} {1} - Return info for device: {2} failed. Device is not in list of devices".format(self._name, self._surname, device))

    def get_current_device(self):
        return self._current_device

    def set_name(self, name):
        """
        Sets 'name' of user for current instance of User class
        :param name: - string value of user's 'name'
        """
        self._name = name
        logger.info(u"User: {0} {1} - Name set to: {2}".format(self._name, self._surname, name))

    def set_surname(self, surname):
        """
        Sets 'surname' of user for current instance of User class
        :param surname: - string value of user's 'surname'
        """
        self._surname = surname
        logger.info(u"User: {0} {1} - Surname set to: {2}".format(self._name, self._surname, surname))

    def set_account_name(self, account_name):
        """
        Sets 'account_name' of user for current instance of User class
        :param account_name: - string value of user's 'account_name'
        """
        self._account_name = account_name
        logger.info(u"User: {0} {1} - account_name set to: {2}".format(self._name, self._surname, account_name))

    def set_password(self, password):
        """
        Sets 'password' of user for current instance of User class
        :type password PasswordStrength
        :param password: - password strength (must be PasswordStrength type)
        """
        self._password = self.get_password_strength(password)
        logger.info(u"User: {0} {1} - Password strength set to: {2} ({3})".format(self._name, self._surname, password.name, self._password))

    def add_devices(self, devices):
        """
        Add 'devices' to the 'devices_list' currently held in this instance of class User
        :param devices: - desired device or list of devices to be added (enum type of AndroidDeviceType or IosDeviceType required)
        """
        new_devices = self._get_devices_info_from_files(self._process_input_device_type(devices))
        self._devices_list.update(new_devices)
        for device in new_devices:
            logger.info(u"User: {0} {1} - Adding device: {2}".format(self._name, self._surname, device))

        # Update all devices with current account_id
        self._set_account_id_in_device_info(self._account_id)

    def remove_devices(self, devices):
        """
        Remove 'devices' from 'device_list' currently held in this instance of class User
        :param devices: - desired device or list of devices to be removed from 'devices_list'
        """
        if type(devices) is not list:
            devices = [devices]

        for device in devices:
            if not self._devices_list[device]["currentDevice"]:
                del self._devices_list[device]
                logger.info(u"User: {0} {1} - Removing device: {2}".format(self._name, self._surname, device))
            else:
                raise AttributeError((u"User: {0} {1} - Can't remove {2} It is set as current device".format(self._name, self._surname, device)))

    def set_devices(self, devices):
        """
        Sets 'device' to the 'devices_list' currently held in this instance of class User (first device in dict set as new current device)
        :param devices: - desired device or list of devices to be set to 'devices_list' (enum type of AndroidDeviceType or IosDeviceType required)
        """
        self._devices_list = self._get_devices_info_from_files(self._process_input_device_type(devices))
        logger.info(u"User: {0} {1} - List of devices discarded".format(self._name, self._surname))

        for device in self._devices_list:
            logger.info(u"User: {0} {1} - Adding device: {2}".format(self._name, self._surname, device))

        # Update all devices with current account_id
        self._set_account_id_in_device_info(self._account_id)

        logger.info(u"User: {0} {1} - New list of devices is set")

    def set_device_name(self, device, name):
        """
        Sets new name into device information
        :param device: - specified device which information shall be updated (enum type of AndroidDeviceType or IosDeviceType required)
        :param name: - new name of device (must be string type)
        """
        if type(device) is AndroidDeviceType or type(device) is IosDeviceType:
            if device in self._devices_list:
                self._devices_list[device]["name"] = name
                logger.info(u"User: {0} {1} - New device name: {2} set to: {3}".format(self._name, self._surname, device.name, name))
            else:
                raise KeyError(u"User: {0} {1} - Setting Current device failed. {2} is not amongst devices in devices list".format(self._name, self._surname, device))
        else:
            raise TypeError(u"User: {0} {1} - Setting device name failed. Parameter 'device' accepts only single AndroidDeviceType or IosDeviceType item".format(self._name, self._surname))

    def set_current_device(self, current_device):
        """
        Sets 'device' as 'current_device' in this instance of class User
        :param current_device: - desired device to be set as 'current_device' (enum type of AndroidDeviceType or IosDeviceType required)
        """
        if type(current_device) is AndroidDeviceType or type(current_device) is IosDeviceType:
            if current_device in self._devices_list:
                self._current_device = current_device
                for device in self._devices_list:
                    if device == current_device:
                        self._devices_list[device]["currentDevice"] = True
                    else:
                        self._devices_list[device]["currentDevice"] = False
                logger.info(u"User: {0} {1} - Current Device: {2}".format(self._name, self._surname, self._current_device))
            else:
                raise KeyError(u"User: {0} {1} - Setting Current device failed. {2} is not amongst devices in devices list".format(self._name, self._surname, current_device))
        else:
            raise TypeError(u"User: {0} {1} - Setting Current device failed. Parameter accepts only single AndroidDeviceType or IosDeviceType item".format(self._name, self._surname))

    # ===========================================================================================
    # Methods regarding user's cloud properties
    # ===========================================================================================
    def get_account_id(self):
        return self._account_id

    def get_zaapas_authorization_token(self):
        return self._zaapas_authorization_token

    def get_zaapas_untrusted_token(self):
        return self._zaapas_untrusted_token

    def get_ua_token(self):
        return self._ua_token

    def get_relations(self):
        return self._relations

    def get_zones(self):
        return self._zones

    def get_primary_zone(self):
        """
        :return: dictionary with user's primary zone information {"role": "admin" / "user", "type": "primary" / "secondary", "zoneId": "{zone identifier}"}
        """
        for zone in self._zones:
            if zone['type'] == 'primary':
                return zone

    def get_zone(self, zone_id):
        """
        :return: dictionary with user's zone information {"role": "admin" / "user", "type": "primary" / "secondary", "zoneId": "{zone identifier}"}
        """
        for zone in self._zones:
            if zone['zoneId'] == zone_id:
                return zone

    def set_account_id(self, account_id):
        """
        Sets 'account id' for current instance of User class
        :param account_id: - string value of 'account id' obtained from Cloud
        """
        self._account_id = account_id
        logger.info(u"User: {0} {1} - Account ID set to:\n{2}\n".format(self._name, self._surname, account_id))
        self._set_account_id_in_device_info(account_id)
        logger.info(u"User: {0} {1} - All devices owner Account ID updated".format(self._name, self._surname))

    def set_relations(self, relations):
        """
        Sets 'relations' of user for current instance of User class
        :param relations: - array of user's 'relations' [{ "type": "managedby" /  "masterof", "accountId": "{user account identifier}"}]
        """
        self._relations = relations
        logger.info(u"User: {0} {1} - relations set to: {2}".format(self._name, self._surname, relations))

    def set_zones(self, zones):
        """
        Sets 'zones' of user for current instance of User class
        :param zones: - array of user's 'zones' [{"role": "admin" / "user", "type": "primary" / "secondary", "zoneId": "{zone identifier}"}]
        """
        self._zones = zones
        logger.info(u"User: {0} {1} - zones set to: {2}".format(self._name, self._surname, zones))

    def set_zone(self, zone_id, zone_type, user_role):
        """
        Sets/adds zone data to user zone
        """
        for zone in self._zones:
            if zone['zoneId'] == zone_id:
                zone['type'] = zone_type
                zone['role'] = user_role
                logger.info(u"User: {0} {1} - updated zone (type:{2} role:{3}, zoneId:{4})".format(self._name, self._surname, zone_type, user_role, zone_id))
                return

        self._zones.append({'type': 'primary', 'role': user_role, 'zoneId': zone_id})
        logger.info(u"User: {0} {1} - added zone (type:{2} role:{3}, zoneId:{4})".format(self._name, self._surname, type, user_role, zone_id))

    def set_primary_zone(self, role, zone_id):
        """
        Sets user's primary zone role and zoneId. Update existing primary zone or create new one.
        :param role: UserRole - value of user's 'role'
        :param zone_id: string - value of 'zone id' obtained from Cloud
        """
        if type(role) is not UserRole:
            raise TypeError(u"User: {0} {1} - Parameter 'role' can be only type enum UserRole".format(self._name, self._surname))

        for zone in self._zones:
            if zone['type'] == 'primary':
                zone['role'] = role.name
                zone['zoneId'] = zone_id
                logger.info(u"User: {0} {1} - updated primary zone (role:{2}, zoneId:{3})".format(self._name, self._surname, role.name, zone_id))
                return

        self._zones.append({'type': 'primary', 'role': role, 'zoneId': zone_id})
        logger.info(u"User: {0} {1} - set primary zone (role:{2}, zoneId:{3})".format(self._name, self._surname, role.name, zone_id))

    def set_primary_zone_role(self, role):
        """
        Sets user's primary zone role
        :param role: UserRole - value of user's 'role'
        """
        if type(role) is not UserRole:
            raise TypeError(u"User: {0} {1} - Parameter 'role' can be only type enum UserRole".format(self._name, self._surname))

        for zone in self._zones:
            if zone['type'] == 'primary':
                zone['role'] = role.name
                logger.info(u"User: {0} {1} - Role in primary zone set to: {2}".format(self._name, self._surname, role.name))
                return

        raise TypeError(u"Primary zone was not found!")

    def set_role_for_zone(self, zone_id, role):
        """
        Sets 'role' of user in given zone for current instance of User class
        :param zone_id: string - zone identifier
        :param role: UserRole - value of user's 'role'
        :return:
        """
        if type(role) is UserRole:
            raise TypeError(u"User: {0} {1} - Parameter 'role' can be only type enum UserRole".format(self._name, self._surname))

        for zone in self._zones:
            if zone['zoneId'] == zone_id:
                zone['role'] = role.name
                logger.info(u"User: {0} {1} - Role in zone: {2} set to: {3}".format(self._name, self._surname, zone_id, role.name))

    def set_zaapas_authorization_token(self, zaapas_authorization_token):
        """
        Sets 'Zaapas authorization token' for current instance of User class
        :param zaapas_authorization_token: - string value of 'Zaapas authorization token' obtained from Cloud
        """
        self._zaapas_authorization_token = zaapas_authorization_token
        logger.info(u"User: {0} {1} - Zaapas Authorization Token set to:\n{2}\n".format(self._name, self._surname, zaapas_authorization_token))

    def set_zaapas_untrusted_token(self, zaapas_untrusted_token):
        """
        Sets 'Zaapas untrusted token' for current instance of User class
        :param zaapas_untrusted_token: - string value of 'Zaapas untrusted token' obtained from Cloud
        """
        self._zaapas_untrusted_token = zaapas_untrusted_token
        logger.info(u"User: {0} {1} - Zaapas Untrusted Token set to:\n{2}\n".format(self._name, self._surname, zaapas_untrusted_token))

    def set_ua_token(self, ua_token):
        """
        Sets 'UA token' for current instance of User class
        :param ua_token: - string value of 'UA token' obtained from Cloud
        """
        self._ua_token = ua_token
        logger.info(u"User: {0} {1} - UA Token set to:\n{2}\n".format(self._name, self._surname, ua_token))

    def set_device_id(self, device, device_id):
        """
        Sets new Device ID (obtained from Cloud) to device info
        :param device: - device which information shall be updated(enum type of AndroidDeviceType or IosDeviceType required)
        :param device_id: - new device id
        """
        if type(device) is AndroidDeviceType or type(device) is IosDeviceType:
            if device in self._devices_list:
                self._devices_list[device]["deviceId"] = device_id
                logger.info(u"User: {0} {1} - New device ID set for:\n{2}\n".format(self._name, self._surname, device))
            else:
                raise KeyError(u"User: {0} {1} - Setting Current device failed. {2} is not amongst devices in devices list".format(self._name, self._surname, device))
        else:
            raise TypeError(u"User: {0} {1} - Setting Current device failed. Parameter accepts only single AndroidDeviceType or IosDeviceType item".format(self._name, self._surname))

    def _set_account_id_in_device_info(self, account_id):
        """
        Sets account id into detailed information of each device to keep them updated
        :param account_id: - desired account_id to be set in info (must be of type string)
        """
        for device in self._devices_list:
            self._devices_list[device]["owner"]["accountId"] = account_id

    @staticmethod
    def get_password_strength(password):
        """
        Return password in string based on strength determined by PasswordStrength enum class
        :type password PasswordStrength
        :param password: - password type (must be PasswordStrength type)
        :return - password in string type
        """
        if type(password) is PasswordStrength:
            return {PasswordStrength.empty: "", PasswordStrength.weak: "aa", PasswordStrength.ok: "aaaBBB12", PasswordStrength.strong: "aaaBBB1234"}[password]
        else:
            raise TypeError("Parameter 'password' can be only type enum PasswordStrength")

    @staticmethod
    def _process_input_device_type(devices):
        """
        Check that input parameter is either single device type item or list of device type items
        :param devices: - device or list of devices (AndroidDeviceType or IosDeviceType required)
        :return: - returns list of device names in string
        """
        # Convert to list if only one device is provided
        if type(devices) is AndroidDeviceType or type(devices) is IosDeviceType:
            devices = [devices]

        # If parameter type is not list at this point, raise TypeError
        if type(devices) is list:
            list_of_devices = []
            for device in devices:
                # Check for parameter type of every item in list to ensure it is AndroidDeviceType or IosDeviceType, otherwise raise TypeError
                if type(device) is AndroidDeviceType or type(device) is IosDeviceType:
                    list_of_devices.append(device)
                else:
                    raise TypeError("'{0}' item type is not supported type in list 'devices'. Please use enum DeviceType".format(type(device)))
            return list_of_devices
        else:
            raise TypeError("'{0}' item type is not supported type in parameter 'devices'. Please use enum AndroidDeviceType or IosDeviceType".format(type(devices)))

    @staticmethod
    def _get_devices_info_from_files(devices):
        """
        Returns information for all devices
        :param devices: - device or list of devices (AndroidDeviceType or IosDeviceType required)
        :return: - returns detailed information about every device from input
        """
        dict_of_devices = {}
        for device in devices:
            # Get all device data from json file placed in lib on path 'zen2/data/devices/'
            with open('zen2/data/devices/' + device.name + '-1.json') as json_data:
                device_data = json.load(json_data)
                json_data.close()

            # Save acquired data into dictionary and return it
            dict_of_devices[device] = device_data

        return dict_of_devices
