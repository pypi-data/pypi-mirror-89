from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep

# Start and login
def newInstance(headless=True):
	"""Create a new instance of Firefox, with a headless option (true by default)"""
	if headless == True:
		opts = Options()
		opts.headless = True
		assert opts.headless
	else:
		opts = Options()

	browser = Firefox(options=opts)
	return browser

def login(browser, password, url="http://192.168.1.1/", delay=10):
	"""Login into the modem's web interface. You can find the default password on the back of your modem."""
	browser.get(url)

	passwordField = browser.find_element_by_id("pwd")
	passwordField.send_keys(password)

	loginButton = browser.find_element_by_id("login_proximus")
	loginButton.click()
	sleep(delay)

# generic functions
def cancel(browser):
	"""Only for scripting. It dismiss a menu."""
	closeButton = browser.find_element_by_id("Cancel")
	closeButton.click()

def apply(browser):
	"""Only for scripting. It apply changes in a menu."""
	applyButton = browser.find_element_by_id("Apply")
	applyButton.click()

def modemNavigation(browser, delay=3):
	"""Only for scripting. It opens the modem's menu"""
	modem = browser.find_element_by_id("Home_Modem_Navigation")
	modem.click()
	sleep(3)

def click(browser, element):
	"""Only for scripting. When 'element.click()' doesn't work because it's not loaded, use this one."""
	browser.execute_script("arguments[0].click();", element)

# Specified functions
def toggleWifi(browser, delay=7, wifi2=True, wifi5=True):
	"""Toggle the wifi (wireless).
	if 'wifi2' is set to True, it means the Wifi-2.4GHz is going to be switched.
	if 'wifi5' is set to True, it means the Wifi-5.0GHz is going to be switched.
	"""
	# Wifi 2.4GHz
	if wifi2 == True:
		menuButton1 = browser.find_element_by_id("Home_WiFi2.4GHz_Navigation")
		menuButton1.click()
		sleep(delay)

		switch = browser.find_element_by_id("Wifi2.4_switch")
		click(browser, switch)
		sleep(delay)

		apply(browser)
		sleep(delay)

	# Wifi 5GHz
	if wifi5 == True:
		menuButton2 = browser.find_element_by_id("Home_WiFi5GHz_Navigation")
		menuButton2.click()
		sleep(delay)

		switch = browser.find_element_by_id("Wifi5.0_switch")
		click(browser, switch)
		sleep(delay)

		apply(browser)
		sleep(delay)

def toggleHotspot(browser, delay=7):
	"""Toggle Proximus Hotspot on and off"""
	modemNavigation(browser)

	hotspot = browser.find_element_by_id("Modem_tab_Hotspot")
	hotspot.click()
	sleep(delay)

	toggle = browser.find_element_by_id("hotspot_switch_enable_disable")
	click(browser, toggle)

	apply(browser)
	sleep(delay)

def restartModem(browser, delay=7):
	"""Restart the modem,
	WARNING: It will disconnect everyone, even those who use ethernet."""
	modemNavigation(browser)

	maintenance = browser.find_element_by_id("Modem_tab_Maintenance")
	maintenance.click()
	sleep(delay)

	restart = browser.find_element_by_id("Modem_Maintenance_Restart")
	click(browser, restart)

	alert = browser.switch_to.alert
	alert.accept()
	sleep(delay)

def newPassword(b, oldPassword, newPassword, delay=5):
	"""Change the default user password"""
	username = b.find_element_by_id("Homepage_Username")
	username.click()

	settings = b.find_element_by_class_name("profile_set")
	settings.click()
	sleep(delay)

	oldField = b.find_element_by_id("U_PS_OldPwd")
	oldField.send_keys(oldPassword)

	newField = b.find_element_by_id("U_PS_NewPwd")
	newField.send_keys(newPassword)

	confirmField = b.find_element_by_id("U_PS_ConfirmPwd")
	confirmField.send_keys(newPassword)

	apply(b)
	sleep(delay)
