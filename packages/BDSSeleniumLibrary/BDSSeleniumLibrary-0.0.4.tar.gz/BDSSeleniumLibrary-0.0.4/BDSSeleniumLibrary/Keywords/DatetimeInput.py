from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.DateTime import datetime, convert_date

class DatetimeInputKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    def get_datetime_input(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'input', '@type="date"', 4, index)

    @keyword()
    def wait_until_page_contains_datetime_input(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'input', '@type="date"', 4, timeout, error)

    @keyword()
    def wait_until_page_not_contains_datetime_input(self, text, timeout=None, error=None):
        self.wait_until_page_contains_htmlelement_being_near_text(text, 'input', '@type="hidden"', 4, timeout, error)

    @keyword()
    def wait_until_datetime_input_is_not_visible(self, text, timeout=None, error=None, index=1):
        xpath = self.get_datetime_input(text, index)
        self.wait_until_element_is_not_visible(text, xpath, timeout, error)

    @keyword()
    def wait_until_datetime_input_is_visible(self, text, timeout=None, error=None, index=1):
        xpath = self.get_datetime_input(text, index)
        self.wait_until_element_is_visible(text, xpath, timeout, error)

    @keyword()
    def date_input_should_be_visible(self, text, message=None, index=1):
        xpath = self.get_datetime_input(text, index)
        self.element_should_be_visible(text, xpath, message)
        
    @keyword()
    def date_input_should_not_be_visible(self, text, message=None, index=1):
        xpath = self.get_datetime_input(text, index)
        self.element_should_not_be_visible(text, xpath, message)

    @keyword()
    def wait_until_datetime_input_is_usable(self, text, timeout=None, index=1):
        self.wait_until_page_contains_datetime_input(text, timeout, None)
        self.wait_until_datetime_input_is_visible(text, timeout, None, 1)

    @keyword()
    def set_datetime_input(self, text, date, index=1):
        date = convert_date(date, result_format='%Y-%m-%d')
        self.wait_until_datetime_input_is_usable(text, 120, index)
        xpath = self.get_datetime_input(text, index)
        self.execute_script('$(document.evaluate(`{0}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).val("{0}").change()'.format(xpath, date))

    @keyword('Get Date Of Input [Datetime]')
    def get_datetime_of_input_datetime(self, text, index=1):
        self.wait_until_page_contains_datetime_input(text, 120, None)
        xpath = self.get_datetime_input(text, index)
        date = self.execute_script('$(document.evaluate(`//*[@id="{0}"]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).val()'.format(xpath))
        date = convert_date(date, result_format='datetime')
        return date

    @keyword('Get Max Datetime Of Input [Datetime]')
    def get_max_datetime_of_input_datetime(self, text, index=1):
        self.wait_until_page_contains_datetime_input(text, 120, None)
        xpath = self.get_datetime_input(text, index)
        date = self.execute_script('$(document.evaluate(`//*[@id="{0}"]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).attr("max") ?? ""'.format(xpath))
        if date != '':
            date = convert_date(date, result_format=datetime)
        else:
            date = ''
        return date

    @keyword('Get Min Datetime Of Input [Datetime]')
    def get_min_datetime_of_input_datetime(self, text, index=1):
        self.wait_until_page_contains_datetime_input(text, 120, None)
        xpath = self.get_datetime_input(text, index)
        date = self.execute_script('$(document.evaluate(`//*[@id="{0}"]`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue).attr("min") ?? ""'.format(xpath))
        if date != '':
            date = convert_date(date, result_format=datetime)
        else:
            date = ''
        return date
