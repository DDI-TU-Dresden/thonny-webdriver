# Webdriver Plugin for the thonny IDE

## Warning

The browser Chromium is not supported. Advanced security features can only be set on Firefox.

## Installation

- Install a browser and webdriver which is supported by Selenium. You can get a list of supported software [here](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/browsers/).

- Install the python dependencies

```bash
pip install -r requirements.txt --user
```

## Start the plugin with thonny

```bash
cd /path/to/thonny/
PYTHONPATH=/path/to/thonny-webdriver/ python -m thonny
```

## Usage in thonny

Click on the "Tools" section in the menu at the top of the program. And then select "Open Website". You will be asked to input a website. A new browser window will open with the desired website.