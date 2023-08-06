from SeleniumLibrary.base import keyword
from .Table import TableKeywords
from robot.libraries.Collections import Collections

class TableImageKeywords(TableKeywords):
    def __init__(self, ctx):
        TableKeywords.__init__(self, ctx)

    @keyword()
    def image_of_column_in_table_should_be(self, expected, message=None, text_in_column=None, table=1, row=1, column=1):
        xpath = self.get_column_in_table_xpath(text_in_column, table, row, column)
        self.page_should_contain_element('xpath={0}//img[contains(@src, "{1}")]'.format(xpath, expected), message)
