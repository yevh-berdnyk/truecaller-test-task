from appium.webdriver import Remote, WebElement
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BaseElement:

    def __init__(self, driver: Remote, locator_value: str, locator_by: str = MobileBy.ID):
        self.driver = driver
        self.locator_value = locator_value
        self.locator_by = locator_by

    def wait_for_element(self, timeout: int = 3) -> WebElement:
        return WebDriverWait(driver=self.driver, timeout=timeout) \
            .until(expected_conditions.presence_of_element_located((self.locator_by, self.locator_value)))

    def is_visible(self) -> bool:
        try:
            return self.wait_for_element().is_displayed()
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            return False


class BaseButton(BaseElement):
    def __init__(self, driver: Remote, locator_value: str, locator_by: str = MobileBy.ID, return_view=None):
        super(BaseButton, self).__init__(driver=driver, locator_value=locator_value, locator_by=locator_by)
        self.return_view = return_view

    def click(self):
        self.wait_for_element().click()
        return self.return_view


class BaseInput(BaseElement):

    def __init__(self, driver: Remote, locator_value: str, locator_by: str = MobileBy.ID):
        super(BaseInput, self).__init__(driver=driver, locator_value=locator_value, locator_by=locator_by)

    def set_value(self, value) -> None:
        self.wait_for_element().set_value(value)


class BaseText(BaseElement):
    def __init__(self, driver: Remote, locator_value: str, locator_by: str = MobileBy.ID):
        super(BaseText, self).__init__(driver=driver, locator_value=locator_value, locator_by=locator_by)

    @property
    def text(self) -> str:
        return self.wait_for_element().text
