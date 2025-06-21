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
    
    class Buttons:
        Refresh_button_working_text = "(working)"
        Refresh_button_normal_text = "Refresh"        
        Refresh_button_pause_text = "Pause"
        Button_disable_color = "gray30"
        Button_restricted_color = "Red"
        Button_enable_color = ['#3B8ED0', '#1F6AA5']
        Button_disable_status = "disabled"

    class Texts:
        Text_disable_color = "Grey"
        Text_enable_color = "White"
        Text_restricted_color = "Red"
        Text_normal_color = ['#F9F9FA', '#1D1E1E']