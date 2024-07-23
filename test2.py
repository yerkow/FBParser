import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from gologin import getRandomPort


gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjllOWZmM2MzNjc2YjZkNWIzYmU5NTAiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjllYTA4ODExNmUzNDMxNzcxMWE0ZGYifQ.gnu-Qmsxzo2ZKvbRi93AcyhRKInr4B7Jt9OS9EmwLRs",
	"profile_id": "669ea07b1f41219bb9aaa139",
	"tmpdir": '/home/yekinsgn/tmp'
	})

if platform == "linux" or platform == "linux2":
	chrome_driver_path = "./chromedriver"
elif platform == "darwin":
	chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
	chrome_driver_path = "chromedriver.exe"

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://www.python.org")
assert "Python" in driver.title
time.sleep(3)
driver.quit()
time.sleep(3)
gl.stop()