import time

from appium.webdriver import Remote
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, InvalidElementStateException
from typing import Dict

from elements import BaseButton, BaseInput, BaseText


class BaseView:
    def __init__(self, driver: Remote):
        self.driver = driver
        self.next_button = BaseButton(driver=self.driver, locator_value='com.truecaller:id/nextButton')
        self.continue_button = BaseButton(driver=self.driver, locator_value='android:id/button1')
        self.cancel_button = BaseButton(driver=self.driver, locator_value='android:id/button2')
        self.next = BaseButton(driver=self.driver, locator_value='com.truecaller:id/next')


class StartView(BaseView):
    def __init__(self, driver: Remote):
        super(StartView, self).__init__(driver)
        self.get_started_button = self.next_button
        self.allow_button = BaseButton(driver=self.driver,
                                       locator_value='com.android.packageinstaller:id/permission_allow_button')
        self.number_button = BaseButton(driver=self.driver, locator_value='com.truecaller:id/wizard_subscription_name',
                                        return_view=CreateProfileView)
        self.agree_button = BaseButton(driver=self.driver, locator_value='com.truecaller:id/agreeButton')

    def allow_permissions(self) -> None:
        if self.cancel_button.is_visible():
            self.cancel_button.click()
        if self.continue_button.is_visible():
            self.continue_button.click()
        if self.allow_button.is_visible():
            for _ in range(4):
                self.allow_button.click()


class CreateProfileView(BaseView):
    def __init__(self, driver: Remote):
        super(CreateProfileView, self).__init__(driver)
        self.type_name_button = BaseButton(driver=self.driver, locator_value='com.truecaller:id/manualInputButton')
        self.first_name_input = BaseInput(driver=self.driver, locator_value='com.truecaller:id/firstName')
        self.last_name_input = BaseInput(driver=self.driver, locator_value='com.truecaller:id/lastName')
        self.later_button = BaseButton(driver=self.driver, locator_value="//*[@text='LATER']",
                                       locator_by=MobileBy.XPATH, return_view=CallsView)

    def fill_profile(self) -> None:
        if not self.next.is_visible():
            self.type_name_button.wait_for_element(timeout=30)
            self.type_name_button.click()
            self.first_name_input.set_value('Test')
            self.last_name_input.set_value('Name')
            self.next_button.click()
        for _ in range(3):
            self.next.click()
        self.cancel_button.click()
        time.sleep(1)
        self.cancel_button.click()
        self.next.click()
        self.later_button.click()


class CallsView(BaseView):
    def __init__(self, driver: Remote):
        super(CallsView, self).__init__(driver)
        self.truecaller_logo = BaseButton(driver=self.driver, locator_value='com.truecaller:id/truecaller_logo',
                                          return_view=SearchView)


class UserInfoView(BaseView):
    def __init__(self, driver: Remote):
        super(UserInfoView, self).__init__(driver)
        self.user_name_text = BaseText(driver=self.driver, locator_value='com.truecaller:id/name_or_number')
        self.email_text = BaseText(
            driver=self.driver,
            locator_value="(//*[contains(@resource-id,'callerDetailedUserInfoContainer')]//android.widget.TextView)[1]",
            locator_by=MobileBy.XPATH)
        self.location_text = BaseText(
            driver=self.driver,
            locator_value="(//*[contains(@resource-id,'callerDetailedUserInfoContainer')]//android.widget.TextView)[2]",
            locator_by=MobileBy.XPATH)

    def get_user_data(self) -> Dict[str, str]:
        user_data = dict()
        user_name = self.user_name_text.text.split()
        user_data['first_name'] = user_name[0]
        try:
            user_data['last_name'] = user_name[1]
        except KeyError:
            user_data['last_name'] = str()
        try:
            user_data['email'] = self.email_text.text
        except NoSuchElementException:
            user_data['email'] = str()
        try:
            user_data['location'] = self.location_text.text
        except NoSuchElementException:
            user_data['location'] = str()
        return user_data


class SearchInput(BaseInput):
    def __init__(self, driver: Remote):
        super(SearchInput, self).__init__(driver=driver, locator_value='com.truecaller:id/search_field')
        self.camera_pop_up = BaseButton(driver=self.driver,
                                        locator_value="//*[contains(@text,'Point your camera at any phone')]",
                                        locator_by=MobileBy.XPATH)

    def set_value(self, value: str) -> None:
        if self.camera_pop_up.is_visible():
            try:
                action = TouchAction(self.driver)
                action.tap(None, 241, 720).perform()
            except InvalidElementStateException:
                pass
        super(SearchInput, self).set_value(value=value)


class SearchView(BaseView):
    def __init__(self, driver: Remote):
        super(SearchView, self).__init__(driver)
        self.search_input = SearchInput(driver=self.driver)

    def click_first_result(self) -> UserInfoView:
        time.sleep(3)
        element = BaseButton(driver=self.driver,
                             locator_value='//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]',
                             locator_by=MobileBy.XPATH)
        element.click()
        return UserInfoView(self.driver)
