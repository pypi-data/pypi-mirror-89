from SeleniumLibrary.base import LibraryComponent
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from SeleniumLibrary.base import keyword
from robot.libraries.DateTime import datetime, convert_date, add_time_to_date

class BDSLibraryComponent(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    #region core businesses

    def get_xpath_of_element_near_xpath(self, root_xpath, type, condition='1=1', level=4):
        for l in range(1, level):
            count_of_element = self.get_element_count('xpath=({0}/ancestor::*[{1}]//{2})[{3}]'.format(root_xpath, l, type, condition))
            if (count_of_element > 0):
                break

        if count_of_element == 0:
            return None
        count_of_element = self.get_element_count('xpath=({0}/ancestor-or-self::{1})[{2}]'.format(root_xpath, type, condition))
        if count_of_element > 0:
            return '(({0}/ancestor-or-self::{1})[{2}])[1]'.format(root_xpath, type, condition)

        count_of_element = self.get_element_count('xpath=({0}/ancestor-or-self::*[{1}]//{2})[{3}]'.format(root_xpath, l, type, condition))
        if count_of_element > 0:
            return '(({0}/ancestor-or-self::*[{1}]//{2})[{3}])[1]'.format(root_xpath, l, type, condition)
        
        count_of_element = self.get_element_count('xpath=({0}/ancestor-or-self::*[{1}]/following-sibling::{2})[{3}]'.format(root_xpath, l, type, condition))
        if count_of_element > 0:
            return '(({0}/ancestor-or-self::*[{1}]/following-sibling::{2})[{3}])[1][1]'.format(root_xpath, l, type, condition)

        count_of_element = self.get_element_count('xpath=({0}/ancestor-or-self::*[{1}]/following-sibling::*[position()<4]//{2})[{3}]'.format(root_xpath, l, type, condition))
        if count_of_element > 0:
            return '(({0}/ancestor-or-self::*[{1}]/following-sibling::*[position()<4]//{2})[{3}])[1]'.format(root_xpath, l, type, condition)
        return '(({0}/ancestor::*[{1}]//{2})[{3}])[1]'.format(root_xpath, l, type, condition)

    def get_htmlelement_is_near_text(self, text, type, condition='1=1', level=4, index=1):
        xpath = '//*[normalize-space(.) = "{0}" or normalize-space(text()) = "{0}" or @id = "{0}" or (local-name() = "input" and @placeholder="{0}")]'.format(text)
        count = self.get_element_count('xpath={0}'.format(xpath))
        if count == 0:
            raise AssertionError('Không thể tìm thấy đối tượng nào với văn bản là {0}'.format(text))
        result = []
        for i in range(1, count + 1):
            item = self.get_xpath_of_element_near_xpath('({0})[{1}]'.format(xpath, i), type, condition)
            if item != None:
                result.append(item)
        
        if len(result) < 1:
            raise AssertionError('Không thể tìm thấy đối tượng nào với văn bản là {0}'.format(text))
        return result[index - 1]
    
    def wait_until_page_contains_htmlelement_being_near_text(self, text, type, condition='1=1', level=4, timeout=None, error=None):
        xpath = '(//*[normalize-space(.) = "{0}" or (@placeholder = "{0}" and local-name() = "input") or @id = "{0}"]/ancestor::*[position() < {1}]//{2})[{3}]'.format(text, level, type, condition)
        self.wait_until_page_contains_element(text, xpath, timeout, error)

    def wait_until_page_does_not_contain_htmlelement_being_near_text(self, text, type, condition='1=1', level=4, timeout=None, error=None):
        xpath = '(//*[normalize-space(.) = "{0}" or (@placeholder = "{0}" and local-name() = "input")]/ancestor::*[position() < {1}]//{2})[{3}]'.format(text, level, type, condition)
        self.wait_until_page_does_not_contain_element(text, xpath, timeout, error)

    #endregion


    #region page contain
    
    def wait_until_page_contains_element(self, text, xpath, timeout=None, error=None):
        if error == None:
            error = self.build_default_error(text, xpath, 'wait_until_page_contains_element', None, timeout)
        self.ctx.keywords['wait_until_page_contains_element']('xpath={0}'.format(xpath), timeout, error)

    def wait_until_page_does_not_contain_element(self, text, xpath, timeout=None, error=None):
        if error == None:
            error = self.build_default_error(text, xpath, 'wait_until_page_does_not_contain_element')
        self.ctx.keywords['wait_until_page_does_not_contain_element']('xpath={0}'.format(xpath), timeout, error)
        
    def page_should_contain_element(self, text, xpath, message=None, loglevel='TRACE', limit=None):
        if message == None:
            message = self.build_default_error(text, xpath, 'page_should_contain_element')
        self.ctx.keywords['page_should_contain_element']('xpath={0}'.format(xpath), message, loglevel, limit)

    #endregion


    #region visiable

    def wait_until_element_is_visible(self, text, xpath, timeout=None, error=None):
        if error == None:
            error = self.build_default_error(text, xpath, 'wait_until_element_is_visible', None, timeout)
        self.ctx.keywords['wait_until_element_is_visible']('xpath={0}'.format(xpath), timeout, error)

    def wait_until_element_is_not_visible(self, text, xpath, timeout=None, error=None):
        if error == None:
            error = self.build_default_error(text, xpath, 'wait_until_element_is_not_visible', None, timeout)
        self.ctx.keywords['wait_until_element_is_not_visible']('xpath={0}'.format(xpath), timeout, error)
        
    def element_should_be_visible(self, text, xpath, message=None):
        if message == None:
            message = self.build_default_error(text, xpath, 'element_should_be_visible')
        self.ctx.keywords['element_should_be_visible']('xpath={0}'.format(xpath), message)

    def element_should_not_be_visible(self, text, xpath, message=None):
        if message == None:
            message = self.build_default_error(text, xpath, 'element_should_not_be_visible')
        self.ctx.keywords['element_should_not_be_visible']('xpath={0}'.format(xpath), message)

    #endregion


    #region enable

    def wait_until_element_is_enabled(self, text, xpath, timeout=None, error=None):
        if error == None:
            error = self.build_default_error(text, xpath, 'wait_until_element_is_enabled')
        self.ctx.keywords['wait_until_element_is_enabled']('xpath={0}'.format(xpath), timeout, error)

    def element_should_be_disabled(self, xpath):
        self.ctx.keywords['element_should_be_disabled']('xpath={0}'.format(xpath))

    def element_should_be_enabled(self, xpath):
        self.ctx.keywords['element_should_be_enabled']('xpath={0}'.format(xpath))

    #endregion


    #region text in html element

    def text_of_element_should_be(self, locator, expected, message, ignore_case=False):
        text = self.get_element_attribute(locator, textContent)
        BuiltIn().should_be_equal_as_strings(text, expected, message, True, ignore_case)

    def text_of_element_should_not_be(self, locator, expected, message, ignore_case=False):
        text = self.get_element_attribute(locator, textContent)
        BuiltIn().should_not_be_equal_as_strings(text, expected, message, True, ignore_case)

    #endregion


    #region value 

    def textfield_value_should_be(self, text, xpath, expected, message=None):
        if error == None:
            error = self.build_default_error(text, xpath, 'textfield_value_should_be', expected)
        self.ctx.keywords['textfield_value_should_be']('xpath={0}'.format(xpath), expected, message)

    def textfield_should_contain(self, text, xpath, expected, message=None):
        if error == None:
            error = self.build_default_error(text, xpath, 'textfield_should_contain', expected)
        self.ctx.keywords['textfield_should_contain']('xpath={0}'.format(xpath), expected, message)

    #endregion


    #region supports

    def fix_xpath(self, xpath, text):
        text = BuiltIn().convert_to_string(text)
        if text.find('"') > 0:
            xpath = xpath.replace('"{0}"'.format(text), "'{text}'".format(text))
        return xpath

    def build_default_error(self, text, xpath, keyword, value=None, timeout=None):
        if keyword == 'wait_until_element_is_enabled':
            return 'Không thể thao tác với đổi tượng. {0} \n xpath: {1}'.format(text, xpath)

        if keyword == 'wait_until_element_is_visible':
            return 'Đối tượng {0} không được hiển thị trong vòng {1} giây. \n xpath: {2}'.format(text, timeout, xpath)

        if keyword == 'wait_until_element_is_not_visible':
            return 'Đối tượng {0} vẫn được hiển thị sau {1} giây. \n xpath: {2}'.format(text, timeout, xpath)

        if keyword == 'element_should_be_visible':
            return 'Đối tượng {0} không được hiển thị. \n xpath: {1}'.format(text, xpath)

        if keyword == 'element_should_not_be_visible':
            return 'Đối tượng {0} vẫn được hiển thị. \n xpath: {1}'.format(text, xpath)

        if keyword == 'textfield_value_should_be':
            return 'Giá trị của đối tượng {0} không phải là {1}. \n xpath: {2}'.format(text, value, xpath)

        if keyword == 'textfield_should_contain':
            return 'Giá trị của đối tượng {0} không chứa {1}. \n xpath: {2}'.format(text, value, xpath)

        if keyword == 'page_should_contain_element':
            return 'Đối tượng {0} không được tìm thấy. \n xpath: {1}'.format(text, xpath)

        if keyword == 'wait_until_page_contains_element':
            return 'Đối tượng {0} không được tìm thấy trong vòng {1} giây. \n xpath: {2}'.format(text, timeout, xpath)

        if keyword == 'wait_until_page_does_not_contain_element': 
            return 'Đối tượng {0} vẫn được tìm thấy trong vòng {1} giây. \n xpath: {2}'.format(text, timeout, xpath)

    def get_webelement(self, locator):
        return self.ctx.keywords['get_webelement'](locator)

    def get_element_attribute(self, locator, attribute):
        return self.ctx.keywords['get_element_attribute'](locator, attribute)

    def get_element_count(self, locator):
        return self.ctx.keywords['get_element_count'](locator)

    def execute_script(self, script):
        self.ctx.driver.execute_script(script)

    #endregion


    #region click action
    
    def click_element_by_javascript(self, xpath):
        self.ctx.driver.execute_script
        is_in_iframe = self.ctx.driver.execute_script('return window.location !== window.parent.location')
        if is_in_iframe == False:
            self.execute_script('document.evaluate(`{0}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()'.format(xpath))
            return True
        else:
            return False
            

    def click_clickable_element_with_xpath(self, xpath):
        is_pass = self.click_element_by_javascript(xpath)
        if is_pass == False:
            tag_name = self.get_element_attribute('xpath={0}'.format(xpath), 'tagName')
            if tag_name == 'INPUT':
                self.ctx.keywords['click_button']('xpath={0}'.format(xpath))
            else:
                self.ctx.keywords['click_element']('xpath={0}'.format(xpath))


    #endregion

    #region support keywords

    @keyword('Get Number From Lines [List Of Number]')
    def get_number_from_lines_list_of_number(self, text, format=','):
        numbers = String().get_regexp_matches(text, '([-]{0,1}[0-9][0-9,\.]+|[\\d])')
        result = BuiltIn().create_list()
        for number in numbers:
            if format == ',':
                number = number.replace('.', '').replace(',', '.')
            else:
                number = number.replace(',', '')
            number = BuiltIn().convert_to_number(number)
            Collections().append_to_list(result, number)
        return result

    @keyword('Get Number From Lines [Number]')
    def get_number_from_lines_number(self, text, format=',', index=1):
        numbers = String().get_regexp_matches(text, '([-]{0,1}[0-9][0-9,\.]+|[\\d])')
        length = BuiltIn().get_length(numbers)
        if length == 0:
            BuiltIn().fail('Không tim thấy số nào hợp lệ')
        if length < index:
            BuiltIn().fail('Số thứ tự được chuyền vào không hợp lệ')
        result = numbers[index - 1]
        if format == ',':
            result = result.replace('.', '').replace(',', '.')
        else:
            result = result.replace(',', '')
        result = BuiltIn().convert_to_number(result)
        result_as_int = BuiltIn().convert_to_integer(result)
        if result == result_as_int:
            result = result_as_int
        return result

    @keyword('Number To Money')
    def number_to_money(self, number: int):
        millions = number / 1000000
        millions = BuiltIn().convert_to_string(millions)
        millions = BuiltIn().convert_to_number(millions, 3)

        percent = number % 1000000
        if number % 1000000 == 0:
            interger = BuiltIn()._convert_to_integer(millions)
        if number > 1000000:
            if percent == 0:
                return '{0} triệu'.format(interger)
            if percent != 0:
                return '{0} triệu'.format(millions)

        hundreds = number / 1000
        hundreds = BuiltIn().convert_to_string(hundreds)
        hundreds = BuiltIn().convert_to_number(hundreds, 2)
        
        percent = number % 1000
        if percent == 0:
            hundreds = BuiltIn().convert_to_integer(hundreds)
        if number < 1000000:
            if percent != 0:
                return '{0} nghìn'.format(hundreds)
            if percent == 0:
                return '{0} nghìn'.format(interger)

    @keyword('Get Text From Lines [List Of Text]')
    def get_text_from_lines_list_of_text(self, text, after_text='', before_text=''):
        result = String().get_regexp_matches(text, '(?<={0}).*(?={1})'.format(after_text, before_text))
        return result

    @keyword()
    def year_is_lear_year(self, year: int):
        return (year % 4 == 0 and year % 100 != 0) or (year % 100 == 0 and year % 400 == 0)

    @keyword()
    def date_is_in_leap_year(self, date):
        date = convert_date(date, result_format='datetime')
        result = self.year_is_lear_year(date.year())
        return result

    @keyword()
    def get_max_day_of_year(self, year: int):
        isLeapYear = self.year_is_lear_year(year)
        if isLeapYear == True:
            return 366
        else:
            return 365

    @keyword()
    def get_max_day_of_month(self, month: int, year: int):
        isLeapYear = self.year_is_lear_year(year)
        if (month == 1 or motnh == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
            return 31
        elif month == 4 or month == 6 or month == 9 or month == 11:
            return 30
        elif isLeapYear == True:
            return 29
        else:
            return 28

    @keyword()
    def add_day_to_date(self, day: int):
        date = add_time_to_date(date, '{0} d'.format(day))
        return date

    @keyword()
    def add_month_to_date(self, date, month):
        date = convert_date(date, result_format='datetime')
        totalDay = 0
        month = range(month)
        for m in month:
            m = (date.month() + 1) % 12
            y = date.year()
            if (m == 0):
                m = 12
                y = y + 1
            maxDay = self.get_max_day_of_month(m, y)
            totalDay = totalDay + maxDay
        date = add_time_to_date(date, '{0} d'.format(totalDay))
        return date

    def build_regex_from_date_format(self, date_format):
        regex = String().replace_string(date_format, '%D', r'%d')
        regex = String.replace_string(regex, '%d', r'[\\d]{2}')
        regex = String.replace_string(regex, '%M', r'%m')
        regex = String.replace_string(regex, '%m', r'[\\d]{2}')
        regex = String.replace_string(regex, '%Y', r'%y')
        regex = String.replace_string(regex, '%y', r'[\\d]{2,4}')
        regex = String.replace_string(regex, '%H', r'%h')
        regex = String.replace_string(regex, '%h', r'[\\d]{2}')
        regex = String.replace_string(regex, '%M', r'%m')
        regex = String.replace_string(regex, '%m', r'[\\d]{2}')
        regex = String.replace_string(regex, '%S', r'%s')
        regex = String.replace_string(regex, '%s', r'[\\d]{2}')
        regex = String.replace_string(regex, '/', '\\/')
        return regex

    def get_datetime_from_lines_datetime(self, text, date_format, index=1):
        regex = self.build_regex_from_date_format(date_format)
        date = String().get_regexp_matches(text, regex)
        length = BuiltIn().get_length(date)
        if (length == 0):
            BuiltIn().fail('Không tim thấy ngày nào hợp lệ')
        if (length < index):
            BuiltIn().fail('Số thứ tự được chuyền vào không hợp lệ')
        result = convert_date(date[index - 1], date_format=date_format, result_format='datetime')
        return result

    #endregion