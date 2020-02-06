from appium.webdriver import Remote


def setup_driver():
    capabilities = dict()
    capabilities['deviceName'] = 'nexus_6'
    capabilities['platformName'] = 'Android'
    capabilities['appiumVersion'] = '1.15.1'
    capabilities['platformVersion'] = '9.0'
    capabilities['newCommandTimeout'] = 600
    capabilities['automationName'] = 'UiAutomator2'
    capabilities['noReset'] = False
    capabilities['appPackage'] = 'com.truecaller'
    capabilities['appActivity'] = 'com.truecaller.ui.TruecallerInit'
    capabilities['appWaitActivity'] = 'com.truecaller.ui.*'
    driver = Remote('http://localhost:4723/wd/hub', capabilities)
    driver.reset()
    driver.start_activity(capabilities['appPackage'], capabilities['appActivity'],
                          app_wait_activity=capabilities['appWaitActivity'])
    return driver
