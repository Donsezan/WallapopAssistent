import uuid
from helper import Helper
from constants import Constants
from Context.searchContentDetails import SearchContentDetails
from Context.paramtersContext import ParamtersContext

class Context():
    parameter_dict = dict()
    context_rehydrate_state = False
    updated_paramter_status = True
        
    @classmethod
    def get_context_rehydrate_state(cls):
        return cls.context_rehydrate_state
    
    @classmethod
    def set_context_rehydrate_state(cls, value):
        cls.context_rehydrate_state = value

    @classmethod
    def get_updated_paramter_status(cls):
        return cls.updated_paramter_status
    
    @classmethod
    def set_updated_paramter_status(cls, value):
        cls.updated_paramter_status = value

    def to_json(cls):
        parameter_dict_serialized = {}
        for key, value in cls.MainParameters.get_dict().items():
            parameter_dict_serialized[key] = {
            "search_type": Helper.remove_newline_symbol(value._search_type),            
            "search_text": Helper.remove_newline_symbol(value._search_text),
            "content_filter_checBox": value._content_filter_checkBox,
            "content_filter_text": Helper.remove_newline_symbol(value._content_filter_text),
            "price_filter_checkbox": value._price_filter_checkbox,
            "price_limit_from": Helper.remove_newline_symbol(value._price_limit_from),
            "price_limit_to": Helper.remove_newline_symbol(value._price_limit_to)       
            }        
        json_data = {
            "history_digging_days": cls.MainParameters.get_history_digging_days(),
            "notification_toastup_checkbox": cls.MainParameters.get_notification_toastup_checkbox(),
            "notification_soundnote_checkbox": cls.MainParameters.get_notification_soundnote_checkbox(),
            "refresh_result": cls.MainParameters.get_refresh_time(),
            "auto_refresh_checkbox": cls.MainParameters.get_auto_refresh_checkbox(),           
            "parameter_dict": parameter_dict_serialized
        }        
        return json_data

    @classmethod
    def rehydrate_json(cls, data):        
        cls.MainParameters.set_history_digging_days(cls._get_parameter(data, "history_digging_days", 0))  
        cls.MainParameters.set_notification_toastup_checkbox(cls._get_parameter(data, "notification_toastup_checkbox", Constants.Buttons.Button_disable_status))
        cls.MainParameters.set_notification_soundnote_checkbox(cls._get_parameter(data, "notification_soundnote_checkbox", Constants.Buttons.Button_disable_status))
        cls.MainParameters.set_refresh_time(cls._get_parameter(data, "refresh_result", 60)),
        cls.MainParameters.set_auto_refresh_checkbox(cls._get_parameter(data, "auto_refresh_checkbox", Constants.Buttons.Button_disable_status)),

        contents_dictionarys =cls._get_parameter(data, Context.Fields.Parameter_dict, None)
        if contents_dictionarys is not None:     
            for key, value in  contents_dictionarys.items():
                cls.MainParameters.create_dict(key)
                cls.MainParameters.set_search_type(key, cls._get_parameter(value, SearchContentDetails.Fields.Search_type, Constants.SearchType.Direct_search))
                cls.MainParameters.set_search_text(key, cls._get_parameter(value, SearchContentDetails.Fields.Search_text, "None"))
                cls.MainParameters.set_content_filter_checkBox(key, cls._get_parameter(value, SearchContentDetails.Fields.Content_filter_checkBox, Constants.Buttons.Button_disable_status))
                cls.MainParameters.set_content_filter_text(key, cls._get_parameter(value, SearchContentDetails.Fields.Content_filter_text, "None"))
                cls.MainParameters.set_price_filter_checkbox(key, cls._get_parameter(value, SearchContentDetails.Fields.Price_filter_checkbox, Constants.Buttons.Button_disable_status))
                cls.MainParameters.set_price_limit_from(key, cls._get_parameter(value, SearchContentDetails.Fields.Price_limit_from, 0))
                cls.MainParameters.set_price_limit_to(key, cls._get_parameter(value, SearchContentDetails.Fields.Price_limit_to, 99999))
                cls.MainParameters.set_SearchGuid(key, cls._get_parameter(value, SearchContentDetails.Fields.Price_limit_to, str(uuid.uuid4())))
        cls.set_context_rehydrate_state(True)
    
    def _get_parameter(data, key, default):
        result = default
        if data is not None: 
            try:
                result = data.get(key, default)
            except KeyError as e:
                print(f"KeyError: {e} for key: {key}")
        return result

    class MainParameters(ParamtersContext):
        pass

    class TempParameters(ParamtersContext):
        pass

    class Fields:
        Parameter_dict = "parameter_dict"