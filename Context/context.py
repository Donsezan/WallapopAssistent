from helper import Helper
from constants import Constants
from Context.paramtersContext import ParamtersContext

from Context.searchContentDetails import SearchContentDetails

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
        for key, value in cls.MainParameters.parameter_dict.get_dict():
            parameter_dict_serialized[key] = value.to_json()

        json_data = {
            "history_digging_days": cls.MainParameters.history_digging_days,
            "notification_toastup_checkbox": cls.MainParameters.notification_toastup_checkbox,
            "notification_soundnote_checkbox": cls.MainParameters.notification_soundnote_checkbox,
            "refresh_result": cls.MainParameters.refresh_result,
            "auto_refresh_checkbox": cls.MainParameters.auto_refresh_checkbox,           
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

        contents_dictionarys =cls._get_parameter(data, "parameter_dict", None)
        if contents_dictionarys is not None:     
            for dict in  contents_dictionarys:
                cls.MainParameters.from_json(dict)


        # contents_dictionarys =cls._get_parameter(data, "contents_dictionary", None)
        # if contents_dictionarys is not None:           
        #     for dict in  contents_dictionarys:
        #         for key, value in dict.items():     
        #             cls.parameter_dict[key] = {}
        #             for content_key, content_data in value.items():
        #                 if isinstance(content_data, dict):
        #                     cls.parameter_dict[key][content_key] = SearchContentDetails(
        #                         search_type = cls._get_parameter(content_data, SearchContentDetails.Fields.Search_type ,Constants.SearchType.Direct_search),
        #                         search_text = cls._get_parameter(content_data, SearchContentDetails.Fields.Search_text, "None"),
        #                         content_filter_checkBox = cls._get_parameter(content_data, SearchContentDetails.Fields.Content_filter_checkBox, Constants.Buttons.Button_disable_status),
        #                         content_filter_text = cls._get_parameter(content_data, SearchContentDetails.Fields.Content_filter_text, "None"),
        #                         price_filter_checkbox = cls._get_parameter(content_data, SearchContentDetails.Fields.Price_filter_checkbox, Constants.Buttons.Button_disable_status),
        #                         price_limit_from = cls._get_parameter(content_data, SearchContentDetails.Fields.Price_limit_from, 0),
        #                         price_limit_to = cls._get_parameter(content_data, SearchContentDetails.Fields.Price_limit_to, 99999),
        #                     )
        # else:
        #     cls.parameter_dict = cls.MainParameters.create_dict("First")

        # vsd = cls.MainParameters.get_search_text("First")
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