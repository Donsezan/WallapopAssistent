import requests
import random

DEVICE_ID = None  # Example device ID, replace with actual if needed
XWallapopSearchId = None

# Define the most comprehensive header set (original list from the issue)
# These headers were observed from a browser session.
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "Cache-Control": "no-cache",
    "Deviceos": "2", # As per original issue
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "X-Appversion": "7.10.0", # As per original issue
    "X-Deviceid": "3c583dea-106c-45f5-af7e-15510cf79269", # As per original issue
    "X-Devicemodel": "sdk_gphone64_x86_64", # As per original issue
    "X-Deviceosversion": "33", # As per original issue
    "X-Platform": "2", # As per original issue
    "Origin": "https://es.wallapop.com", # Added during iterative testing, good to keep
    "Referer": "https://es.wallapop.com/", # Added during iterative testing, good to keep
}

def Session_request():
    options_url = "https://es.wallapop.com/api/auth/session"
    _header = {
    ":authority": "es.wallapop.com",
    ":method": "GET",
    ":path": "/api/auth/session",
    ":scheme": "https",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en",    
    "Baggage": "sentry-environment=prod,sentry-release=8.672.0,sentry-public_key=c659be310b054ef5a765af65f8d56540,sentry-trace_id=0aa600bb7cb54ab6b8baadd68d1ac923,sentry-sample_rate=0,sentry-transaction=%2Fsearch,sentry-sampled=false",
    "Content-Type": "application/json",
    "Cookie":f"device_id={DEVICE_ID}; wallapop_keep_session=true",
    "Dnt": "1",
    "Priority": "u=1, i",
    "Referer": "https://es.wallapop.com/search?source=search_box&keywords=bose",
    "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sentry-Trace": "0aa600bb7cb54ab6b8baadd68d1ac923-93193ca414884e9f-0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        print("Allowed Methods:", response.headers.get('Allow', 'No Allow Header'))
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}")

def OptionsRequest_1():
    options_url = "https://api.wallapop.com/api/v3/searchalerts/savedsearch/exists?source=search_box&keywords=bose"
    _header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Access-Control-Request-Headers": "deviceos,x-appversion,x-deviceid,x-deviceos",
        "Access-Control-Request-Method": "HEAD",
        "Connection": "keep-alive",
        "Host": "api.wallapop.com",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    try:
        response = requests.options(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        print("Allowed Methods:", response.headers.get('Allow', 'No Allow Header'))
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}")    

def OptionsRequest_2():
    options_url = "https://api.wallapop.com/api/v3/search?source=search_box&keywords=bose"
    _header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Access-Control-Request-Headers": "deviceos,x-appversion,x-deviceid,x-deviceos",
        "Access-Control-Request-Method": "GET",
        "Connection": "keep-alive",
        "Host": "api.wallapop.com",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    try:
        response = requests.options(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        print("Allowed Methods:", response.headers.get('Allow', 'No Allow Header'))
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}")    

def FeatureFlags_request_3():
    options_url = "https://feature-flag.wallapop.com/api/v3/featureflag?featureFlags=webx_disable_opening_braze_session"
    _header = {
    "Accept": "application/vnd.featureflag-v2+json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en",
    "Cache-Control": "no-store",
    "Connection": "keep-alive",
    "Deviceos": "0",    
    "Dnt": "1",
    "Host": "feature-flag.wallapop.com",
    "Origin": "https://es.wallapop.com",
    "Pragma": "no-cache",
    "Referer": "https://es.wallapop.com/",
    "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "X-Appversion": "86720",
    "X-Deviceid": DEVICE_ID,
    "X-Deviceos": "0",
    "X-Semanticversion": "8.672."

    }
    try:
        response = requests.get(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        print("Allowed Methods:", response.headers.get('Allow', 'No Allow Header'))
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}") 

def Search_option_reqest_4():
    options_url = "https://api.wallapop.com/api/v3/search/filters/regular-filters?source=search_box&keywords=bose"
    _header = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en",
        "Access-Control-Request-Headers": "deviceos,x-appversion,x-deviceid,x-deviceos",
        "Access-Control-Request-Method": "GET",
        "Connection": "keep-alive",
        "Host": "api.wallapop.com",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    try:
        response = requests.options(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        print("Allowed Methods:", response.headers.get('Allow', 'No Allow Header'))
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}")    

def Search_alerts_request():
    options_url = "https://api.wallapop.com/api/v3/searchalerts/savedsearch/exists?source=search_box&keywords=bose"
    _header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es,en;q=0.9",
        "Connection": "keep-alive",
        "Deviceos": "0",
        "Dnt": "1",
        "Host": "api.wallapop.com",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
        "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "X-Appversion": "86720",
        "X-Deviceid": DEVICE_ID, #ToDo findout if this is needed
        "X-Deviceos": "0"
    }
    try:
        response = requests.head(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        print("Allowed Methods:", response.headers.get('Allow', 'No Allow Header'))
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}")    

def Search_request():
    options_url = "https://api.wallapop.com/api/v3/search?source=search_box&keywords=bose"
    _header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es,en;q=0.9",
        "Connection": "keep-alive",
        "Deviceos": "0",
        "Dnt": "1",
        "Host": "api.wallapop.com",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
        "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "X-Appversion": "86720",
        "X-Deviceid": DEVICE_ID, #ToDo findout if this is needed
        "X-Deviceos": "0"
    }
    try:
        response = requests.get(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        return response.json(), response.headers.get('X-Wallapop-Search-Id', None)
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}")    

def get_next_page_request(next_page_token, search_id):
    options_url = f"https://api.wallapop.com/api/v3/search?next_page={next_page_token}&source=deep_link&search_id={search_id}"
    _header = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es,en;q=0.9",
        "Connection": "keep-alive",
        "Deviceos": "0",
        "Dnt": "1",
        "Host": "api.wallapop.com",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
        "Sec-Ch-Ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "X-Appversion": "86720",
        "X-Deviceid": DEVICE_ID, #ToDo findout if this is needed
        "X-Deviceos": "0"
    }
    try:
        response = requests.get(options_url, headers=_header, timeout=10)
        print(f"OPTIONS Response Status Code: {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making OPTIONS request: {e}")    



def generate_random_hex_part():
    """
    Generates a random 4-character hexadecimal string.
    Equivalent to the JS function `generateRandomHexPart`.
    """
    return hex(int(65536 * (1 + random.random())))[2:].zfill(5)[1:]

def generate_application_device_id():
    return (
        generate_random_hex_part() + generate_random_hex_part() + "-" +
        generate_random_hex_part() + "-" +
        generate_random_hex_part() + "-" +
        generate_random_hex_part() + "-" +
        generate_random_hex_part() + generate_random_hex_part() + generate_random_hex_part()
    )



def main():  
    DEVICE_ID = generate_application_device_id()  # Generate a new device ID for each run.
    print("Generated Device ID:", DEVICE_ID)
    #session_request = Session_request()
    #option_1 = OptionsRequest_1()
    #option_2 = OptionsRequest_2()
    #featureFlags_request_3 = FeatureFlags_request_3()
   
    #search_option_reqest_4=  Search_option_reqest_4()
    #search_alerts_request = Search_alerts_request()
    #XWallapopSearchId
    search_request, xWallapopSearchId = Search_request()  # type: ignore
    XWallapopSearchId = xWallapopSearchId 
    next_page = get_next_page_request(search_request.get('meta', '').get('next_page', ''),XWallapopSearchId) # type: ignore
    
    print("\n--- Script Execution Finished ---")
    print("As noted in the comments, a 403 Forbidden error is the expected outcome from this environment based on previous tests.")

if __name__ == "__main__":
    main()

    