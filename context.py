from helper import Helper

class Context:
    search_text = str
    content_search_checBox = str
    content_search_text = str   
    price_filter_checkbox = str
    price_limit_from = int
    price_limit_to = int
    notification_toastup_checkbox = str
    notification_soundnote_checkbox = str
    refresh_result = int

    @classmethod
    def get_search_text(cls):
        return cls.search_text
    
    @classmethod
    def set_search_text(cls, value):
        cls.search_text = value

    @classmethod
    def get_content_search_checkBox(cls):
        return cls.content_search_checBox
    
    @classmethod
    def set_content_search_checkBox(cls, value):
        cls.content_search_checBox = value

    @classmethod
    def get_content_search_text(cls):
        return cls.content_search_text
    
    @classmethod
    def set_content_search_text(cls, value):
        cls.content_search_text = value

    @classmethod
    def get_refresh_result(cls):
        return cls.refresh_result
    
    @classmethod
    def set_refresh_result(cls, value):
        cls.refresh_result = value

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

    def to_json(cls):
        return {
            "search_text": Helper.remove_newline_symbol(cls.get_search_text()),
            "content_search_checBox": cls.get_content_search_checkBox(),
            "content_search_text": Helper.remove_newline_symbol(cls.get_content_search_text()),
            "price_filter_checkbox": cls.get_price_filter_checkbox(),
            "price_limit_from": Helper.remove_newline_symbol(cls.get_price_limit_from()),
            "price_limit_to": Helper.remove_newline_symbol(cls.get_price_limit_to()),
            "notification_toastup_checkbox": cls.get_notification_toastup_checkbox(),
            "notification_soundnote_checkbox": cls.get_notification_soundnote_checkbox(),
            "refresh_result": Helper.remove_newline_symbol(cls.get_refresh_result())
        }

    @classmethod
    def rehydrate_json(cls, data):
        #data = json.loads(json_str)   
        cls.set_search_text(cls.get_parameter(data, "default_search_text", "None"))
        cls.set_content_search_checkBox(cls.get_parameter(data,"content_search_checBox", "disabled"))
        cls.set_content_search_text(cls.get_parameter(data, "content_search_text", "None"))
        cls.set_price_filter_checkbox(cls.get_parameter(data, "price_filter_checkbox", "disabled"))
        cls.set_price_limit_from(cls.get_parameter(data, "price_limit_from", 0)) 
        cls.set_price_limit_to(cls.get_parameter(data, "price_limit_to", 0))  
        cls.set_notification_toastup_checkbox(cls.get_parameter(data, "notification_toastup_checkbox", "disabled"))
        cls.set_notification_soundnote_checkbox(cls.get_parameter(data, "notification_soundnote_checkbox", "disabled"))
        cls.set_refresh_result(cls.get_parameter(data, "refresh_result", 60)) 

    
    def get_parameter(data, key, default):
        result = default
        if data is not None: 
            try:
                result = data.get(key, default)
            except KeyError as e:
                print(f"KeyError: {e}")
        return result
        