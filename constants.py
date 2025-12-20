class Constants:
    History_file_name = lambda additional_symbols: f"History_{additional_symbols}.json"
    Parameters_file_name = "Parameters.json"
    SearchString_Siparator = ','
    CheackBox_enabled_status = "active"
    Direct_search_path = "https://api.wallapop.com/api/v3/search"    
    Items_per_rotation = 40
    Temp_folder = "temp"

    class Frames:
        Home = "Home"
        Settings = "Settings"
    
    class SearchType:
        Direct_search = 0
        History_search = 1
    
    class Colors:
        Primary = "#13C1AC" # Wallapop Green
        Background = "#F0F2F5" # Light Gray
        CardBackground = "#FFFFFF" # White
        TextPrimary = "#253238" # Dark Blue/Gray
        TextSecondary = "#90A4AE"
        TextError = "#e04f5f" # Red
        GrayNormal = "gray75"
        GrayHover = "gray85"
        
    class Buttons:
        Refresh_button_working_text = "(working)"
        Refresh_button_normal_text = "Refresh"        
        Refresh_button_pause_text = "Pause"
        
        Button_disable_color = "gray80" # Lighter gray for disabled
        Button_restricted_color = "#e04f5f" # Red
        Button_enable_color = "#13C1AC" # Wallapop Green
        
        Button_disable_status = "disabled"

    class Texts:
        Text_disable_color = "gray60"
        Text_enable_color = "#253238"
        Text_restricted_color = "#e04f5f"
        Text_normal_color = "#253238"