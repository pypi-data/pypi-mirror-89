import platform
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from pyvirtualdisplay import Display
from webdriverdownloader import ChromeDriverDownloader, GeckoDriverDownloader, OperaChromiumDriverDownloader


def platform_driver(webdriver_path, headless=True):
    if platform.system() == 'Linux':
        if "chromedriver" in webdriver_path:
            display = Display(visible=0, size=(800, 600))
            display.start()
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
        elif "geckodriver" in webdriver_path:
            display = Display(visible=0, size=(800, 600))
            display.start()
            options = webdriver.FirefoxOptions()
            options.add_argument('--no-sandbox')
            driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
    if platform.system() == 'Darwin':
        if "chromedriver" in webdriver_path:
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
        elif "geckodriver" in webdriver_path:
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(executable_path=webdriver_path, options=options)
        elif "operadriver" in webdriver_path:
            options = OperaOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Opera(executable_path=webdriver_path, options=options)
    return driver


def cicle_browser(count, path_to_driver):
    if count == 1:
        driver = webdriver.Firefox(executable_path=path_to_driver)
    elif count == 2:
        driver = webdriver.Chrome(executable_path=path_to_driver)
    elif count == 3:
        driver = webdriver.Safari(executable_path=path_to_driver)
    else:
        driver = webdriver.Edge(executable_path=path_to_driver)
    return driver


def switch_to(name, path_to_driver, headless=False):
    if name == 'Firefox':
        driver = webdriver.Firefox(executable_path=path_to_driver)
    elif name == 'Chrome':
        driver = webdriver.Chrome(executable_path=path_to_driver)
    elif name == 'Safari':
        driver = webdriver.Safari(executable_path=path_to_driver)
    elif name == 'Edge':
        driver = webdriver.Edge(executable_path=path_to_driver)
    return driver
