from SeleniumLibrary import SeleniumLibrary
from .Keywords import (
    AdvancedDropdownKeywords,
    CheckBoxKeywords,
    ClickableElementKeywords,
    DatetimeInputKeywords,
    DatetimePickerKeywords,
    FancyBoxKeywords,
    FileInputKeywords,
    InputKeywords,
    MultipleDropdownKeywords,
    RadioKeywords,
    SingleDropdownKeywords,
    TableImageKeywords,
    TableTextKeywords,
    TextKeywords,
    TextAreaKeywords
)

class BDSSeleniumLibrary(SeleniumLibrary):
    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None, plugins=None,
                 event_firing_webdriver=None):
        SeleniumLibrary.__init__(
            self, timeout, implicit_wait, 
            run_on_failure, 
            screenshot_root_directory, plugins,
            event_firing_webdriver)
        
        self.add_library_components([
            AdvancedDropdownKeywords(self),
            CheckBoxKeywords(self),
            ClickableElementKeywords(self),
            DatetimeInputKeywords(self),
            DatetimePickerKeywords(self),
            FancyBoxKeywords(self),
            FileInputKeywords(self),
            InputKeywords(self),
            MultipleDropdownKeywords(self),
            RadioKeywords(self),
            SingleDropdownKeywords(self),
            TableImageKeywords(self),
            TableTextKeywords(self),
            TextKeywords(self),
            TextAreaKeywords(self)
        ])