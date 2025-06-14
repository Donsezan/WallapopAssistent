import requests
import random
from datetime import datetime
from constants import Constants

class APIConnectionError(Exception):
    """Custom exception for API connection errors."""
    pass

class GraberServices:
    @staticmethod
    def generate_random_hex_part():
        """
        Generates a random 4-character hexadecimal string.
        Equivalent to the JS function `generateRandomHexPart`.
        """
        return hex(int(65536 * (1 + random.random())))[2:].zfill(5)[1:]

    @staticmethod
    def generate_application_device_id():
        return (
            GraberServices.generate_random_hex_part() + GraberServices.generate_random_hex_part() + "-" +
            GraberServices.generate_random_hex_part() + "-" +
            GraberServices.generate_random_hex_part() + "-" +
            GraberServices.generate_random_hex_part() + "-" +
            GraberServices.generate_random_hex_part() + GraberServices.generate_random_hex_part() + GraberServices.generate_random_hex_part()
        )

    def __init__(self):
            self.device_id = GraberServices.generate_application_device_id()
            self.search_id = None # Initialize search_id
            self.searchPath = Constants.Direct_search_path # Retained for now, though new methods use specific URLs
            self.headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
                "Cache-Control": "no-cache",
                "Deviceos": "2",
                "Pragma": "no-cache",
                "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Linux"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "X-Appversion": "7.10.0",
                "X-Deviceid": self.device_id, # Using the generated device_id
                "X-Devicemodel": "sdk_gphone64_x86_64",
                "X-Deviceosversion": "33",
                "X-Platform": "2",
                "Origin": "https://es.wallapop.com",
                "Referer": "https://es.wallapop.com/",
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
                # 'category_ids': '15000', # Example: ensure this is in your self.parameters if used
            }              
    def SetParam(self, start_value):
        """
        DEPRECATED: This method is for an older search mechanism and is not used
        by the v3 search flow implemented via search_initial and fetch_next_page.
        The 'start' parameter is now handled by pagination tokens.
        """
        val = {
            'start': str(start_value)            
        }   
        return self.parameters.update(val)
    
    def SetParam_for_direct(self, value, step, start_items_count, end_items_count):
        """
        DEPRECATED: This method is for an older search mechanism.
        Keywords, pagination, and result counts are handled by
        get_all_results_for_keywords, search_initial, and fetch_next_page
        in the v3 search flow.
        """
        val = {           
            'start': str(start_items_count),
            'keywords': str(value),
            'step': str(step),
            'items_count': str(end_items_count),
        }   
        return self.parameters.update(val)

    
    def _make_api_request(self, url, params=None, headers=None):
        _headers = headers if headers is not None else self.headers
        # _params = params # Parameters will be passed directly to requests.get

        try:
            response = requests.get(url, headers=_headers, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
            return response  # Return the full response object
        except requests.exceptions.ConnectionError as e:
            raise APIConnectionError(f"API connection error: {e}")
        except requests.exceptions.HTTPError as e:
            # Log or handle HTTP errors specifically if needed
            raise APIConnectionError(f"API request failed with status {e.response.status_code}: {e}")
        except requests.exceptions.RequestException as e:
            # Catch any other request-related errors
            raise APIConnectionError(f"General API request error: {e}")

    def search_initial(self, keywords, **kwargs):
        url = "https://api.wallapop.com/api/v3/search"

        # Start with essential, non-overridable params
        params = {
            'source': 'search_box',
            'keywords': keywords,
        }

        # Define keys for default values to be pulled from self.parameters
        default_param_keys = [
            'latitude', 'longitude', 'country_code', 'user_region',
            'user_postal_code', 'order_by', 'category_ids',
            'items_count', 'filters_source'
        ]

        # Add defaults from self.parameters if not supplied directly in kwargs
        for key in default_param_keys:
            if key not in kwargs:  # Only consider if not explicitly passed by the caller
                value = self.parameters.get(key)
                if value is not None: # Only add if self.parameters has a non-None value for this key
                    params[key] = value

        # Apply any overrides or additional params from kwargs
        # This will overwrite defaults if keys are present in kwargs
        params.update(kwargs)

        # Final cleanup: Remove any keys where the value is None
        # This handles cases where kwargs might explicitly pass None for a parameter
        params = {k: v for k, v in params.items() if v is not None}

        raw_response = self._make_api_request(url, params=params)
        self.search_id = raw_response.headers.get('X-Wallapop-Search-Id')

        json_response = raw_response.json()
        next_page_token = json_response.get('meta', {}).get('next_page')

        return json_response, next_page_token

    def fetch_next_page(self, next_page_token):
        if not self.search_id:
            raise ValueError("search_id is not set. Call search_initial first.")
        if not next_page_token:
            # Consider if this should raise error or return empty/None
            return None, None

        url = f"https://api.wallapop.com/api/v3/search?next_page={next_page_token}&source=deep_link&search_id={self.search_id}"

        raw_response = self._make_api_request(url) # No specific params needed here, all in URL
        json_response = raw_response.json()
        new_next_page_token = json_response.get('meta', {}).get('next_page')
        
        return json_response, new_next_page_token

    def ParseResults(self, json_response, target_list): # Changed 'resonse' to 'json_response'
        if not json_response or 'search_objects' not in json_response:
            print("No search objects found in the response.")
            return []

        products = json_response['search_objects']
        results = []
        if target_list is not None and len(target_list) != 0:
            for product in products:
                title = product.get('title', '') # Use .get for safety
                for keyword in target_list:
                    if keyword.lower() in title.lower(): # Case-insensitive comparison
                        print(f"The title '{title}' contains '{keyword}'.")
                        results.append(product)
                        break # Avoid adding same product multiple times if multiple keywords match
        else:
            results = products # Return all products if no target_list

        print(f"Processed records: {len(products)}")
        print(f"Filtered results records: {len(results)}")
        return results

    def get_all_results_for_keywords(self, keywords, target_list=None, max_results=None, **kwargs):
        """
        Retrieves all results for given keywords, handling pagination and optional filtering.

        :param keywords: Keywords to search for.
        :param target_list: Optional list of keywords to filter titles in ParseResults.
        :param max_results: Optional maximum number of results to return.
        :param kwargs: Additional parameters for the initial search.
        :return: List of product results.
        """
        all_products = []

        try:
            initial_json_response, next_page_token = self.search_initial(keywords, **kwargs)

            if initial_json_response:
                parsed_results = self.ParseResults(initial_json_response, target_list)
                all_products.extend(parsed_results)
            else:
                # If initial search yields nothing, no point in continuing
                next_page_token = None

            while next_page_token:
                if max_results is not None and len(all_products) >= max_results:
                    print(f"Reached max_results limit of {max_results}. Stopping pagination.")
                    break

                print(f"Fetching next page with token: {next_page_token}")
                next_page_json_response, next_page_token = self.fetch_next_page(next_page_token)

                if next_page_json_response:
                    parsed_results = self.ParseResults(next_page_json_response, target_list)
                    all_products.extend(parsed_results)
                else:
                    # If fetching next page yields nothing or token becomes None, stop
                    print("No more results from fetch_next_page or token is invalid.")
                    break

        except APIConnectionError as e:
            print(f"An API connection error occurred: {e}")
            # Depending on desired behavior, could re-raise, return partial results, or empty
            # For now, it will fall through and return whatever all_products contains.
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Handle other potential errors gracefully
            # For now, it will fall through

        if max_results is not None:
            return all_products[:max_results]
        return all_products