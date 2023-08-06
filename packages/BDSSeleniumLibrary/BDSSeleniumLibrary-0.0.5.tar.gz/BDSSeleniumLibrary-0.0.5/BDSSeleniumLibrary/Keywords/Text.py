from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.String import String

class TextKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)

    def get_table_containing_text_xpath(self, text, index=1):
        return '(//*[contains(text(), "{0}")]/ancestor::table)[{1}]'.format(text, index)
    
    @keyword()
    def table_containing_text_should_contains_text(self, text, columnIndex, rowIndex, expected, message=None, loglevel='TRACE', limit=None, elementIndex=1, tableIndex=1):
        xpath = self.get_table_containing_text_xpath(text, tableIndex)
        self.page_should_contain_element('xpath=({0}//tr[{1}]/*[{2}]/self::*[contains(normalize-space(.),"{3}")] | {0}//tr[{1}]/*[{2}]//*[contains(normalize-space(.), "{3}")])[{4}]'.format(xpath, rowIndex, columnIndex, expected, elementIndex), message, loglevel, limit)
    
    @keyword('Get Text In Page [List Of String]')
    def get_text_in_page_list_of_string(self, after_text='', before_text=''):
        result = BuiltIn().create_list()
        elements = self.get_webelement('//*[(contains(normalize-space(.), "{0}") or "{0}" = "{1}") and (contains(normalize-space(.), "{2}") or "{2}" = "{1}")]'.format(after_text, None, before_text))

        for element in elements:
            line = self.get_element_attribute(element, outerText)
            text = self.get_text_from_lines_list_of_text(line.replace("\t", "\n"), after_text, before_text)
            result.append(text)
        result = Collections().remove_duplicates(result)
        return result

    @keyword('Get Text In Page [String]')
    def get_text_in_page_string(self, after_text='', before_text='', index=1):
        result = self.get_text_from_lines_list_of_text(after_text, before_text)
        return result[index - 1]

    @keyword()
    def text_in_page_should_be(self, expected, message=None, ignore_case=False, after_text='', before_text='', index=1):
        text = self.get_text_in_page_string(after_text, before_text)
        text = text.strip()
        return text

    @keyword('Get Number In Page [Number]')
    def get_number_in_page_number(self, after_text='', before_text='', format=',', index=1):
        lines = self.get_text_in_page_list_of_string(after_text, before_text)
        result = BuiltIn().create_list()
        for line in lines:
            numbers = self.get_number_from_lines_list_of_number(text, format)
            for number in numbers:
                result.append(number)
        result = Collections().remove_duplicates(result)
        return result[index - 1]

    @keyword('Get Line In Same Space With Image [String]')
    def get_line_in_same_space_with_image_string(self, img, image_index=1, scope=1, line=1):
        text_content = self.get_element_attribute('(//img[contains(@src, "{0}") and position() = {1}]/ancestor::*[normalize-space(.) != ""])[last() - ${scope - 1}]'.format(img, image_index), 'outerText')
        text_content = String().replace_string_using_regexp(text_content, r'[ ]{2,}', '')
        result = String().split_to_lines(text_content.replace('\t', ''))
        Collections().remove_values_from_list(result, '')
        return result[line - 1]

    @keyword('Get Number Of Line In Same Space With Image [Number]')
    def get_number_of_line_in_same_space_with_image_number(self, img, image_index=1, scope=1, line_index=1, format=',', number_index=1):
        line = self.get_line_in_same_space_with_image_string(img, image_index, scope, line_index)
        number = self.get_number_from_lines_number(line, format, number_index)
        return number

    @keyword()
    def line_in_same_space_with_image_should_be(self, img, expected, image_index=1, messgae=None, ignore_case=False, scope=1, line_index=1):
        line = self.get_line_in_same_space_with_image_string(img, image_index, scope, line_index).strip()
        BuiltIn().should_be_equal_as_strings(line, expected, messgae, ignore_case)

    @keyword()
    def number_of_line_in_same_space_with_image_should_be(self, img, expeced, image_index=1, message=None, scope=1, line_index=1, format=',', number_index=1):
        number = get_number_of_line_in_same_space_with_image_number(img, image_index, scope, line_index, format, number_index)
        BuiltIn().should_not_be_equal_as_numbers(number, expected, messgae)

    @keyword()
    def number_of_line_in_same_space_with_image_more_than(self, img, expeced: int, image_index=1, message=None, scope=1, line_index=1, format=',', number_index=1):
        number = get_number_of_line_in_same_space_with_image_number(img, image_index, scope, line_index, format, number_index)
        result = number > expeced
        BuiltIn().should_not_be_equal_as_strings(result, 'True', message)

    @keyword()
    def number_of_line_in_same_space_with_image_more_than_or_equal_to(self, img, expeced: int, image_index=1, message=None, scope=1, line_index=1, format=',', number_index=1):
        number = get_number_of_line_in_same_space_with_image_number(img, image_index, scope, line_index, format, number_index)
        result = number >= expeced
        BuiltIn().should_not_be_equal_as_strings(result, 'True', message)

    @keyword()
    def number_of_line_in_same_space_with_image_less_than(self, img, expeced: int, image_index=1, message=None, scope=1, line_index=1, format=',', number_index=1):
        number = get_number_of_line_in_same_space_with_image_number(img, image_index, scope, line_index, format, number_index)
        result = number < expeced
        BuiltIn().should_not_be_equal_as_strings(result, 'True', message)
        
    @keyword()
    def number_of_line_in_same_space_with_image_less_than_or_equal_to(self, img, expeced: int, image_index=1, message=None, scope=1, line_index=1, format=',', number_index=1):
        number = get_number_of_line_in_same_space_with_image_number(img, image_index, scope, line_index, format, number_index)
        result = number <= expeced
        BuiltIn().should_not_be_equal_as_strings(result, 'True', message)

    @keyword
    def wait_until_page_contains_text(self, text, timeout=None, error=None, index=1):
        if error == None:
            error = 'Không thể tìm thấy text "{0}"'.format(text)
        self.wait_until_page_contains_element(text, '(((//*[contains(., "{0}")])/text())[contains(., "{0}")]/..)[{1}]'.format(text, index), timeout, error)
        
    @keyword
    def wait_until_text_is_visible(self, text, timeout=None, error=None, index=1):
        if error == None:
            error = '"{0}" không được hiển thị'.format(text)
        self.wait_until_page_contains_element(text, '(((//*[contains(., "{0}")])/text())[contains(., "{0}")]/..)[{1}]'.format(text, index), timeout, error)

    @keyword
    def wait_until_page_does_not_contain_text(self, text, timeout=None, error=None, index=1):
        if error == None:
            error = 'Vẫn thể tìm thấy text "{0}"'.format(text)
        self.wait_until_page_contains_element(text, '(((//*[contains(., "{0}")])/text())[contains(., "{0}")]/..)[{1}]'.format(text, index), timeout, error)