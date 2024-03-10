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