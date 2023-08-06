from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.DateTime import datetime, convert_date

class DatetimePickerKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    def jump_to_date(self, text, date, date_format=None, index=1):
        xpath = self.get_datetime_picker_input_xpath(text, index)
        self.ctx.keywords['click_element']('xpath={0}'.format(xpath))
        date = convert_date(date, result_format='datetime')
        selectedDate = self.get_value_of_datetime_picker(text, date_format, index)
        monthDiff = date.month() - selectedDate.month()
        yearDiff = date.year() - selectedDate.year()
        move = yearDiff*12 + monthDiff
        if move < 0:
            move = move * -1
            shiftForward = 0
        else:
            shiftForward = 1

        items = range(move)

        for item in items:
            if shiftForward == 1:
                self.ctx.keywords['click_element']('xpath=//a[./span[contains(text(), \'Prev\')]]')
            if shiftForward == 0:
                self.ctx.keywords['click_element']('xpath=//a[./span[contains(text(), \'Next\')]]')


    def get_datetime_picker_input_xpath(self, text, index=1):
        return self.get_htmlelement_is_near_text(text, 'input', '@type!="hidden" or @id="{0}"'.format(text), 4, index)

    @keyword()
    def get_value_of_datetime_picker(self, text, date_format, index=1):
        xpath = self.get_datetime_picker_input_xpath(text, index)
        value = self.get_element_attribute('xpath={0}'.format(xpath), 'value')
        if value == '':
            year = int(self.get_element_attribute('xpath=//*[@id="ui-datepicker-div"]//select[@class="ui-datepicker-year"]/option[@selected="selected"]', 'value'))
            month = int(self.get_element_attribute('xpath=//*[@id="ui-datepicker-div"]//select[@class="ui-datepicker-month"]/option[@selected="selected"]', 'value'))
            month = month + 1
            monthAsString = str(month)
            if month < 10:
                monthAsString = '0{0}'.format(monthAsString)
                return convert_date('{0}-{0}-01'.format(year, month), result_format='datetime')
        else:
            return convert_date(value, date_format=date_format, result_format='datetime')

    @keyword()
    def set_datetime_picker(self, date, date_format, index=1):
        self.jump_to_date(text, date, date_format, index)
        date = convert_date(date, result_format='datetime')
        self.wait_until_element_is_enabled('datetime picker input', 'xpath=//a[text()="{0}"]'.format(date.day()))
        self.ctx.keywords['click_element']('xpath=//div[@id="ui-datepicker-div"]//table[@class = "ui-datepicker-calendar"]//*[text()="{0}"]'.format(date.day()))

    @keyword()
    def wait_until_datetime_picker_popup_is_closed(self, timeout=None, message=None):
        self.ctx.keywords['wait_until_element_is_not_visible']('xpath=//*[@id="ui-datepicker-div"]', timeout, message)

    @keyword()
    def date_of_datetime_picker_should_be_disabled(self, text, date, date_fromat, index=1):
        self.jump_to_date(text, date, date_fromat, index)
        date = convert_date(date, result_format='datetime')
        classAttr = self.get_element_attribute('xpath=//td[./*[text()="{0}"]]'.format(date.day()), 'class')
        self.ctx.keywords['should_contain'](classAttr, 'ui-datepicker-unselectable', '{0} should be disable. But it was not'.format(date))

    @keyword()
    def date_of_datetime_picker_should_be_enabled(self, text, date, date_fromat, index=1):
        self.jump_to_date(text, date, date_fromat, index)
        date = convert_date(date, result_format='datetime')
        classAttr = self.get_element_attribute('xpath=//td[./*[text()="{0}"]]'.format(date.day()), 'class')
        self.ctx.keywords['should_not_contain'](classAttr, 'ui-datepicker-unselectable', '{0} should be disable. But it was not'.format(date))

    @keyword()
    def value_of_datetime_picker_should_be(self, text, date, date_format, message=None, ignore_case=None, index=1):
        date = convert_date(date, result_format='datetime')
        value = self.get_value_of_datetime_picker(text, date_format, index)

        BuiltIn().should_be_equal_as_strings('{0}/{1}/{2}'.format(value.day(), value.month(), value.year()), '{0}/{1}/{2}'.format(date.day(), date.month(), date.year()), message, True, ignore_case)

    
