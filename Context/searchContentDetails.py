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
                     searchGuid=None,
                     dip_limit=0):
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
        self._dip_limit = dip_limit
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
    def Dip_limit(self):
        return self._dip_limit

    @Dip_limit.setter
    def Dip_limit(self, value):
        self._dip_limit = value

    @property
    def Content(self):
        return  self._content

    @Content.setter
    def Content(self, value):
        self._content = value

    def to_json(self):
        # Using direct attribute access like _search_type for serialization
        # as it seems to be the pattern in Context.to_json and to avoid issues with Helper.remove_newline_symbol
        # if properties return non-string types directly for some fields.
        json_data = {
            self.Fields.Search_type: Helper.remove_newline_symbol(self._search_type),
            self.Fields.Search_text: Helper.remove_newline_symbol(self._search_text),
            self.Fields.Content_filter_checkBox: self._content_filter_checkBox, # Assuming this is a boolean or string not needing newline removal
            self.Fields.Content_filter_text: Helper.remove_newline_symbol(self._content_filter_text),
            self.Fields.Price_filter_checkbox: self._price_filter_checkbox, # Assuming this is a boolean or string
            self.Fields.Price_limit_from: Helper.remove_newline_symbol(str(self._price_limit_from)), # Ensure string for remove_newline
            self.Fields.Price_limit_to: Helper.remove_newline_symbol(str(self._price_limit_to)), # Ensure string for remove_newline
            self.Fields.SearchGuid: self._searchGuid, # searchGuid is already a string
            self.Fields.Dip_limit: self._dip_limit # Assuming dip_limit is a number
        }
        return json_data

    def from_json(self, json_data):
        self.Search_type = json_data.get(self.Fields.Search_type, Constants.SearchType.Direct_search)
        self.Search_text = json_data.get(self.Fields.Search_text, "None")
        self.Content_filter_checkBox = json_data.get(self.Fields.Content_filter_checkBox, Constants.Buttons.Button_disable_status)
        self.Content_filter_text = json_data.get(self.Fields.Content_filter_text, "None")
        self.Price_filter_checkbox = json_data.get(self.Fields.Price_filter_checkbox, Constants.Buttons.Button_disable_status)
        self.Price_limit_from = json_data.get(self.Fields.Price_limit_from, 0)
        self.Price_limit_to = json_data.get(self.Fields.Price_limit_to, 9999)
        self.SearchGuid = json_data.get(self.Fields.SearchGuid, str(uuid.uuid4()))
        self.Dip_limit = json_data.get(self.Fields.Dip_limit, 0)
       

    class Fields:
        Search_type = "search_type"
        Search_text = "search_text"
        Content_filter_checkBox = "content_filter_checkBox" # Corrected typo from checBox
        Content_filter_text = "content_filter_text"
        Price_filter_checkbox = "price_filter_checkbox"
        Price_limit_from = "price_limit_from"
        Price_limit_to = "price_limit_to"
        SearchGuid = "search_guid" # Removed trailing underscore
        Dip_limit = "dip_limit"