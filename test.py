import time
import asyncio
import pyppeteer
from sys import platform
from gologin import GoLogin

async def main():
	gl = GoLogin({
		"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjllOWZmM2MzNjc2YjZkNWIzYmU5NTAiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjllYTA4ODExNmUzNDMxNzcxMWE0ZGYifQ.gnu-Qmsxzo2ZKvbRi93AcyhRKInr4B7Jt9OS9EmwLRs",
		"profile_id": "669ea07b1f41219bb9aaa139",
		})

	debugger_address = gl.start()
	browser = await pyppeteer.connect(browserURL="http://"+debugger_address, defaultViewport=None)
	page = await browser.newPage()
	await gl.normalizePageView(page)
	await page.goto('https://gologin.com')
	await page.screenshot({'path': 'gologin.png'})
	await browser.close()
	gl.stop()

asyncio.get_event_loop().run_until_complete(main())