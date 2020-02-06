## Test Task
This repository contains my solution to the Truecaller test task

### Required installations
* Download and install Android SDK: https://developer.android.com/studio/
* Download, install and run Appium: http://appium.io/
* Having Python3 installed with pip clone the repo and navigate to the root directory.
Install requirements: pip3 install requirements.txt
* Install Truecaller app on a real Android device: https://play.google.com/store/apps/details?id=com.truecaller&hl=en

### How to run it
* Connect your real Android device with PC via cable and enable USB debugging. Make sure WiFi or mobile data is turned on.
Do NOT run the script on your real device if you are already using Truecaller app! All application data will be deleted before the run
* Open command line and run truecaller.py file with a phone number as an argument
```python3 <path/to/the/file/truecaller.py> +1234567890```

Result file example:

```json
{
    "first_name": "Test",
    "last_name": "Name",
    "email": "test@email.com",
    "location": "Ukraine"
}
```