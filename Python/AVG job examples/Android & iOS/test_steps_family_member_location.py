import json
import copy
import datetime
from time import sleep
import zen2.platform_simulator as sim
from lib_python import steps, execution, logger, variables
from lib_python.compare import compare_values
from zen2.InputParameterConvertor import InputParameterConvertor
from zen2.commands.Init import Init
from zen2.commands.RegisterRequestListener import RegisterRequestListener
from zen2.commands.SendRequest import SendRequest
from zen2.data.TestData import is_android, is_ios
from zen2.data.LayoutNoticeContentData import LayoutNoticeContentData
from zen2.messages.ZplNetworkStatusGetCachedDataResponse import ZplNetworkStatusGetCachedDataResponse
from zen2.messages.ZplZplAccountDetailsGetCachedDataResponse import ZplZplAccountDetailsGetCachedDataResponse
from zen2.messages.ZplZplAccountStatusGetCachedDataResponse import ZplZplAccountStatusGetCachedDataResponse
from zen2.messages.ZplZplContentOnChange import ZplZplContentOnChange
from zen2.messages.ZplZplInvitationIncomingGetCachedDataResponse import ZplZplInvitationIncomingGetCachedDataResponse
from zen2.messages.ZplZplInvitationOutgoingGetCachedDataResponse import ZplZplInvitationOutgoingGetCachedDataResponse
from zen2.messages.ZplZplUsersGetCachedDataResponse import ZplZplUsersGetCachedDataResponse
from zen2.messages.ZplZplDevicesGetCachedDataResponse import ZplZplDevicesGetCachedDataResponse
from zen2.messages.ZprSimulatorSFCResourceStatus import ZprSimulatorSFCResourceStatus
from zen2.messages.ZprSimulatorSFCResourceStatusResponse import ZprSimulatorSFCResourceStatusResponse
from zen2.module_methods.ActivityFeed.TimeConverter import TimeConverter
from zen2.module_methods.FamilyMemberLocation.FamilyMemberLocationCommonMethods import build_user_location
from zen2.module_methods.HomeScreen.LocationToAddress import LocationToAddress
from zen2.layouts.NoticeContentData import NoticeContentData


def family_member_location_init_simulator(params):
    """
    Sends initial sequence of commands to simulator
    :param params: parameters from TSD
    """
    user_name = params['user_name']
    user = variables.users[user_name]
    variables.logged_user = {user_name: user}

    variables.timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+01:00")

    # Connect platform simulator
    variables.sim = sim.PlatformSimulator()
    variables.sim.connect()

    # Create command register request listener with message zpl.NetworkStatus.GetCachedData
    network_status_response = ZplNetworkStatusGetCachedDataResponse.create_message(connected=True, result_value=0)
    register_network_status_response = RegisterRequestListener.create_command(message_id="zpl.NetworkStatus.GetCachedData", request_response_list=[[None, network_status_response]])

    # Create command register request listener with message zpl.Zpl.Account.Status.GetCachedData
    account_getstatus_response = ZplZplAccountStatusGetCachedDataResponse.create_message(0, zone_membership="in-zone", account_status="activated")
    register_account_getstatus_response = RegisterRequestListener.create_command(message_id="zpl.Zpl.Account.Status.GetCachedData", request_response_list=[[None, account_getstatus_response]])

    # Create command register request listener with message zpl.Zpl.Account.Details.GetCachedData
    request_response_list = ZplZplAccountDetailsGetCachedDataResponse.create_message(result_value=0, user=user)
    register_account_details = RegisterRequestListener.create_command(message_id="zpl.Zpl.Account.Details.GetCachedData", request_response_list=[[None, request_response_list]])

    # Create command register request listener with message zpl.Zpl.Users.GetCachedData
    users_response = ZplZplUsersGetCachedDataResponse.create_message(result_value=0, users=[user])
    register_users_refresh = RegisterRequestListener.create_command(message_id="zpl.Zpl.Users.GetCachedData", request_response_list=[[None, users_response]])

    # Create command register request listener with message zpl.Zpl.Devices.GetCachedData
    devices_response = ZplZplDevicesGetCachedDataResponse.create_message(result_value=0, user_objects=variables.users.values())
    register_devices_refresh = RegisterRequestListener.create_command(message_id="zpl.Zpl.Devices.GetCachedData", request_response_list=[[None, devices_response]])

    # Create command register register listener with message zpl.Zpl.Invitation.Outgoing.GetCachedData
    invitation_outgoing_response = ZplZplInvitationOutgoingGetCachedDataResponse.create_message(result_value=0, timestamp=variables.timestamp)
    register_invitation_outgoing = RegisterRequestListener.create_command(message_id="zpl.Zpl.Invitation.Outgoing.GetCachedData", request_response_list=[[None, invitation_outgoing_response]])

    # Create command register register listener with message zpl.Zpl.Invitation.Incoming.GetCachedData
    invitation_incoming_response = ZplZplInvitationIncomingGetCachedDataResponse.create_message(result_value=0, timestamp=variables.timestamp)
    register_invitation_incoming = RegisterRequestListener.create_command(message_id="zpl.Zpl.Invitation.Incoming.GetCachedData", request_response_list=[[None, invitation_incoming_response]])

    # Create init command which includes configuration of ui module, register request listener command
    init_command = Init.create_command(background_modules=["zpr.ContentPlacementResolver"], ui_modules=["HomeScreen"], commands_list=[register_network_status_response, register_account_getstatus_response, register_account_details, register_users_refresh, register_invitation_outgoing, register_invitation_incoming, register_devices_refresh])

    # Control ack command after sent init command
    init = variables.sim.send(init_command)
    variables.sim.check_ack(init)

    # waiting to process init
    variables.dashboard_screen.family_tab.wait_for(30)

    execution.passed()

steps.new_step("FamilyMemberLocation - Init simulator for dashboard, logged user: {user_name}", family_member_location_init_simulator)


def family_member_location_connect_appium(params):
    user_name = params['user']
    user = variables.users[user_name]
    variables.logged_user = {user_name: user}

    execution.passed()

steps.new_step("FamilyMemberLocation - Set currently logged user: {user}", family_member_location_connect_appium)


def family_member_location_set_location_variable_for_user(params):

    latitude_value = params['latitude_value']
    longitude_value = params['longitude_value']

    if abs(InputParameterConvertor.convert_to_float(latitude_value)) > 90:
        execution.error("Wrong latitude: {}".format(latitude_value))

    if abs(InputParameterConvertor.convert_to_float(longitude_value)) > 180:
        execution.error("Wrong longitude: {}".format(longitude_value))

    accuracy = InputParameterConvertor.convert_to_int(params['accuracy_value'])

    time_stamp = "2015-10-10T16:27:43+02:00"

    user = variables.users[params['user_name']]
    user_devices = user.get_devices()
    device = user.get_device_info(user_devices[0])

    try:
        variables.locations_of_users
    except AttributeError:
        variables.locations_of_users = {}

    variables.locations_of_users[user.get_account_id()] = build_user_location(device['deviceId'], latitude_value, longitude_value, accuracy, time_stamp)

    execution.passed()

steps.new_step("FamilyMemberLocation - Set coordinates {latitude_value}, {longitude_value} with accuracy {accuracy_value} for user {user_name}", family_member_location_set_location_variable_for_user)


def family_member_location_set_location_variable_from_file(params):
    # NOTE: this E2E test step may be old and may not work
    try:
        variables.locations_of_users
    except AttributeError:
        variables.locations_of_users = {}

    with open('zen2/data/notice_content_data/' + params['file'] + '.json') as locations_json_data:
        locations = json.load(locations_json_data)

    for user_data in locations["users"]:
        variables.locations_of_users[user_data["accountId"]] = build_user_location(user_data["deviceId"],
                                                                                   user_data["location"]["latitude"], user_data["location"]["longitude"],
                                                                                   user_data["location"]["accuracy"], user_data["location"]["updateTimestamp"])

    execution.passed()

steps.new_step("FamilyMemberLocation - Set user's coordinates from {file}", family_member_location_set_location_variable_from_file)


def family_member_location_register_listener_for_packages(params):
    # path to web server
    server_path = "http://ddtfstorage-sn.cz.avg.com/Zaap/regression_tests/services/"

    # list of available packages
    available_packages = ["servicePackage.zip", "servicePackageNew.zip", "pluginDetail.zip", "fakeService1.zip", "fakeService2.zip", "fakeService3.zip", "fakeService1New.zip", "fakeService2New.zip", "fakeService3New.zip"]

    # create list of packages from step parameter
    packages_list = params["packages_names_comma_separated"].split(",")
    packages_list = map(unicode.strip, packages_list)

    # check name validity of packages
    request_response = []
    for package in packages_list:
        package_checked = InputParameterConvertor.check_valid_parameter(input_data=package, valid_values_set=available_packages)
        resource_registration_request = ZprSimulatorSFCResourceStatus.create_message(package_checked)
        resource_registration_response = ZprSimulatorSFCResourceStatusResponse.create_message(True, "{0}{1}".format(server_path, package_checked))
        request_response.append([resource_registration_request, resource_registration_response])

    registration_command = RegisterRequestListener.create_command(message_id="zpr.Simulator.SFC.ResourceStatus", request_response_list=request_response)

    check_command = variables.sim.send(registration_command)
    variables.sim.check_ack(check_command)
    logger.info("Registration of package listener with message zpr.Simulator.SFC.ResourceStatus was successful.")

    execution.passed()

steps.new_step("FamilyMemberLocation - Register request listener for packages: {packages_names_comma_separated}", family_member_location_register_listener_for_packages)


def family_member_location_send_location_package(params):
    new_snapshot = InputParameterConvertor.convert_to_bool(params['new_snapshot'])

    zone_id = variables.logged_user.values()[0].get_primary_zone()['zoneId']
    plugin_type = InputParameterConvertor.check_valid_parameter(params['plugin_type'], ["Status", "Detail"])
    if plugin_type == "Status":
        content_data = LayoutNoticeContentData.data_for_layout_with_json_data("service_package", {"users": []})
        content = NoticeContentData.create_content_data(content_id="status.low", origin_plugin_id="service", id_="1", zone_id=zone_id, content=content_data)
    else:  # Detail
        content_data = LayoutNoticeContentData.data_for_layout_with_json_data("plugin_detail_package", {"users": []})
        content = NoticeContentData.create_content_data(content_id="detail.low", origin_plugin_id="service", id_="1", zone_id=zone_id, content=content_data)

    try:
        variables.contents
    except AttributeError:
        variables.contents = {}

    variables.contents[params['plugin_type']] = content

    increment = True
    try:
        variables.contentIncrementVersion
    except AttributeError:
        increment = False

    if increment is False or new_snapshot:
        variables.contentIncrementVersion = 0
        increment = False
    else:
        variables.contentIncrementVersion += 1

    content_change_message = ZplZplContentOnChange.create_message(increment=increment, version=variables.contentIncrementVersion, add=[content])

    # generate and send request
    request_command = SendRequest.create_command(message_id="zpl.Zpl.Content.OnChange", message_data=content_change_message)

    check_command = variables.sim.send(request_command)
    variables.sim.check_ack(check_command)
    logger.info("zpl.Zpl.Content.OnChange command was sent successfully.")

    execution.passed()

steps.new_step("FamilyMemberLocation - Send content with map for plugin {plugin_type} as newsnapshot: {new_snapshot}", family_member_location_send_location_package)


def family_member_location_send_location_package_for_user(params):
    # constants
    exact_location = 'Exact location'
    save_place = 'Safe place'
    offline = 'Offline'
    invisible = 'Invisible'

    device_status = InputParameterConvertor.check_valid_parameter(params['device_status'], [exact_location, save_place, offline, invisible])
    latitude_value = params['latitude_value']
    longitude_value = params['longitude_value']

    if abs(InputParameterConvertor.convert_to_float(latitude_value)) > 90:
        execution.error("Wrong latitude: {}".format(latitude_value))

    if abs(InputParameterConvertor.convert_to_float(longitude_value)) > 180:
        execution.error("Wrong longitude: {}".format(longitude_value))

    accuracy_value = InputParameterConvertor.check_valid_parameter(params['accuracy_value'], ["Address", "Street", "Post code", "Town"])
    timestamp_value = InputParameterConvertor.check_valid_parameter(params['timestamp_value'], ["Just now", "5m ago", "10m ago", "59m ago", "2h ago", "23h ago", "1d ago", "2d ago"])

    # translate accuracy param into value in meters
    accuracy = {"Address": 5, "Street": 358, "Post code": 30000, "Town": 40000}[accuracy_value]

    # translate timestamp param into formatted time for message
    time_stamp = TimeConverter.activity_feed_timestamp("0m")
    if timestamp_value != "Just now":
        delta = timestamp_value.partition(' ')[0]
        time_stamp = TimeConverter.activity_feed_timestamp(delta)

    user = variables.users[params['user_name']]
    user_devices = user.get_devices()
    device = user.get_device_info(user_devices[0])

    try:
        variables.locations_of_users
    except AttributeError:
        variables.locations_of_users = {}

    try:
        variables.locations_of_users_for_map
    except AttributeError:
        variables.locations_of_users_for_map = {}

    if device_status in (exact_location, offline, invisible):
        # save location of user
        variables.locations_of_users[user.get_account_id()] = build_user_location(device['deviceId'], latitude_value, longitude_value, accuracy, time_stamp)

        if device_status == exact_location:
            variables.locations_of_users_for_map[user.get_account_id()] = copy.copy(variables.locations_of_users[user.get_account_id()])
            logger.info("Number of users for map: {0}".format(len(variables.locations_of_users_for_map)))

        elif user.get_account_id() in variables.locations_of_users_for_map.keys():
            del variables.locations_of_users_for_map[user.get_account_id()]
            logger.info("Number of users for map after remove offline and invisible: {0}".format(len(variables.locations_of_users_for_map)))

    else:
        # TODO implement Safe place device status
        execution.error("Device status Safe place will be implemented later.")

    # generate message containing data with all known locations of users, along with all thingies around it
    users = []
    for key, location in variables.locations_of_users.iteritems():
        users.append({"accountId": key, "deviceId": location['deviceId'], "location": location['data']})

    update_contents = []
    if "Status" in variables.contents:
        variables.contents["Status"]["content"]["data"] = {"users": users}
        update_contents.append(variables.contents["Status"])
    if "Detail" in variables.contents:
        variables.contents["Detail"]["content"]["data"] = {"users": users}
        update_contents.append(variables.contents["Detail"])

    variables.contentIncrementVersion += 1
    content_change_message = ZplZplContentOnChange.create_message(increment=True, version=variables.contentIncrementVersion, update=update_contents)

    # generate and send request
    request_command = SendRequest.create_command(message_id="zpl.Zpl.Content.OnChange", message_data=content_change_message)

    check_command = variables.sim.send(request_command)
    variables.sim.check_ack(check_command)

    # Sleep for 10 seconds needed for Android, so service will be loaded for each user
    if is_android():
        sleep(10)

    logger.info("zpl.Zpl.Content.OnChange command was sent successfully.")

    execution.passed()

steps.new_step("FamilyMemberLocation - Set device status {device_status} with location - lat. {latitude_value}, lon. {longitude_value}, accuracy {accuracy_value} level and timestamp {timestamp_value} for user {user_name}", family_member_location_send_location_package_for_user)


def family_member_location_check_opened_status_for_service(params):
    user = variables.users[params['user']]
    location_text = LocationToAddress.location_to_address(variables.locations_of_users[user.get_account_id()]["data"]).encode('utf-8')
    plugin_expected_displayed = InputParameterConvertor.convert_to_bool(params['bool'])

    user_name = user.get_name()
    if user_name == variables.logged_user.values()[0].get_name():
        logger.info("{0} is the logged user, searching plugins for user name: Me".format(params['user']))
        user_name = 'Me'

    logger.info("User object for {0} found, searching location plugin: {1} for user name: {2}".format(params['user'], location_text, user_name))

    all_cards = variables.dashboard_screen.all_cards_on_dashboard
    all_cards_names = all_cards.get_list(True)
    if user_name not in all_cards_names:
        execution.error("User with name: {0} not found on dashboard! Found only cards: {1}".format(user_name, all_cards_names))

    user_index = all_cards.get_index(user_name)
    all_users_names = [user.get_name() for user in variables.users.values()]
    plugin_displayed = None
    if len(all_cards_names) > user_index+1:
        for i in xrange(user_index+1, len(all_cards_names)):
            diff = compare_values(all_cards_names[i], location_text)
            if diff:
                logger.info("Comparing plugin no.{0}... Plugin does not match expected value:\n{1}".format(str(i-user_index), diff))
            else:
                plugin_displayed = True
                logger.info("Comparing plugin no.{0}... Plugin matches expected value: {1}".format(str(i - user_index), location_text))
                break

            # there is another user (==no more plugins for current user) or no more cards
            if all_cards_names[i] in all_users_names or i == (len(all_cards_names)-1):
                plugin_displayed = False
                logger.info("Plugin: {0} not found in {1} plugin card(s) for user: {2}".format(location_text, str(i-user_index), user_name))
    else:
        plugin_displayed = False

    if plugin_displayed != plugin_expected_displayed:
        execution.error("Plugin displayed == {0}, expected state == {1}! Check debug logs for more info...".format(plugin_displayed, plugin_expected_displayed))

    execution.passed()

steps.new_step("FamilyMemberLocation - Family member location card for user {user} on Dashboard is displayed: {bool}", family_member_location_check_opened_status_for_service)


def family_member_location_element_on_card_displayed(params):
    element_name = InputParameterConvertor.check_valid_parameter(params['element_name'].upper(), ['ADDRESS', 'TIMESTAMP'])
    user = variables.users[params['user']]

    label_to_search = user.get_name()
    if label_to_search == variables.logged_user.values()[0].get_name():
        label_to_search = 'Me'

    try:
        if element_name == 'ADDRESS':
            variables.dashboard_screen.get_plugin_status_object_at_index_for_user_name(user_name=label_to_search, plugin_index=1)
        elif element_name == 'TIMESTAMP':
            variables.dashboard_screen.get_plugin_detail_object_at_index_for_user_name(user_name=label_to_search, plugin_index=1)
    except LookupError:
        execution.error("The element {0} was not found in location card for user {1}.".format(element_name, label_to_search))

    logger.info("The element {0} is displayed in location card for user {1}.".format(element_name, user.get_name()))
    execution.passed()

steps.new_step("FamilyMemberLocation - Element {element_name} on Family member location card for user {user} is displayed", family_member_location_element_on_card_displayed)


def family_member_location_correct_address_timestamp_displayed_on_card(params):
    element_name = InputParameterConvertor.check_valid_parameter(params['element_name'].upper(), ["ADDRESS", "TIMESTAMP"])
    option_name = InputParameterConvertor.check_valid_parameter(params['option_name'],
                                                                ["Address level", "Street level", "Post code level", "Town level",
                                                                 "Safe place", "Offline", "Invisible",
                                                                 "Just now", "5m ago", "10m ago", "59m ago", "2h ago", "23h ago", "1d ago", "2d ago"])
    if option_name in ("Safe place", "Offline", "Invisible"):
        execution.error("Address checking for device status Safe place, Offline and Invisible will be implemented later.")

    user = variables.users[params['user_name']]
    label_to_search = user.get_name()
    if label_to_search == variables.logged_user.values()[0].get_name():
        label_to_search = "Me"

    if element_name == 'ADDRESS':
        logger.info("Getting ADDRESS from plugin card for user: {0}".format(user.get_name()))
        plugin_status = variables.dashboard_screen.get_plugin_status_object_at_index_for_user_name(user_name=label_to_search, plugin_index=1)
        address_from_cell = plugin_status.get_text()
        logger.info(u"ADDRESS: {0}".format(address_from_cell))

        accuracy = {"Address level": 5, "Street level": 358, "Post code level": 30000, "Town level": 40000}[option_name]
        location = variables.locations_of_users[user.get_account_id()]['data']  # for each user there are two files saved: 'data' (contains location data) and 'deviceId'
        location["accuracy"] = accuracy
        address_from_google_api = LocationToAddress.location_to_address(location)

        diff = compare_values(address_from_cell, address_from_google_api)
        if diff:
            execution.error("Address with accuracy: {0} for user {1} is not displayed correctly!\n{2}".format(option_name, user.get_name(), diff))

    elif element_name == 'TIMESTAMP':
        logger.info("Getting TIMESTAMP from plugin card for user: {0}".format(user.get_name()))
        plugin_detail = variables.dashboard_screen.get_plugin_detail_object_at_index_for_user_name(user_name=label_to_search, plugin_index=1)
        time_label_from_cell = plugin_detail.get_text()
        logger.info(u"TIMESTAMP: {0}".format(time_label_from_cell))

        if option_name == "Just now":
            if time_label_from_cell not in ["Just now", "1 min"]:
                execution.error("Timestamp with time: Just now for user {0} is not displayed correctly!\nDisplayed: {1}, expected: 'Just now' or '1 min'!".format(user.get_name(), time_label_from_cell))
        elif option_name in ("5m ago", "10m ago", "59m ago", "2h ago", "23h ago", "1d ago", "2d ago"):
            diff = None
            if is_android():
                timestamp_check = TimeConverter.check_timestamp(time_label_from_cell, 60)
                diff = timestamp_check['error_message']
            elif is_ios():
                delta = option_name.split(' ')[0]
                time_label_from_python = TimeConverter.ios_localized_timestamp_for_saved_time_at_creation(delta, format24h=True)
                diff = compare_values(time_label_from_cell, time_label_from_python)
            else:
                execution.error("Specified OS is not supported/implemented")

            if diff:
                execution.error("Timestamp for user {0} is not displayed correctly!\n{1}".format(user.get_name(), diff))
        else:
            execution.error("Timestamp can not have value {0}! Please check step parameters.".format(option_name))

    logger.info("{0} of user {1} is displayed correctly.".format(element_name, user.get_name()))
    execution.passed()

steps.new_step("FamilyMemberLocation - Correct element {element_name} for option {option_name} is displayed on Family member location card for user {user_name}", family_member_location_correct_address_timestamp_displayed_on_card)


def family_member_location_correct_address_is_displayed_on_card(params):
    latitude_value = InputParameterConvertor.convert_to_float(params['latitude_value'])
    longitude_value = InputParameterConvertor.convert_to_float(params['longitude_value'])
    accuracy_value = InputParameterConvertor.convert_to_int(params['accuracy_value'])

    if abs(latitude_value) > 90:
        execution.error("Wrong latitude: {}".format(latitude_value))

    if abs(longitude_value) > 180:
        execution.error("Wrong longitude: {}".format(longitude_value))

    if accuracy_value < 0:
        execution.error("Negative accuracy: {}".format(accuracy_value))

    location = {"latitude": latitude_value, "longitude": longitude_value, "accuracy": accuracy_value}
    address_from_google_api = LocationToAddress.location_to_address(location)

    user = variables.users[params['user']]
    label_to_search = user.get_name()
    if label_to_search == variables.logged_user.values()[0].get_name():
        label_to_search = "Me"

    user_plugin_status = variables.dashboard_screen.get_plugin_status_object_at_index_for_user_name(user_name=label_to_search, plugin_index=1)
    address_from_cell = user_plugin_status.get_text()

    diff = compare_values(address_from_cell, address_from_google_api)
    if diff:
        execution.error("Address of user {0} is not displayed correctly.\n{1}".format(params['user'], diff))

    logger.info("Address of user {0} is displayed correctly.".format(params['user']))
    execution.passed()

steps.new_step("FamilyMemberLocation - Correct address with coordinates {latitude_value}, {longitude_value} and accuracy {accuracy_value} is displayed on Family member location card for user {user}", family_member_location_correct_address_is_displayed_on_card)
