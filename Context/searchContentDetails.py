import uuid
from helper import Helper
from constants import Constants

class SearchContentDetails:
    def __init__(self, search_type = Constants.SearchType.Direct_search, 
                     search_text = "None", 
                     content_filter_checkBox = Constants.Buttons.Button_disable_status,
                     content_filter_text = "None",
                     price_filter_checkbox = Constants.Buttons.Button_disable_status,
                     price_limit_from = 0,
                     price_limit_to = 9999,
                     searchGuid=None):
        if searchGuid is None:
            searchGuid = str(uuid.uuid4())
        self._search_type = search_type
        self._search_text = search_text    
        self._content_filter_checkBox = content_filter_checkBox
        self._content_filter_text = content_filter_text
        self._price_filter_checkbox = price_filter_checkbox
        self._price_limit_from = price_limit_from
        self._price_limit_to = price_limit_to  
        self._searchGuid = searchGuid
        self._content = []

        @property
        def Search_type(self):
            return  self._search_type

        @Search_type.setter
        def Search_type(self, value):
            self._search_type = value

        @property
        def Search_text(self):
            return  self._search_text

        @Search_text.setter
        def Search_text(self, value):
            self._search_text = value

        @property
        def Content_filter_checkBox(self):
            return  self._content_filter_checkBox

        @Content_filter_checkBox.setter
        def Content_filter_checkBox(self, value):
            self._content_filter_checkBox = value
        
        @property
        def Content_filter_text(self):
            return  self._content_filter_text

        @Content_filter_text.setter
        def Content_filter_text(self, value):
            self._content_filter_text = value

        @property
        def Price_filter_checkbox(self):
            return  self._price_filter_checkbox

        @Price_filter_checkbox.setter
        def Price_filter_checkbox(self, value):
            self._price_filter_checkbox = value

        @property
        def Price_limit_from(self):
            return  self._price_limit_from

        @Price_limit_from.setter
        def Price_limit_from(self, value):
            self._price_limit_from = value

        @property
        def Price_limit_to(self):
            return  self._price_limit_to

        @Price_limit_to.setter
        def Price_limit_to(self, value):
            self._price_limit_to = value

        @property
        def SearchGuid(self):
            return  self._searchGuid

        @SearchGuid.setter
        def SearchGuid(self, value):
            self._searchGuid = value

        @property
        def Content(self):
            return  self._content

        @Content.setter
        def Content(self, value):
            self._content = value        

        def to_json(self):
            json_data = {
            "search_type": Helper.remove_newline_symbol(Search_type()),            
            "search_text": Helper.remove_newline_symbol(Search_text()),
            "content_filter_checBox": Content_filter_checkBox(),
            "content_filter_text": Helper.remove_newline_symbol(Content_filter_text()),
            "price_filter_checkbox": Price_filter_checkbox(),
            "price_limit_from": Helper.remove_newline_symbol(Price_limit_from()),
            "price_limit_to": Helper.remove_newline_symbol(Price_limit_to())       
            }        
            return json_data
        
        def from_json(self, json_data):           
            self.Search_type = json_data.get("search_type", Constants.SearchType.Direct_search),
            self.Search_text=json_data.get("search_text", "None"),
            self.content_filter_checkBox=json_data.get("content_filter_checkBox", Constants.Buttons.Button_disable_status),
            self.content_filter_text=json_data.get("content_filter_text", "None"),
            self.price_filter_checkbox=json_data.get("price_filter_checkbox", Constants.Buttons.Button_disable_status),
            self.price_limit_from=json_data.get("price_limit_from", 0),
            self.price_limit_to=json_data.get("price_limit_to", 9999),
            self.searchGuid=json_data.get("searchGuid", str(uuid.uuid4()))
       

    class Fields:
        Search_type = "search_type"
        Search_text = "search_text"
        Content_filter_checkBox = "content_filter_checkBox"
        Content_filter_text = "content_filter_text"
        Price_filter_checkbox = "price_filter_checkbox"
        Price_limit_from = "price_limit_from"
        Price_limit_to = "price_limit_to"
        SearchGuid_= "searchGuid"