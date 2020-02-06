import sys

import json

from driver_setup import setup_driver
from views import StartView, CreateProfileView, CallsView, SearchView


def get_truecaller_user_data(phone_number: str):
    driver = setup_driver()
    start_view = StartView(driver)
    start_view.get_started_button.click()
    start_view.allow_permissions()
    if start_view.number_button.is_visible():
        start_view.number_button.click()
    start_view.agree_button.click()
    create_profile_view = CreateProfileView(driver)
    create_profile_view.fill_profile()
    calls_view = CallsView(driver)
    calls_view.truecaller_logo.click()
    search_view = SearchView(driver)
    search_view.search_input.set_value(phone_number)
    info_view = search_view.click_first_result()
    user_data = info_view.get_user_data()
    with open('output/user_data.json', 'w', encoding='utf-8') as f:
        json.dump(user_data, f, indent=4)
    driver.quit()


if __name__ == "__main__":
    get_truecaller_user_data(sys.argv[1])
