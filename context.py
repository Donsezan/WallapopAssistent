from helper import Helper
from constants import Constants

class Context:
    search_type = int
    search_text = str
    content_filter_checBox = str
    content_filter_text = str   
    price_filter_checkbox = str
    price_limit_from = int
    price_limit_to = int
    history_digging_days = int
    notification_toastup_checkbox = str
    notification_soundnote_checkbox = str
    refresh_result = int
    auto_refresh_checkbox = str
    main_content = []
    
    context_rehydrate_state = False

    @classmethod
    def get_search_type(cls):
        return int(cls.search_type)
    
    @classmethod
    def set_search_type(cls, value):
        cls.search_type = value

    @classmethod
    def get_search_text(cls):
        return cls.search_text
    
    @classmethod
    def set_search_text(cls, value):
        cls.search_text = value

    @classmethod
    def get_content_filter_checkBox(cls):
        return cls.content_filter_checBox
    
    @classmethod
    def set_content_filter_checkBox(cls, value):
        cls.content_filter_checBox = value

    @classmethod
    def get_content_filter_text(cls):
        return cls.content_filter_text
    
    @classmethod
    def set_content_filter_text(cls, value):
        cls.content_filter_text = value

    @classmethod
    def get_refresh_time(cls):
        return cls.refresh_result
    
    @classmethod
    def set_refresh_time(cls, value):
        cls.refresh_result = value

    @classmethod
    def get_auto_refresh_checkbox(cls):
        return cls.auto_refresh_checkbox
    
    @classmethod
    def set_auto_refresh_checkbox(cls, value):
        cls.auto_refresh_checkbox = value

    @classmethod
    def get_price_filter_checkbox(cls):
        return cls.price_filter_checkbox
    
    @classmethod
    def set_price_filter_checkbox(cls, value):
        cls.price_filter_checkbox = value

    @classmethod
    def get_price_limit_from(cls):
        return cls.price_limit_from
    
    @classmethod
    def set_price_limit_from(cls, value):
        cls.price_limit_from = value

    @classmethod
    def get_price_limit_to(cls):
        return cls.price_limit_to
    
    @classmethod
    def set_price_limit_to(cls, value):
        cls.price_limit_to = value

    @classmethod
    def get_history_digging_days(cls):
        return int(cls.history_digging_days)
    
    @classmethod
    def set_history_digging_days(cls, value):
        cls.history_digging_days = value
    
    @classmethod
    def get_notification_toastup_checkbox(cls):
        return cls.notification_toastup_checkbox
    
    @classmethod
    def set_notification_toastup_checkbox(cls, value):
        cls.notification_toastup_checkbox = value

    @classmethod
    def get_notification_soundnote_checkbox(cls):
        return cls.notification_soundnote_checkbox
    
    @classmethod
    def set_notification_soundnote_checkbox(cls, value):
        cls.notification_soundnote_checkbox = value

    @classmethod
    def get_main_content(cls):
        return cls.main_content
    
    @classmethod
    def set_main_content(cls, value):
        cls.main_content = value

    @classmethod
    def get_context_rehydrate_state(cls):
        return cls.context_rehydrate_state
    
    @classmethod
    def set_context_rehydrate_state(cls, value):
        cls.context_rehydrate_state = value

    def to_json(cls):
        return {
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
            "auto_refresh_checkbox": Helper.remove_newline_symbol(cls.get_auto_refresh_checkbox())
            
        }

    @classmethod
    def rehydrate_json(cls, data):
        #data = json.loads(json_str)   
        cls.set_search_type(cls.get_parameter(data, "search_type", Constants.SearchType.Direct_search))
        cls.set_search_text(cls.get_parameter(data, "search_text", "None"))
        cls.set_content_filter_checkBox(cls.get_parameter(data,"content_filter_checBox", Constants.Buttons.Button_disable_status))
        cls.set_content_filter_text(cls.get_parameter(data, "content_filter_text", "None"))
        cls.set_price_filter_checkbox(cls.get_parameter(data, "price_filter_checkbox", Constants.Buttons.Button_disable_status))
        cls.set_price_limit_from(cls.get_parameter(data, "price_limit_from", 0)) 
        cls.set_price_limit_to(cls.get_parameter(data, "price_limit_to", 99999))  
        cls.set_history_digging_days(cls.get_parameter(data, "history_digging_days", 0))  
        cls.set_notification_toastup_checkbox(cls.get_parameter(data, "notification_toastup_checkbox", Constants.Buttons.Button_disable_status))
        cls.set_notification_soundnote_checkbox(cls.get_parameter(data, "notification_soundnote_checkbox", Constants.Buttons.Button_disable_status))
        cls.set_refresh_time(cls.get_parameter(data, "refresh_result", 60)),
        cls.set_auto_refresh_checkbox(cls.get_parameter(data, "auto_refresh_checkbox", Constants.Buttons.Button_disable_status)),
        cls.set_context_rehydrate_state(True)

    
    def get_parameter(data, key, default):
        result = default
        if data is not None: 
            try:
                result = data.get(key, default)
            except KeyError as e:
                print(f"KeyError: {e}")
        return result
        