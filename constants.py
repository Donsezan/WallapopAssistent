class Constants:
    History_file_name = "History.josn"
    Parameters_file_name = "Parameters.json"
    SearchString_Siparator = ','
    CheackBox_enabled_status = "active"
    Direct_search_path = "https://api.wallapop.com/api/v3/general/search"    
    Items_per_rotation = 40
    Temp_folder = "temp"
    
    class SearchType:
        Direct_search = 0
        History_search = 1
    
    class Buttons:
        Refresh_button_working_text = "(working)"
        Refresh_button_normal_text = "Refresh"        
        Refresh_button_pause_text = "Pause"
        Button_disable_color = "gray30"
        Button_enable_color = ['#3B8ED0', '#1F6AA5']
        Button_disable_status = "disabled"