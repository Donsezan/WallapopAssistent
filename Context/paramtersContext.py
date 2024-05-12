from helper import Helper
from Context.searchContentDetails import SearchContentDetails

class ParamtersContext(SearchContentDetails):      
    @classmethod
    def cleare_dict(cls):
        cls.ParamtersStructure.parameter_dict = dict()

    @classmethod
    def overide_dict(cls, target):
        cls.ParamtersStructure.parameter_dict = target

    @classmethod
    def create_dict(cls, dict_name): 
        cls.ParamtersStructure.parameter_dict[dict_name] = SearchContentDetails()
        return cls.ParamtersStructure.parameter_dict

    @classmethod
    def remove_dict(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)
        del cls.ParamtersStructure.parameter_dict[dict_name]

    @classmethod
    def get_dict(cls):
        return cls.ParamtersStructure.parameter_dict
    
    @classmethod
    def get_parameter_byKey(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)        
        return cls.ParamtersStructure.parameter_dict[dict_name]

    @classmethod
    def get_search_type(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)        
        return int(cls.ParamtersStructure.parameter_dict[dict_name]._search_type)
    
    @classmethod
    def set_search_type(cls,dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)     
        cls.ParamtersStructure.parameter_dict[dict_name]._search_type = value   

    @classmethod
    def get_search_text(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)     
        return cls.ParamtersStructure.parameter_dict[dict_name]._search_text
    
    @classmethod
    def set_search_text(cls, dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        cls.ParamtersStructure.parameter_dict[dict_name]._search_text = value  

    @classmethod
    def get_content_filter_checkBox(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        return cls.ParamtersStructure.parameter_dict[dict_name]._content_filter_checkBox
    
    @classmethod
    def set_content_filter_checkBox(cls,dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        cls.ParamtersStructure.parameter_dict[dict_name]._content_filter_checkBox = value

    @classmethod
    def get_content_filter_text(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        return cls.ParamtersStructure.parameter_dict[dict_name]._content_filter_text
    
    @classmethod
    def set_content_filter_text(cls, dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        cls.ParamtersStructure.parameter_dict[dict_name]._content_filter_text = value

    @classmethod
    def get_price_filter_checkbox(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        return cls.ParamtersStructure.parameter_dict[dict_name]._price_filter_checkbox
    
    @classmethod
    def set_price_filter_checkbox(cls, dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        cls.ParamtersStructure.parameter_dict[dict_name]._price_filter_checkbox = value

    @classmethod
    def get_price_limit_from(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        return int(cls.ParamtersStructure.parameter_dict[dict_name]._price_limit_from)
    
    @classmethod
    def set_price_limit_from(cls, dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        cls.ParamtersStructure.parameter_dict[dict_name]._price_limit_from = value

    @classmethod
    def get_price_limit_to(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        return int(cls.ParamtersStructure.parameter_dict[dict_name]._price_limit_to)
    
    @classmethod
    def set_price_limit_to(cls, dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        cls.ParamtersStructure.parameter_dict[dict_name]._price_limit_to = value
        
    @classmethod
    def get_refresh_time(cls):
        return cls.ParamtersStructure.refresh_result
    
    @classmethod
    def set_refresh_time(cls, value):
        cls.ParamtersStructure.refresh_result = value

    @classmethod
    def get_auto_refresh_checkbox(cls):
        return cls.ParamtersStructure.auto_refresh_checkbox
    
    @classmethod
    def set_auto_refresh_checkbox(cls, value):
       cls.ParamtersStructure.auto_refresh_checkbox = value

    @classmethod
    def get_history_digging_days(cls):
        return int(cls.ParamtersStructure.history_digging_days)
    
    @classmethod
    def set_history_digging_days(cls, value):
        cls.ParamtersStructure.history_digging_days = value
    
    @classmethod
    def get_notification_toastup_checkbox(cls):
        return cls.ParamtersStructure.notification_toastup_checkbox
    
    @classmethod
    def set_notification_toastup_checkbox(cls, value):
        cls.ParamtersStructure.notification_toastup_checkbox = value

    @classmethod
    def get_notification_soundnote_checkbox(cls):
        return cls.ParamtersStructure.notification_soundnote_checkbox
    
    @classmethod
    def set_notification_soundnote_checkbox(cls, value):
       cls.ParamtersStructure.notification_soundnote_checkbox = value 
    
    @classmethod
    def get_content(cls, dict_name):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        return int(cls.ParamtersStructure.parameter_dict[dict_name]._content)
    
    @classmethod
    def set_content(cls, dict_name, value):
        Helper._validationForKey(cls.ParamtersStructure.parameter_dict, dict_name)   
        cls.ParamtersStructure.parameter_dict[dict_name]._content = value
  
    class ParamtersStructure:
        history_digging_days = int
        notification_toastup_checkbox = str
        notification_soundnote_checkbox = str
        refresh_result = int
        auto_refresh_checkbox = str
        parameter_dict = dict()
    