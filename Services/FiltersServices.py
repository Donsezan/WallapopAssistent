import re
from datetime import datetime 
from constants import Constants

class FiltersServices:
    def Init():
        print ("Init FiltersServices")

    def filteringContent(self, contents, titlePatern, discriptionPatern,  priceRange, isDiscriptionCheck = False, isPriceCheck = False):
        if contents is None or len(contents) == 0:
             return contents
        contents = self._filter_text(contents, titlePatern, 'title')
        if isDiscriptionCheck:
           contents = self._filter_text(contents, discriptionPatern, 'description')
        if isPriceCheck:
           contents = self._filter_content_by_price(contents, priceRange)
        return contents



    def _filter_text(self, contents, input_patterns, key):
        filtered_contents = []
        compiled_patterns = [re.compile(pattern.replace('*', '\\d*'), re.IGNORECASE) for pattern in input_patterns]    #.* - any symbol
        for obj in contents:
            obj_value = obj[key].lower()          
            if all(pattern.search(obj_value) for pattern in compiled_patterns):
                    filtered_contents.append(obj)
        return filtered_contents
    


    # def _filter_text(self, contents, input_patterns, key):        
    #     filtered_contents = []
    #     for input_pattern in input_patterns:    
    #         pattern = input_pattern.replace('*', '\S{1}')
    #         regex_pattern = re.compile(pattern)   
    #         filtered_contents += [obj for obj in contents if regex_pattern.match(obj[key].lower())]
    #     return filtered_contents
    
    def _filter_content_by_price(self, contents, price_range_dict): # Renamed 'prices' to 'price_range_dict' for clarity
        min_price = float(price_range_dict.get('min', 0))
        max_price = float(price_range_dict.get('max', float('inf'))) # Default max to infinity if not present

        filtered_data = [obj for obj in contents if min_price <= float(obj.get('price', '0')) <= max_price]
        return filtered_data

    
    def _filter_description_content(self, contents):
        for filter_text in self.ctx.get_content_filter_text().split(Constants.SearchString_Siparator):  
                contents = [obj for obj in contents if filter_text in obj['description'].lower()]
        return contents
