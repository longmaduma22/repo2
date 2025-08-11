import cloudscraper
from bs4 import BeautifulSoup
import sys
import re
import base64
import uuid
from datetime import datetime
from time import sleep
from colorama import Fore, init
import json
import requests

init(autoreset=True)

red = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
cam = "\033[38;5;208m"
tim = "\033[1;35m"
lam = "\033[1;36m"
trang = "\033[1;37m"

def banner():
    print(f"""{Fore.YELLOW}╔══════════════════════════════════════════════════════╗
{Fore.YELLOW}║                                                      {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}████████╗██╗  ██╗ ████████╗ █████╗  █████╗ ██╗      {Fore.YELLOW}║
{Fore.YELLOW}║  {Fore.WHITE}╚══██╔══╝██║  ██║ ╚══██╔══╝██╔══██╗██╔══██╗██║      {Fore.YELLOW}║
{Fore.YELLOW}║     {Fore.WHITE}██║   ███████║    ██║   ██║  ██║██║  ██║██║      {Fore.YELLOW}║
{Fore.YELLOW}║     {Fore.WHITE}██║   ██╔══██║    ██║   ██║  ██║██║  ██║██║      {Fore.YELLOW}║
{Fore.YELLOW}║     {Fore.WHITE}██║   ██║  ██║    ██║   ╚█████╔╝╚█████╔╝███████╗ {Fore.YELLOW}║
{Fore.YELLOW}║     {Fore.WHITE}╚═╝   ╚═╝  ╚═╝    ╚═╝    ╚════╝  ╚════╝ ╚══════╝ {Fore.YELLOW}║
{Fore.YELLOW}║                                                      ║
{Fore.YELLOW}║      \033[1;36mAdmin: Thiệu Hoàng | YouTube: @thieuhoang75     {Fore.YELLOW}║
{Fore.YELLOW}║              {Fore.YELLOW}Ngày: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}               {Fore.YELLOW}║
{Fore.YELLOW}╚══════════════════════════════════════════════════════╝
""")

def extract_post_id(input_url):
    patterns = [
        r'/posts/(pfbid\w+)',  
        r'/posts/(\d+)',      
        r'/(\d+)(?:/|\?|$)',  
        r'/pfbid(\w+)'        
    ]
    for pattern in patterns:
        match = re.search(pattern, input_url)
        if match:
            return match.group(1)
    return None

def get_canonical_post_url(input_url, cookie=None):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    headers = {}
    cookies = {}
    if cookie:
        cookies = {"cookie": cookie}
        headers["cookie"] = cookie
    try:
        response = scraper.get(input_url, cookies=cookies, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching the URL: {e}")
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_og_url = soup.find('meta', property='og:url')
    canonical_url = meta_og_url['content'] if meta_og_url and meta_og_url.get('content') else input_url
    post_id = extract_post_id(canonical_url)
    if post_id:
        return post_id
    else:
        print("Could not extract post ID.")
        sys.exit(1)

def decode_base64(encoded_str):
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

def _encode_to_base64(_data):
    byte_representation = _data.encode('utf-8')
    base64_bytes = base64.b64encode(byte_representation)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def _Infofb(cookie):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    heads={
        "accept": "*/*",
        "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7", 
        "content-type": "application/x-www-form-urlencoded", 
        "sec-ch-prefers-color-scheme": "light", 
        "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"", 
        "sec-ch-ua-full-version-list": "\"Not-A.Brand\";v=\"99.0.0.0\", \"Chromium\";v=\"124.0.6327.4\"", 
        "sec-ch-ua-mobile": "?0", 
        "sec-ch-ua-model": "\"\"", 
        "sec-ch-ua-platform": "\"Linux\"", 
        "sec-ch-ua-platform-version": "\"\"", 
        "sec-fetch-dest": "empty", 
        "sec-fetch-mode": "cors", 
        "sec-fetch-site": "same-origin", 
        "x-asbd-id": "129477", 
        "x-fb-friendly-name": "ProfileCometTimelineListViewRootQuery", 
        "x-fb-lsd": "7_RkODA0fo-6ShZlbFpHEW"
    }
    get = scraper.get("https://www.facebook.com/me", headers=heads, cookies={"cookie": cookie})
    try:
        get = get.url
        get_text = scraper.get(get, headers=heads, cookies={"cookie": cookie}).text
        _sea = get_text.split(',"NAME":"')[1].split('",')[0]
        _name = bytes(_sea, "utf-8").decode("unicode_escape")
        _fb1 = get_text.split('["DTSGInitialData",[],{"token":"')[1].split('"')[0]
        _lsd = get_text.split('["LSD",[],{"token":"')[1].split('"')[0]
        _idfb = cookie.split('c_user=')[1].split(';')[0]
        return [_fb1, _idfb, _name, _lsd]
    except Exception as e:
        print(f"Lỗi khi lấy thông tin: {e}")
        return False

def get_access_token(cookie):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Cookie': cookie
    }
    try:
        response = scraper.get('https://business.facebook.com/business_locations', headers=headers)
        token = re.search('(EAAG\w+)', response.text).group(1)
        return token
    except:
        return None

def _Like(cookie, uid, type, fb1, idfb, lsd):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    headers = {
        "accept": "*/*", 
        "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7", 
        "content-type": "application/x-www-form-urlencoded", 
        "sec-ch-prefers-color-scheme": "light", 
        "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"", 
        "sec-ch-ua-full-version-list": "\"Not-A.Brand\";v=\"99.0.0.0\", \"Chromium\";v=\"124.0.6327.4\"", 
        "sec-ch-ua-mobile": "?0", 
        "sec-ch-ua-model": "\"\"", 
        "sec-ch-ua-platform": "\"Linux\"", 
        "sec-ch-ua-platform-version": "\"\"", 
        "sec-fetch-dest": "empty", 
        "sec-fetch-mode": "cors", 
        "sec-fetch-site": "same-origin", 
        "x-asbd-id": "129477", 
        "x-fb-friendly-name": "CometUFIFeedbackReactMutation", 
        "x-fb-lsd": lsd
    }
    _reac = {
        "LIKE": "1635855486666999",
        "LOVE": "1678524932434102",
        "CARE": "613557422527858",
        "HAHA": "115940658764963",
        "WOW": "478547315650144",
        "SAD": "908563459236466",
        "ANGRY": "444813342392137"
    }
    _id_reac = _reac.get(type)
    jazoest = sum(ord(c) for c in fb1)
    _data = {
        'av': idfb,
        '__usid': str(uuid.uuid4()),
        '__aaid': '0',
        '__user': idfb,
        '__a': '1',
        '__req': '2c',
        '__hs': '19896.HYP:comet_pkg.2.1..2.1',
        'dpr': '1',
        '__ccg': 'EXCELLENT',
        '__rev': '1014402108',
        '__s': '5vdtpn:wbz2hc:8r67q5',
        '__hsi': str(int(datetime.now().timestamp() * 1000)),
        '__dyn': '7AzHK4HwkEng5K8G6EjBAg5S3G2O5U4e2C17xt3odE98K361twYwJyE24wJwpUe8hwaG1sw9u0LVEtwMw65xO2OU7m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE567Udo5qfK0zEkxe2GewyDwkUe9obrwKxm5oe8464-5pUfEdK261eBx_wHwdG7FoarCwLyES0Io88cA0z8c84q58jyUaUcojxK2B08-269wkopg6C13whEeE4WVU-4EdrxG1fy8bUaU',
        '__csr': 'gug_2A4A8gkqTf2Ih6RFnbk9mBqaBaTs8_tntineDdSyWqiGRYCiPi_SJuLCGcHBaiQXtLpXsyjIymm8oFJswG8CSGGLzAq8AiWZ6VGDgyQiiTBKU-8GczE9USmi4A9DBABHgWEK3K9y9prxaEa9KqQV8qUlxW22u4EnznDxSewLxq3W2K16BxiE5VqwbW1dz8qwCwjoeEvwaKVU6q0yo5a2i58aE7W0CE5O0fdw1jim0dNw7ewPBG0688025ew0bki0cow3c8C05Vo0aNF40BU0rmU3LDwaO06hU06RG6U1g82Bw0Gxw6Gw',
        '__comet_req': '15',
        'fb_dtsg': fb1,
        'jazoest': '2' + str(jazoest),
        'lsd': lsd,
        '__spin_r': '1014402108',
        '__spin_b': 'trunk',
        '__spin_t': str(int(datetime.now().timestamp())),
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'CometUFIFeedbackReactMutation',
        'variables': json.dumps({
            "input": {
                "attribution_id_v2": "CometHomeRoot.react,comet.home,tap_tabbar,1719027162723,322693,4748854339,,",
                "feedback_id": _encode_to_base64("feedback:" + str(uid)),
                "feedback_reaction_id": _id_reac,
                "feedback_source": "NEWS_FEED",
                "is_tracking_encrypted": True,
                "tracking": [],
                "session_id": str(uuid.uuid4()),
                "actor_id": idfb,
                "client_mutation_id": str(uuid.uuid4())
            },
            "useDefaultActor": False,
            "__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider": False
        }),
        'server_timestamps': 'true',
        'doc_id': '7047198228715224',
    }
    cookies = {
        "cookie": cookie
    }
    _get = scraper.post("https://www.facebook.com/api/graphql/", headers=headers, cookies=cookies, data=_data)
    if 'feedback_react' in _get.text:
        return True
    else:
        return False

def CMT_graphql(cookie, id, idfb, fb1, msg, lsd, doc_id='7297709336999878'):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    })
    headers = {
        "accept": "*/*",
        "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded", 
        "sec-ch-prefers-color-scheme": "light", 
        "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"", 
        "sec-ch-ua-full-version-list": "\"Not-A.Brand\";v=\"99.0.0.0\", \"Chromium\";v=\"124.0.6327.4\"", 
        "sec-ch-ua-mobile": "?0", 
        "sec-ch-ua-model": "\"\"", 
        "sec-ch-ua-platform": "\"Linux\"", 
        "sec-ch-ua-platform-version": "\"\"", 
        "sec-fetch-dest": "empty", 
        "sec-fetch-mode": "cors", 
        "sec-fetch-site": "same-origin", 
        "x-asbd-id": "129477", 
        "x-fb-friendly-name": "useCometUFICreateCommentMutation", 
        "x-fb-lsd": lsd
    }
    jazoest = sum(ord(c) for c in fb1)
    _data = {
        'av': idfb,
        '__aaid': '0',
        '__user': idfb,
        '__a': '1',
        '__req': '3a',
        '__hs': '19906.HYP:comet_pkg.2.1..2.1',
        'dpr': '1',
        '__ccg': 'GOOD',
        '__rev': '1014619389',
        '__s': 'z5ciff:vre7af:23swxc',
        '__hsi': str(int(datetime.now().timestamp() * 1000)),
        '__dyn': '7AzHK4HwkEng5K8G6EjBAg2owIxu13wFwhUngS3q2ibwNw9G2Saw8i2S1DwUx60GE5O0BU2_CxS320om78c87m221Fwgo9oO0-E4a3a4oaEnxO0Bo7O2l2Utwqo31wiE567Udo5qfK0zEkxe2GewDG1jwUBwJK2W5olwUwgojUlDw-wUwxwjFovUaU3VBwFKq2-azo2NwwwOg2cwMwhEkxebwHwNxe6Uak0zU8oC1hxB0qo4e16wWwjHDzUiwRK6E4-8wLwHw',
        '__csr': 'gaRMHkaEj4EQgznFON5ifOjsLJA9idO8LqsAHJXeIX48l9lRN4kDmyTAvcKSIAGQtljy9kV4DlGaBAnWUCiqqWmWKA6pBBUymnHBArrCDDKaGaggAQubV8V34iVUCiicoC32Ujm8Ki8H-6UJ1h2KlAyECdg4237CxmQ6F89onXAwjEe8uwxxu5ES2G1qxy3K0xonx21ewnEb8eU2yG2q0hm1yw8G7o7G7oaodU1381T84m0auwdy0dDwb201Z4w2Fo036dg0gYCw2BA0wU7e04WU0qQwlodE04Dq01zOw4Bw51w7hxK',
        '__comet_req': '15',
        'fb_dtsg': fb1,
        'jazoest': '2' + str(jazoest),
        'lsd': lsd,
        '__spin_r': '1014619389',
        '__spin_b': 'trunk',
        '__spin_t': str(int(datetime.now().timestamp())),
        'fb_api_caller_class': 'RelayModern',
        'fb_api_req_friendly_name': 'useCometUFICreateCommentMutation',
        'variables': json.dumps({
            "feedLocation": "DEDICATED_COMMENTING_SURFACE",
            "feedbackSource": 0,
            "focusCommentID": None,
            "groupID": None,
            "input": {
                "client_mutation_id": str(uuid.uuid4()),
                "actor_id": idfb,
                "attachments": [],
                "feedback_id": _encode_to_base64("feedback:" + str(id)),
                "is_tracking_encrypted": True,
                "tracking": [],
                "text_and_ranges": [{"text": msg, "ranges": []}]
            },
            "scale": 1,
            "useDefaultActor": False,
            "__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider": False
        }),
        'server_timestamps': 'true',
        'doc_id': doc_id,
    }
    cookies = {
        "cookie": cookie
    }
    _post = scraper.post("https://www.facebook.com/api/graphql/", headers=headers, cookies=cookies, data=_data)
    if 'create_comment' in _post.text:
        return True
    else:
        return False

def CMT_public(cookie, post_id, msg):
    token = get_access_token(cookie)
    if not token:
        return False
    url = f"https://graph.facebook.com/v23.0/{post_id}/comments"
    params = {
        'message': msg,
        'access_token': token
    }
    response = requests.post(url, params=params)
    if response.status_code == 200 and 'id' in response.json():
        return True
    else:
        print(response.text)
        return False

def CMT_mbasic(cookie, post_id, msg, fb1):
    scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'android',
        'mobile': True
    })
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Cookie': cookie
    }
    url = 'https://mbasic.facebook.com/' + post_id
    response = scraper.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form', action=lambda x: x and 'comment.php' in x)
    if form:
        action = form['action']
        data = {
            'fb_dtsg': fb1,
            'comment_text': msg
        }
        inputs = form.find_all('input', type='hidden')
        for inp in inputs:
            if inp.get('name'):
                data[inp['name']] = inp['value']
        full_url = 'https://mbasic.facebook.com' + action
        post_resp = scraper.post(full_url, data=data, headers=headers)
        if post_resp.status_code == 200 or 'comment' in post_resp.text.lower():
            return True
    return False

def CMT(cookie, id, idfb, fb1, msg, lsd):
    # Method 1: mbasic comment (simulating mobile browser, similar to cheo method)
    if CMT_mbasic(cookie, id, msg, fb1):
        return True
    # Method 2: GraphQL with original doc_id
    if CMT_graphql(cookie, id, idfb, fb1, msg, lsd):
        return True
    # Method 3: Public Graph API
    if CMT_public(cookie, id, msg):
        return True
    return False

def main():
    banner()
    proxy = input(f"{lam}Nhập proxy (nếu có, ví dụ: http://user:pass@ip:port, bỏ trống nếu không): ")
    if proxy:
        print(f"{cam}Proxy được sử dụng: {proxy}")
    cookie = input(f"{lam}Nhập cookie Facebook: ")
    _info = _Infofb(cookie)
    if _info == False:
        print(f"{red}Cookie không hợp lệ hoặc tài khoản bị out!")
        sys.exit(1)
    fb1, idfb, name, lsd = _info
    print(f"{luc}Tài khoản: {name} | ID: {idfb} | LSD: {lsd}")
    url_post = input(f"{lam}Nhập URL post Facebook: ")
    post_id = get_canonical_post_url(url_post, cookie)
    print(f"{luc}Post ID: {post_id}")
    while True:
        job_type = input(f"{lam}Chọn loại job (1: Comment, 2: Like, 3: Cảm xúc, 0: Thoát): ")
        if job_type == '0':
            break
        elif job_type == '1':
            msg = input(f"{lam}Nhập nội dung comment: ")
            result = CMT(cookie, post_id, idfb, fb1, msg, lsd)
            if result:
                print(f"{luc}Comment thành công: {msg}")
            else:
                print(f"{red}Comment thất bại với tất cả các method!")
        elif job_type == '2':
            result = _Like(cookie, post_id, 'LIKE', fb1, idfb, lsd)
            if result:
                print(f"{luc}Like thành công!")
            else:
                print(f"{red}Like thất bại!")
        elif job_type == '3':
            print(f"{lam}Chọn cảm xúc: LIKE, LOVE, CARE, HAHA, WOW, SAD, ANGRY")
            emotion = input(f"{lam}Nhập loại cảm xúc: ").upper()
            if emotion in ['LIKE', 'LOVE', 'CARE', 'HAHA', 'WOW', 'SAD', 'ANGRY']:
                result = _Like(cookie, post_id, emotion, fb1, idfb, lsd)
                if result:
                    print(f"{luc}Cảm xúc {emotion} thành công!")
                else:
                    print(f"{red}Cảm xúc {emotion} thất bại!")
            else:
                print(f"{red}Cảm xúc không hợp lệ!")
        else:
            print(f"{red}Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
