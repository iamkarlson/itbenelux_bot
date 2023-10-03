import requests
import re

URL = "https://news.ycombinator.com/"


def get_resp(url):
    resp = requests.get(url)
    return resp.text


def parse_resp(resp):
    """
    <a href="http://behindthepixels.io/IMGUI/" class="storylink">Immediate Mode GUI</a>
    """
    re_a = re.compile(
        r'<a href="(https?://.*)" class="storylink">(.*?)</a>', re.IGNORECASE)

    m = re_a.search(resp)
    url = m.group(1)
    text = m.group(2)
    return url, text


def get_top():
    print("getting top from hn")
    resp = get_resp(URL)
    # print(resp)
    url, text = parse_resp(resp)
    print("url: %s" % (url))
    print("text: %s" % (text))
    return url, text
