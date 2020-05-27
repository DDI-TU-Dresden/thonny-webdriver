from selenium import webdriver
from thonny import get_workbench
from selenium.common import exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tkinter.simpledialog import askstring


class Singleton:
    """This Singleton class is needed so you do not spawn more selenium contexts when
    opening a new link or working on a past context.

    __instance: The current instance of this class.
    closed: A variable that indicates if the current browser window has been closed by
            the user.
        """

    __instance = None
    closed = False

    @staticmethod
    def getInstance():
        """This is a modified Singleton.getInstance() method. It will create a new
        instance if the variable closed is set to true.

        Returns:
            Singleton object with an initialized selenium context
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


def open_website():
    """This method gets called if the "Open Website" command is clicked in the "tools"
    menu. It will get the Singleton instance and then tries to open the desired
    website. Insecure Certificates will be shown as an error page to the user. If the
    browser window has been closed by the user, a new selenium context will be created.

        Returns:
            None
        """
    singleton = Singleton.getInstance()
    address = askstring("Website", "Which website would you like to visit?")
    try:
        singleton.driver.get(address)
    except exceptions.InsecureCertificateException:
        return
    except exceptions.WebDriverException:
        singleton.toggle_closed()
        singleton = Singleton.getInstance()
        singleton.driver.get(address)


def load_plugin():
    """This method gets called if this plugin is in the PYTHONPATH environment variable
       upon starting thonny. This code is executed before TK windows are drawn. That is
       why you should use add a command to the thonny GUI before running anything.

        Returns:
            None
        """
    get_workbench().add_command(
        command_id="webview",
        menu_name="tools",
        command_label="Open Website",
        handler=open_website,
    )
