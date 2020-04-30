import requests
from bs4 import BeautifulSoup

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

def search_scammerInfo(dork):
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

    query = dork
    query = query.replace(' ', '+')
    URL = f"https://scammer.info/?q={query}"

    headers = {"user-agent": USER_AGENT}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for div in soup.find_all('div', class_='DiscussionListItem'):
            results.append(div)
        #print("[INFO][GOOGLE][>] ")
        print(results)
    
    elif resp.status_code == 429: 
        print("[INFO][GOOGLE][>] Too Many Requests response status code: the user has sent too many requests in a given amount of time.")

search_scammerInfo("658")