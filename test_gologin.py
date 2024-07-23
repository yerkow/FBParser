import requests

FILES_GATEWAY = 'https://files-gateway.gologin.com'
API_URL = 'https://api.gologin.com'
data = ''
access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjllOWZmM2MzNjc2YjZkNWIzYmU5NTAiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjllYTA4ODExNmUzNDMxNzcxMWE0ZGYifQ.gnu-Qmsxzo2ZKvbRi93AcyhRKInr4B7Jt9OS9EmwLRs'
profile_id = '669ea07d251669cb3a6e309e'
profile_zip_path = '/home/yekinsgn/tmp/test.zip'
headers = {
    'Authorization': 'Bearer ' + access_token,
    'User-Agent': 'Selenium-API',
    'browserId': profile_id
}
print(access_token, profile_id)
data = requests.get((FILES_GATEWAY + '/download'), headers=headers).content
with open(profile_zip_path, 'wb') as f:
    f.write(data)
