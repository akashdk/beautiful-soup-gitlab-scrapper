import requests
import getpass
import datetime
from datetime import timedelta


from lxml import html


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)



BASE_URL = "https://gitlab_url"
LOGIN_URL = BASE_URL + "/users/sign_in"


def main(*args):
    session_requests = requests.session()
    print("Email")
    email = input()
    print("your username")
    user_id = input()
    password = getpass.getpass()
    CALENDER_URL = BASE_URL + "/users/"+ user_id +"/calendar.json"
    today = datetime.datetime.today()
    yesterday = today - timedelta(days=1)
    today = today.strftime("%Y-%m-%d")
    yesterday = yesterday.strftime("%Y-%m-%d")
    result = session_requests.get(LOGIN_URL, verify=False)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath('//*[@name="authenticity_token"]//@value')))[0]
    payload = {
    "user[login]": email,
    "user[password]": password,
    "authenticity_token": authenticity_token
    }
    logged_ = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL), verify=False)
    calender = session_requests.get(CALENDER_URL, headers = dict(referer = CALENDER_URL), verify=False).json()
    print("Yesterday commits --> ", calender.get(yesterday,"No Records :-/"))
    print("Today commits --> ", calender.get(today,"No Records :-/"))
    print("Total commits --> ",sum(calender.values()))


if __name__ == '__main__':
    main()