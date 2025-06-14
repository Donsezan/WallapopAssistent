import requests
from datetime import datetime
from constants import Constants

class APIConnectionError(Exception):
    """Custom exception for API connection errors."""
    pass

class GraberServices:
    def __init__(self):
            self.searchPath = Constants.Direct_search_path
            self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'DeviceOS': '0',
            'Host': 'api.wallapop.com',
            'MPID': '-3950720573702771896',
            'Origin': 'https://es.wallapop.com',
            'Pragma': 'no-cache',
            'Referer': 'https://es.wallapop.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-AppVersion': '78401',
            'X-DeviceID': '31763af9-44cc-4268-9cb8-c40fbed4625a',
            'X-DeviceOS': '0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            }
            self.parameters = {
                # 'user_province': 'Madrid',
                # 'internal_search_id': 'a16035f8-fb4b-4967-9676-e9baaa2a0a48',
                'latitude': '36.6563536',
                'start': '0',
                'user_region': 'Comunidad de Madrid',
                # 'user_city': 'Poligono Industrial Aimayr',
                # 'search_id': '5ce64549-e8d1-4275-9f7a-4eb79fbae9f4',
                'country_code': 'ES',
                'user_postal_code': '29004',
                'items_count': '40',
                'filters_source': 'quick_filters',
                # 'pagination_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'order_by': 'newest',
                'step': '0',
                # 'category_ids': '15000',
                'longitude': '-3.646063',
            }              
    def SetParam(self, start_value):    
        val = {
            'start': str(start_value)            
        }   
        return self.parameters.update(val)
    
    def SetParam_for_direct(self, value, step, start_items_count, end_items_count):    
        val = {           
            'start': str(start_items_count),
            'keywords': str(value),
            'step': str(step),
            'items_count': str(end_items_count),
        }   
        return self.parameters.update(val)

    
    def  GetReposne(self, request_param):  
        if request_param is None:
             request_param = self.parameters
        # response = requests.get(self.searchPath, headers=self.headers, params=request_param) # Duplicated line removed
        try:
            response = requests.get(self.searchPath, headers=self.headers, params=request_param)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code      
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(f"API connection error: {e}")
        except requests.exceptions.HTTPError as e:
            raise APIConnectionError(f"API request failed with status {e.response.status_code}: {e}")
        
        return response.json()

    def ParseResults(self, resonse, target_list):
        products = resonse['search_objects']       
        results = []
        if target_list is not None and len(target_list) != 0:
            for product in products:
                title = product['title']
                for keyword in target_list:
                    if keyword in title:
                        print(f"The title contains '{keyword}'.")
                        results.append(product)
        else:
            results = products
        print ("Proccesed records: ", len(products))
        print ("Results records: ", len(results))
        return results 