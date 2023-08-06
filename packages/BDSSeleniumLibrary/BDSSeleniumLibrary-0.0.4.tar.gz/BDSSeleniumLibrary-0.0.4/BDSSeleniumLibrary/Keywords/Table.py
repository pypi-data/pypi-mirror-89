from SeleniumLibrary.base import keyword
from BDSSeleniumLibrary.Core import BDSLibraryComponent
from robot.libraries.Collections import Collections

class TableKeywords(BDSLibraryComponent):
    def __init__(self, ctx):
        BDSLibraryComponent.__init__(self, ctx)
    
    def get_table_xpath(self, text_in_column=None, table=1):
        xpath = '(//table[(.//*[(local-name() = "td" or local-name() = "th") and contains(normalize-space(.), "{0}")] or "{0}" = "{1}")])[{2}]'.format(text_in_column, None, table)
        self.wait_until_page_contains_element('', 'xpath={0}'.format(xpath), 120, 'Không tìm thấy table')
        return xpath
    
    def count_table_number(self, text_in_column=None):
        xpath = '//table[(.//*[(local-name() = "td" or local-name() = "th") and contains(normalize-space(.), "{0}")] or "{0}" = "{1}")]'.format(text_in_column, None)
        count = self.get_element_count('xpath={0}'.format(xpath))
        return count

    def get_row_in_table_xpath(self, text_in_column=None, table=1, row=1):
        xpath = self.get_table_xpath(text_in_column, table)
        xpath = '({0}//tr)[{1}]'.format(xpath, row)
        self.wait_until_page_contains_element('', 'xpath={0}'.format(xpath), 120, 'Không tìm thấy row của table')
        self.wait_until_page_contains_element('', 'xpath={0}'.format(xpath), 120, 'Không tìm thấy table')
        return xpath
    
    def count_row_in_table_number(self, text_in_column=None, table=1):
        xpath = self.get_table_xpath(text_in_column, table)
        xpath = '({0}//tr)'.format(xpath)
        count = self.get_element_count('xpath={0}'.format(xpath))
        return count

    def get_column_in_table_xpath(self, text_in_column=None, table=1, row=1, column=1):
        xpath = self.get_row_in_table_xpath(text_in_column, table, row)
        xpath = '({0}/*[local-name() = "td" or local-name() = "th"])[{1}]'.format(xpath, column)
        self.wait_until_page_contains_element('', 'xpath={0}'.format(xpath), 120, 'Không tìm thấy column của table')
        self.wait_until_page_contains_element('', 'xpath={0}'.format(xpath), 120, 'Không tìm thấy table')
        return xpath

    def count_column_in_table_number(self, text_in_column=None, table=1, row=1):
        xpath = self.get_row_in_table_xpath(text_in_column, table, row)
        xpath = '({0}/*[local-name() = "td" or local-name() = "th"])'.format(xpath)
        count = self.get_element_count('xpath={0}'.format(xpath))
        return count


