class Context:
    search_text = str
    content_search_checBox = str
    content_search_text = str
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