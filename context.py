import json

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

    def to_json(self):
        return {
            "search_text": self.remove_newline_symbol(self.search_text),
            "content_search_checBox": self.content_search_checBox,
            "content_search_text": self.remove_newline_symbol(self.content_search_text),
            "price_filter_checkbox": self.price_filter_checkbox,
            "price_limit_from": self.remove_newline_symbol(self.price_limit_from),
            "price_limit_to": self.remove_newline_symbol(self.price_limit_to),
            "notification_toastup_checkbox": self.notification_toastup_checkbox,
            "notification_soundnote_checkbox": self.notification_soundnote_checkbox,
            "refresh_result": self.remove_newline_symbol(self.refresh_result)
        }

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        instance = cls()
        instance.search_text = data["search_text"]
        instance.content_search_checBox = data["content_search_checBox"]
        instance.content_search_text = data["content_search_text"]
        instance.price_filter_checkbox = data["price_filter_checkbox"]
        instance.price_limit_from = data["price_limit_from"]
        instance.price_limit_to = data["price_limit_to"]
        instance.notification_toastup_checkbox = data["notification_toastup_checkbox"]
        instance.notification_soundnote_checkbox = data["notification_soundnote_checkbox"]
        instance.refresh_result = data["refresh_result"]
        return instance
    
    def remove_newline_symbol(self, input):
        output = input
        symbol = "\n"
        if input.endswith(symbol):       
            output = input[:-len(symbol)]
        return output