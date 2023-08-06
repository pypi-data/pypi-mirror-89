from SeleniumLibrary.base import keyword
from .Table import TableKeywords
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.Collections import Collections
from robot.libraries.String import String

class TableTextKeywords(TableKeywords):
    def __init__(self, ctx):
        TableKeywords.__init__(self, ctx)

    @keyword('Get Lines Of Row In Table [String]')
    def get_lines_of_row_in_table_string(self, text_in_column=None, table=1, row=1):
        xpath = self.get_row_in_table_xpath(text_in_column, table, row)
        lines = self.get_element_attribute('xpath={0}'.format(xpath), 'outerText')
        return lines
    
    @keyword('Get Line Of Row In Table [String]')
    def get_line_of_row_in_table_string(self, text_in_column=None, table=1, row=1, line=1):
        lines = self.get_lines_of_row_in_table_string(text_in_column, table, row)
        lineAsStrim = String().strip_string(lines.replace("\n", ""))
        if (lineAsStrim == ''):
            return ''
        linesAsArray = String.split_to_lines(lines.replace("\t", "\n"))
        result = BuiltIn().create_list()
        for l in linesAsArray:
            if (l != ''):
                result.append(l)
        if (result.count() == 1):
            return ''
        return linesAsArray[line - 1]

    @keyword('Get Lines Of Column In Table [String]')
    def get_lines_of_column_in_table_string(self, text_in_column=None, table=1, row=1, column=1):
        xpath = self.get_column_in_table_xpath(text_in_column, table, row, column)
        lines = self.get_element_attribute('xpath={0}'.format(xpath), 'outerText')
        return lines

    @keyword('Get HtmlContent Of Column In Table [Html]')
    def get_htmlContent_of_column_in_table_html(self, text_in_column=None, table=1, row=1, column=1):
        xpath = self.get_column_in_table_xpath(text_in_column, table, row, column)
        lines = self.get_element_attribute('xpath={0}'.format(xpath), 'outerHTML')
        return lines

    @keyword('Get Line Of Column In Table [String]')
    def get_line_of_column_in_table_string(self, text_in_column=None, table=1, row=1, column=1, line=1):
        lines = self.get_lines_of_column_in_table_string(text_in_column, table, row, column)
        lineAsStrim = String().strip_string(lines.replace("\n", ""))
        if (lineAsStrim == ''):
            return ''
        linesAsArray = String.split_to_lines(lines.replace("\t", "\n"))
        result = BuiltIn().create_list()
        for l in linesAsArray:
            if (l != ''):
                result.append(l)

        if (result.count() == 1):
            return ''
        return result[line - 1]

    @keyword('Get Line In HtmlContent Of Column In Table [Html]')
    def get_line_in_htmlContent_of_column_in_table_string(self, text_in_column=None, table=1, row=1, column=1, line=1):
        lines = self.get_htmlContent_of_column_in_table_html(text_in_column, table, row, column)
        lineAsStrim = String().strip_string(lines.replace("\n", ""))
        if (lineAsStrim == ''):
            return ''
        linesAsArray = String.split_to_lines(lines.replace("\t", "\n"))
        result = BuiltIn().create_list()
        for l in linesAsArray:
            if (l != ''):
                result.append(l)

        if (result.count() == 1):
            return ''
        return result[line - 1]

    @keyword()
    def line_of_column_in_table_should_be(self, expected, message=None, ignore_true=None, text_in_column=None, table=1, row=1, column=1, line=1):
        text = self.get_line_of_column_in_table_string(text_in_column, table, row, column, line)
        BuiltIn().should_be_equal_as_strings(text, expected, message, True, ignore_case)

    @keyword()
    def line_of_column_in_table_should_not_be(self, expected, message=None, ignore_true=None, text_in_column=None, table=1, row=1, column=1, line=1):
        text = self.get_line_of_column_in_table_string(text_in_column, table, row, column, line)
        BuiltIn().should_not_be_equal_as_strings(text, expected, message, True, ignore_case)
    
    @keyword()
    def line_of_column_in_table_should_contain(self, expected, message=None, ignore_true=None, text_in_column=None, table=1, row=1, column=1, line=1):
        text = self.get_line_of_column_in_table_string(text_in_column, table, row, column, line)
        BuiltIn().should_contain(text, expected, message, True, ignore_case)
    
    @keyword()
    def line_of_column_in_table_should_not_contain(self, expected, message=None, ignore_true=None, text_in_column=None, table=1, row=1, column=1, line=1):
        text = self.get_line_of_column_in_table_string(text_in_column, table, row, column, line)
        BuiltIn().should_not_contain(text, expected, message, True, ignore_case)

    @keyword()
    def column_in_table_should_contain_image(self, expected_url, message=None, ignore_true=None, text_in_column=None, table=1, row=1, column=1):
        html = self.get_htmlContent_of_column_in_table_html(text_in_column, table, row, column)
        BuiltIn().should_contain(html, 'src="{0}"'.format(expected_url), message, True, ignore_case)

    @keyword()
    def line_of_column_in_table_should_contain_image(self, expected_name, message=None, ignore_true=None, text_in_column=None, table=1, row=1, column=1, line=1):
        html = self.get_line_in_htmlContent_of_column_in_table_string(text_in_column, table, row, column, line)
        BuiltIn().should_match_regexp(html, 'src=".*{0}"'.format(expected_name))
