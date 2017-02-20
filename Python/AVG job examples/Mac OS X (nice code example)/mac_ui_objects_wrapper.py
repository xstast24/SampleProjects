from atomac._a11y import ErrorUnsupported
from atomac.AXClasses import NativeUIElement


class SelectorType:
    id = 'AXIdentifier'
    identifier = 'AXIdentifier'
    class_name = 'AXRole'
    role = 'AXRole'
    enabled = 'AXEnabled'
    focused = 'AXFocused'
    value = 'AXValue'
    title = 'AXTitle'
    placeholder = 'AXPlaceholderValue'


class AtomacObject:
    """
    This class is the base object for Mac UI automation mapping. Searches for the first element matching criteria and perform an action on it.
    Supported methods:
    wait_for()
    click()
    right_click()
    clear()
    get_text()
    set_text()
    append_text()
    get_position()
    get_size()
    get_class_name()
    get_attribute()
    list_supported_attributes()
    is_enabled()
    is_displayed()
    get_element()
    """
    def __init__(self, app, selector=None, selector_type=SelectorType.id, selectors=None, selectors_types=None, index=0, parent=None, direct_child_only=False):
        """
        By default, new element is searched in whole app scope. The search is based on selector or multiple selectors.
        If a parent is given, new element is searched in parent's scope. If direct_child_only, new element is searched only in direct children of app or parent.
        If selectors and selectors_types are given, new element is searched by this criteria, not using selector and selector_type parameter.
        :param app: Pyatom element, application launched by bundle_id
        :param selector: selector to identify the desired element
        :param selector_type: type of selector from class SelectorType, the default selector is accessibility IDentifier
        :param selectors: list - list of selectors to identify the desired element, each selector must have its type specified in 'selectors_types' argument
        :param selectors_types: list - list of selectors types from class SelectorType to match all the selectors in list of selectors in 'selectors' argument
        :param index: integer - index of element, in case that search procedure would return an array of elements
        :param parent: AtomacObject or Pyatom element; if a parent is given, the new element will be searched only in the parent's scope
        :param direct_child_only: True - return only element's direct child / False - return child of the element or child of any recursive children elements
        """
        self.app = app
        self.selector = selector
        self.selector_type = selector_type
        self.selectors = selectors
        self.selectors_types = selectors_types
        self.index = index
        self.parent = parent
        self.direct_children_only = direct_child_only

    def click(self):
        """
        Left mouse click in the middle of the element.
        """
        element = self.get_element()
        position = element.AXPosition
        size = element.AXSize
        element.clickMouseButtonLeft((position[0] + size[0] / 2, position[1] + size[1] / 2))

    def right_click(self):
        """
        Right mouse click in the middle of the element.
        """
        element = self.get_element()
        position = element.AXPosition
        size = element.AXSize
        element.clickMouseButtonRight((position[0] + size[0] / 2, position[1] + size[1] / 2))

    def clear(self):
        """
        Delete all characters in a textfield. Raising exception if the element is not a text field.
        """
        from atomac.AXKeyCodeConstants import DELETE

        element = self.get_element()
        if element.AXRole != u"AXTextField":
            raise Exception("Can not clear a text in the given element. The element is not a text field!")
        # triple click to select the whole field content, send DELETE to erase the text
        position = element.AXPosition
        size = element.AXSize
        element.tripleClickMouse((position[0] + size[0] / 2, position[1] + size[1] / 2))
        element.sendKeys([DELETE])

    def clear_alternative(self):
        """
        Delete all characters in a text field - alternative to clear() in case GUI is glitchy
        """
        from atomac.AXKeyCodeConstants import BACKSPACE, DELETE

        element = self.get_element()
        count = self.get_attribute('AXNumberOfCharacters')
        self.click()
        for i in range(count):
            element.sendKeys([BACKSPACE])
            element.sendKeys([DELETE])

    def get_text(self):
        """
        Get text from the element. AXValue for text fields, AXTitle for buttons.
        :return text: unicode string with text of the element
        """
        element = self.get_element()
        try:
            return element.AXValue
        except ErrorUnsupported:
            return element.AXTitle

    def set_text(self, text):
        """
        Set text of the given text field to the desired value (clear text field and set the new text).
        :param text: text which should be written to the text field
        """
        self.clear()
        self.get_element().sendKeys(text)

    def append_text(self, text):
        """
        Append text of the given text field.
        :param text: text which should be appended to the text field
        """
        from atomac.AXKeyCodeConstants import DOWN

        try:
            # text is sent to the focused element, so click into the text field
            self.click()
            # then send DOWN (down arrow) key to get to the end of text in field, because before we clicked in the middle of element
            self.get_element().sendKey(DOWN)
            # finally send the text
            self.get_element().sendKeys(text)
        except ErrorUnsupported:
            raise Exception("Can not write a text to the given element. The element is not a text field!")

    def get_position(self):
        """
        Get a position of the element.
        :return dictionary {'x': posX, 'y': posY}
        """
        position = self.get_element().AXPosition
        return {'x': position[0], 'y': position[1]}

    def get_size(self):
        """
        Get a size of the element.
        :return dictionary {'width': sizeX, 'height': sizeY}
        """
        size = self.get_element().AXSize
        return {'width': size[0], 'height': size[1]}

    def get_class_name(self):
        """
        Get a class name of the element, eg. AXButton, AXStaticText.
        """
        return self.get_element().AXRole

    def get_accessibility_id(self):
        """
        Get accessibility identifier of the element.
        """
        return self.get_element().AXIdentifier

    def get_attribute(self, attribute):
        """
        Get accessibility attribute of the element. Use list_supported_attributes() to get names of all available attributes of the element.
        :param attribute: string - name of the attribute, eg. AXNumberOfCharacters, AXValue
        :return attribute value
        """
        try:
            return self.get_element()._getAttribute(attribute)
        except ErrorUnsupported:
            raise Exception("Attribute: '{0}' is not supported by this UI element. Use element.list_supported_attributes().")

    def list_supported_attributes(self):
        """
        List all attributes available for the element.
        :return list of supported attributes' names
        """
        return self.get_element().getAttributes()

    def is_enabled(self):
        """
        Check if button is enabled.
        :return True = enabled / False = disabled
        """
        return self.get_element().AXEnabled

    def is_displayed(self):
        """
        Try to find the element. If found -> displayed, if not found -> missing or hidden.
        :return True = displayed / False = not found
        """
        try:
            self.get_element()
            return True
        except LookupError:
            return False

    def wait_for(self, timeout_seconds, period_seconds=1):
        """
        Trying to find the element every 'period' in given 'timeout'. If not found, raises exception. If found, return waiting time in seconds.
        :param timeout_seconds: maximal time waiting for the element (seconds)
        :param period_seconds: retry the searching every 'period' (seconds)
        :return time: time in seconds, how long has been the element waited for
        """
        from time import sleep, time

        start = time()
        end = start + timeout_seconds
        while time() < end:
            try:
                self.get_element()
                return time() - start
            except LookupError:
                sleep(period_seconds)

        raise AssertionError("Waiting for element {0}={1} was not successful in {2}s.".format(self.selector_type if self.selector else self.selectors_types, self.selector if self.selector else self.selectors, timeout_seconds))

    def save_screenshot(self, path):
        """
        Get and save screenshot of element or window.
        :param path: path to save the screenshot file; eg. screen.png, /path/to/image.png
        """
        from atomac.ldtpd.generic import Generic
        from cStringIO import StringIO
        from PIL import Image

        # capture the app window screen and load it as Image using PIL
        generic = Generic()
        image_base64_string = generic.imagecapture(window_name=self.app.windows()[0].AXTitle)
        image = StringIO(image_base64_string.decode('base64'))
        image = Image.open(image)

        # get app window position
        app_pos_x, app_pos_y = self.app.windows()[0].AXPosition
        # get element position and size
        elem_pos_x, elem_pos_y = self.get_element().AXPosition
        elem_size_x, elem_size_y = self.get_element().AXSize
        # count element's relative position
        pos_x = elem_pos_x - app_pos_x
        pos_y = elem_pos_y - app_pos_y
        # crop and save the image
        image = image.crop((int(pos_x), int(pos_y), int(pos_x+elem_size_x), int(pos_y+elem_size_y)))
        image.save(path)

    def get_element(self):
        # check valid parent
        if isinstance(self.app, NativeUIElement):
            parent_element = self.app
        else:
            raise Exception("Can not get the app reference!")

        if self.parent is not None:
            if isinstance(self.parent, AtomacObject):
                parent_element = self.parent.get_element()
            elif isinstance(self.parent, NativeUIElement):
                parent_element = self.parent
            else:
                raise Exception("Unknown parent element type!")

        # get selectors
        if self.selectors is None and self.selectors_types is None:
            params = {self.selector_type: self.selector}
        elif self.selectors is not None and self.selectors_types is not None:
            if len(self.selectors) == len(self.selectors_types):
                    i = 0
                    params = {}
                    for selector in self.selectors:
                        params[self.selectors_types[i]] = selector
                        i += 1
            else:
                raise Exception("Number of selectors and selectors_types does not match - {0} : {1}!".format(len(self.selectors), len(self.selectors_types)))
        else:
            raise Exception("Selectors and selectors_types does not match - {0} : {1}!".format(self.selectors, self.selectors_types))

        # look up the elements
        children = None
        child = None
        if self.direct_children_only:
            if self.index == 0:
                child = parent_element.findFirst(**params)
            else:
                children = parent_element.findAll(**params)
        else:
            if self.index == 0:
                child = parent_element.findFirstR(**params)
            else:
                children = parent_element.findAllR(**params)

        # if there were more responses, choose by self.index parameter
        if children is not None and len(children) > abs(self.index):
            child = children[self.index]

        # return the element
        if child:
            return child
        else:
            raise LookupError("There is no element given element for {0} and index: {1}!".format(params, self.index))
