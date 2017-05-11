import requests
import browser_cookie3

# TODO: Get user path
cj = browser_cookie3.chrome('/home/evert.config/chromium/Default/Cookies')

s_session_id = ''

for cookie in cj:
    if cookie.domain == 'clickup.up.ac.za' and cookie.name == 's_session_id':
        s_session_id = cookie.value

print(s_session_id)

headers = {'Cookie': 's_session_id=' + s_session_id, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

r = requests.get("https://clickup.up.ac.za/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1", headers=headers);

# TODO: Check if cookie is good

print(r.text)
