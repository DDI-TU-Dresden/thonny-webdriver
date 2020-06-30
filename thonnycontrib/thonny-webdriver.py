from selenium import webdriver
from thonny import get_workbench
from selenium.common import exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tkinter.simpledialog import askstring
from threading import Thread
import time


class Singleton:
    """This Singleton class is needed so you do not spawn more selenium contexts when
    opening a new link or working on a past context.

    __instance: The current instance of this class.
    closed: A variable that indicates if the current browser window has been closed by
    the user.
    sleeptime: The seconds to wait after every check if an HTML element has changed.
    observed_ids: The HTML element ids which are observed by the observe method.
        """

    __instance = None
    closed = False
    sleeptime = 2
    observed_ids = []

    @staticmethod
    def getInstance():
        """This is a modified Singleton.getInstance() method. It will create a new
        instance if the variable closed is set to true.

        Returns:
            Nested Singleton object with an initialized webdriver using a selenium
            context
        """
        if Singleton.__instance == None or Singleton.closed:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """This is a modified Singleton constructor. Just like Singleton.getInstance()
        it will create a new instance if the variable closed is set to true. Before
        creating the new context, security settings will also be set for Firefox. Other
        browsers only support the W3C compliant capabilities (
        https://www.w3.org/TR/webdriver/#capabilities).
        """
        if Singleton.__instance != None and Singleton.closed == False:
            raise Exception("This class is a singleton!")
        else:
            try:
                firefox_capabilities = DesiredCapabilities.FIREFOX
                # Only communicate over HTTPS and do not accept insecure Certificates
                firefox_capabilities["handleAlerts"] = False
                firefox_capabilities["acceptSslCerts"] = False
                firefox_capabilities["acceptInsecureCerts"] = False
                profile = webdriver.FirefoxProfile()
                profile.accept_untrusted_certs = False
                profile.set_preference("network.http.use-cache", False)
                profile.set_preference("dom.security.https_only_mode", True)
                # Disable unsafe cipher
                profile.set_preference("security.ssl3.rsa_des_ede3_sha", False)
                # Disable ciphers with no forward secrecy
                profile.set_preference("security.ssl3.dhe_rsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.dhe_rsa_aes_256_sha", False)
                profile.set_preference("security.ssl3.rsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.rsa_aes_256_sha", False)
                profile.set_preference("security.ssl3.ecdhe_ecdsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.ecdhe_ecdsa_aes_256_sha", False)
                profile.set_preference("security.ssl3.ecdhe_rsa_aes_128_sha", False)
                profile.set_preference("security.ssl3.ecdhe_rsa_aes_256_sha", False)
                self.driver = webdriver.Firefox(
                    capabilities=firefox_capabilities, firefox_profile=profile
                )
            except BaseException:
                try:
                    self.driver = webdriver.Chrome()
                except BaseException:
                    try:
                        self.driver = webdriver.Safari()
                    except BaseException:
                        try:
                            self.driver = webdriver.Edge()
                        except BaseException:
                            try:
                                self.driver = webdriver.Opera()
                            except BaseException:
                                try:
                                    self.driver = webdriver.Ie()
                                except Exception as e:
                                    print(str(e))
                                    print(
                                        "You seem to be using a browser and webdriver "
                                        + "which are not supported by selenium. You can "
                                        + "find the list of supported browsers here: "
                                        + "https://www.selenium.dev/documentation/en/"
                                        + "getting_started_with_webdriver/browsers/"
                                    )
            Singleton.closed = False
            Singleton.__instance = self

    def toggle_closed(self):
        """This method toggles the closed variable.

        Returns:
            None
        """
        Singleton.closed = not Singleton.closed

    def get_sleeptime(self):
        """This method gets the current sleep time. The time to wait after every check
        if an HTML element has changed.

        Returns:
            float in seconds
        """
        return Singleton.sleeptime

    def set_sleeptime(self, sleeptime):
        """This method sets the sleep time. The time to wait after every check if an
        HTML element has changed.

        :param sleeptime: Seconds to sleep represented as float

        Returns:
            None
        """
        Singleton.sleeptime = sleeptime

    def get_observed_ids(self):
        """Get the list of HTML element ids which are currently observed.

        Returns:
            list of HTML element ids
        """
        return Singleton.observed_ids

    def add_observed_id(self, html_id):
        """This method adds one HTML element id to the list of currently observed ids.

        :param html_id: HTML element id that you wish to add

        Returns:
            None
        """
        Singleton.observed_ids.append(html_id)

    def remove_observed_id(self, html_id):
        """This method removes one HTML element id to the list of currently observed
        ids.

        :param html_id: HTML element id that you wish to remove

        Returns:
            None
        """
        Singleton.observed_ids.remove(html_id)


def open_website():
    """This method gets called if the "Open Website" command is clicked in the "tools"
    menu. It will get the Singleton instance and then tries to open the desired
    website. Insecure Certificates will be shown as an error page to the user. If the
    browser window has been closed by the user, a new selenium context will be created.

        Returns:
            None
        """
    singleton = Singleton.getInstance()
    # This is the URL for struktog only available in the campus VPN
    address = "http://172.26.62.121"
    try:
        singleton.driver.get(address)
    except exceptions.InsecureCertificateException:
        return
    except exceptions.WebDriverException:
        singleton.toggle_closed()
        singleton = Singleton.getInstance()
        singleton.driver.get(address)
    # This simulates a click on the ToggleSourcecode element, to show the select element to choose a programming language
    singleton.driver.execute_script('document.getElementsByClassName("ToggleSourcecode")[0].click()')
    # This also simulates a click on the correct option but the code is different as the .click() function does not work for this: https://stackoverflow.com/questions/49886729/simulate-a-human-click-and-select-on-dropdown-menu
    singleton.driver.execute_script('var optionToClick = document.getElementById("SourcecodeSelect").childNodes[1]; optionToClick.selected = true; optionToClick.dispatchEvent(new PointerEvent("pointerdown", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("mousedown", {bubbles: true})); optionToClick.dispatchEvent(new PointerEvent("pointerup", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("mouseup", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("mouseout", {bubbles: true})); optionToClick.dispatchEvent(new MouseEvent("click", {bubbles: true})); optionToClick.dispatchEvent(new Event("change", {bubbles: true}));')



def observe_element_in_background():
    """This method gets called by the start_observing_element_by_id method. If the text
    of the HTML element changes, the info will be printed to stdout.

        Returns:
            None
        """
    singleton = Singleton.getInstance()
    driver = singleton.driver
    url = driver.current_url
    observed_ids = singleton.get_observed_ids()
    list_id = len(observed_ids) - 1
    html_id = observed_ids[list_id]
    observed_text = driver.find_element_by_id(html_id).text
    # Get the current opened code view
    code_view = get_workbench().get_editor_notebook().get_current_editor().get_code_view()
    # Change the content to the observed text
    code_view.set_content(observed_text)
    print("Start observing on the following URL: " + url)
    print("And the following ID: " + html_id)
    while html_id in singleton.get_observed_ids():
        try:
            element = driver.find_element_by_id(html_id)
            if element.text != observed_text:
                print("Text of " + html_id + " changed to: " + element.text)
                observed_text = element.text
                # Change the content to the observed text every time a change is detected
                code_view.set_content(observed_text)
        except exceptions.NoSuchElementException as e:
            print(e)
            print("Observing this element is not possible as it does not exist.")
            return
        except exceptions.WebDriverException as e:
            print(
                "The Browser window was closed. Observing this element is not possible"
                + " anymore"
            )
            print(e)
            return
        time.sleep(singleton.get_sleeptime())
    print("Observing was stopped as requested.")


def start_observing_element_by_id():
    """This method gets called if the "Start observing element by id" command is
    clicked in the "tools" menu. It will prompt the user to provide an HTML ID which
    will be added to the list of observed elements. After that, a new thread will be
    created to observe this HTML ID.

        Returns:
            None
        """
    observe_id = "Sourcecode"
    singleton = Singleton.getInstance()
    singleton.add_observed_id(observe_id)
    t = Thread(target=observe_element_in_background)
    t.daemon = True
    t.start()


def stop_observing_element_by_id():
    """This method gets called if the "Stop observing element by id" command is clicked
    in the "tools" menu. It will prompt the user to provide an HTML ID which will be removed
    from the list of observed elements.

        Returns:
            None
        """
    observe_id = "Sourcecode"
    singleton = Singleton.getInstance()
    singleton.remove_observed_id(observe_id)


def load_plugin():
    """This method gets called if this plugin is in the PYTHONPATH environment variable
       upon starting thonny. This code is executed before TK windows are drawn. That is
       why you should use add a command to the thonny GUI before running anything.

        Returns:
            None
        """
    get_workbench().add_command(
        command_id="webview_open_website",
        menu_name="tools",
        command_label="Open website",
        handler=open_website,
    )
    get_workbench().add_command(
        command_id="webview_observing_add",
        menu_name="tools",
        command_label="Start observing element by id",
        handler=start_observing_element_by_id,
    )
    get_workbench().add_command(
        command_id="webview_observing_delete",
        menu_name="tools",
        command_label="Stop observing element by id",
        handler=stop_observing_element_by_id,
    )
