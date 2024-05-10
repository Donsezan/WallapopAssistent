from helper import Helper
from constants import Constants


from Context.baseContext import BaseContext
from Context.searchContentDetails import SearchContentDetails


class Context(BaseContext, SearchContentDetails):
    parameter_dict = dict()

    @classmethod
    def create_param_dict(cls, dict_name): 
        cls.parameter_dict[dict_name] = SearchContentDetails()
        return cls.parameter_dict

    @classmethod
    def remove_param_dict(cls, dict_name):
        cls._validationForKey(dict_name)
        del cls.parameter_dict[dict_name]

    @classmethod
    def get_parameter_dicts(cls):
        return cls.parameter_dict

    @classmethod
    def get_parameter_byKey(cls, dict_name):
        cls._validationForKey(dict_name)        
        return cls.parameter_dict[dict_name]

    @classmethod
    def get_search_type(cls, dict_name):
        cls._validationForKey(dict_name)        
        return int(cls.parameter_dict[dict_name]._search_type)
    
    @classmethod
    def set_search_type(cls,dict_name, value):
        cls._validationForKey(dict_name)     
        cls.parameter_dict[dict_name]._search_type = value   

    @classmethod
    def get_search_text(cls, dict_name):
        cls._validationForKey(dict_name)     
        return cls.parameter_dict[dict_name]._search_text
    
    @classmethod
    def set_search_text(cls, value, dict_name):
        cls._validationForKey(dict_name)   
        cls.parameter_dict[dict_name]._search_text = value  

    @classmethod
    def get_content_filter_checkBox(cls, dict_name):
        cls._validationForKey(dict_name)   
        return cls.parameter_dict[dict_name]._content_filter_checkBox
    
    @classmethod
    def set_content_filter_checkBox(cls,dict_name, value):
        cls._validationForKey(dict_name)   
        cls.parameter_dict[dict_name]._content_filter_checkBox = value

    @classmethod
    def get_content_filter_text(cls, dict_name):
        cls._validationForKey(dict_name)   
        return cls.parameter_dict[dict_name]._content_filter_text
    
    @classmethod
    def set_content_filter_text(cls, dict_name, value):
        cls._validationForKey(dict_name)   
        cls.parameter_dict[dict_name]._content_filter_text = value

    @classmethod
    def get_price_filter_checkbox(cls, dict_name):
        cls._validationForKey(dict_name)   
        return cls.parameter_dict[dict_name]._price_filter_checkbox
    
    @classmethod
    def set_price_filter_checkbox(cls, dict_name, value):
        cls._validationForKey(dict_name)   
        cls.parameter_dict[dict_name]._price_filter_checkbox = value

    @classmethod
    def get_price_limit_from(cls, dict_name):
        cls._validationForKey(dict_name)   
        return int(cls.parameter_dict[dict_name]._price_limit_from)
    
    @classmethod
    def set_price_limit_from(cls, dict_name, value):
        cls._validationForKey(dict_name)   
        cls.parameter_dict[dict_name]._price_limit_from = value

    @classmethod
    def get_price_limit_to(cls, dict_name):
        cls._validationForKey(dict_name)   
        return int(cls.parameter_dict[dict_name]._price_limit_to)
    
    @classmethod
    def set_price_limit_to(cls, dict_name, value):
        cls._validationForKey(dict_name)   
        cls.parameter_dict[dict_name]._price_limit_to = value


    def to_json(cls):
        json_data = {
            "search_type": Helper.remove_newline_symbol(cls.get_search_type()),            
            "search_text": Helper.remove_newline_symbol(cls.get_search_text()),
            "content_filter_checBox": cls.get_content_filter_checkBox(),
            "content_filter_text": Helper.remove_newline_symbol(cls.get_content_filter_text()),
            "price_filter_checkbox": cls.get_price_filter_checkbox(),
            "price_limit_from": Helper.remove_newline_symbol(cls.get_price_limit_from()),
            "price_limit_to": Helper.remove_newline_symbol(cls.get_price_limit_to()),
            "history_digging_days": Helper.remove_newline_symbol(cls.get_history_digging_days()),
            "notification_toastup_checkbox": cls.get_notification_toastup_checkbox(),
            "notification_soundnote_checkbox": cls.get_notification_soundnote_checkbox(),
            "refresh_result": Helper.remove_newline_symbol(cls.get_refresh_time()),
            "auto_refresh_checkbox": Helper.remove_newline_symbol(cls.get_auto_refresh_checkbox()),
            "contents_dictionary": cls.parameter_dict,        
        }        
        return json_data

    @classmethod
    def rehydrate_json(cls, data):
        cls.set_history_digging_days(cls._get_parameter(data, "history_digging_days", 0))  
        cls.set_notification_toastup_checkbox(cls._get_parameter(data, "notification_toastup_checkbox", Constants.Buttons.Button_disable_status))
        cls.set_notification_soundnote_checkbox(cls._get_parameter(data, "notification_soundnote_checkbox", Constants.Buttons.Button_disable_status))
        cls.set_refresh_time(cls._get_parameter(data, "refresh_result", 60)),
        cls.set_auto_refresh_checkbox(cls._get_parameter(data, "auto_refresh_checkbox", Constants.Buttons.Button_disable_status)),


        contents_dictionarys =cls._get_parameter(data, "contents_dictionary", None)
        if contents_dictionarys is not None:           
            for dict in  contents_dictionarys:
                for key, value in dict.items():     
                    cls.parameter_dict[key] = {}
                    for content_key, content_data in value.items():
                        if isinstance(content_data, dict):
                            cls.parameter_dict[key][content_key] = SearchContentDetails(
                                search_type = cls._get_parameter(content_data, SearchContentDetails.Fields.Search_type ,Constants.SearchType.Direct_search),
                                search_text = cls._get_parameter(content_data, SearchContentDetails.Fields.Search_text, "None"),
                                content_filter_checkBox = cls._get_parameter(content_data, SearchContentDetails.Fields.Content_filter_checkBox, Constants.Buttons.Button_disable_status),
                                content_filter_text = cls._get_parameter(content_data, SearchContentDetails.Fields.Content_filter_text, "None"),
                                price_filter_checkbox = cls._get_parameter(content_data, SearchContentDetails.Fields.Price_filter_checkbox, Constants.Buttons.Button_disable_status),
                                price_limit_from = cls._get_parameter(content_data, SearchContentDetails.Fields.Price_limit_from, 0),
                                price_limit_to = cls._get_parameter(content_data, SearchContentDetails.Fields.Price_limit_to, 99999),
                            )
        else:
            cls.parameter_dict = cls.create_param_dict("First")

        vsd = cls.get_search_text("First")
        cls.set_context_rehydrate_state(True)
    
    def _get_parameter(data, key, default):
        result = default
        if data is not None: 
            try:
                result = data.get(key, default)
            except KeyError as e:
                print(f"KeyError: {e} for key: {key}")
        return result
    @classmethod

    def _validationForKey(cls, key):
        if not key in cls.parameter_dict:
            raise ValueError("invalid dictionary key: " + key)