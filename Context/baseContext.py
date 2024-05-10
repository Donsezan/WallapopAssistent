class BaseContext:
    history_digging_days = int
    notification_toastup_checkbox = str
    notification_soundnote_checkbox = str
    refresh_result = int
    auto_refresh_checkbox = str
    main_content = {}

    context_rehydrate_state = False
    updated_paramter_status = True
   
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
    def get_main_content(cls, key):
        for dictionary in cls.main_content:
            if key in dictionary:
                return dictionary
        raise ValueError("invalid dictionary key: " + key)
    
    @classmethod
    def get_all_content(cls):
        return cls.main_content
    
    @classmethod
    def set_all_content(cls, all_content):
        cls.main_content
    
    @classmethod
    def set_main_content(cls,key, value):
        cls.main_content[key] = value

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
