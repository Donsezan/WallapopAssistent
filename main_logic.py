from Services.GraberServices import GraberServices
from Services.FileServices import FileServices
from constants import Constants
from datetime import datetime 

class Main_logic:
    def __init__(self):
        self.max_history_days = 5 
        self.target_list = ["NUC","Latitude", "thinkpad", "Dell", "x390", "HP"]

    def Main(self):
     
        file_services_instance = FileServices()
        graberServices_instance = GraberServices()
       
        sorted_objects = []

        self.loaded_contnet = file_services_instance.Rehidrate_from_file(Constants.History_file_name)
        self.loaded_contnet = self.delete_old_records_in_histry(self.loaded_contnet, self.max_history_days)
        self.loaded_contnet_exist = False
        if self.loaded_contnet is not None and len(self.loaded_contnet) != 0:    
            self.loaded_contnet_exist = True  
            sorted_objects = sorted(self.loaded_contnet, key=lambda x: datetime.strptime(x['creation_date'], '%Y-%m-%dT%H:%M:%S.%f%z'), reverse=True)
        else:
            self.loaded_contnet_exist = False             

        # Get the latest object
        self.new_content_array = []
        new_sorted_objects = ""
        if self.loaded_contnet_exist:     
                new_sorted_objects = sorted(self.loaded_contnet, key=lambda x: datetime.strptime(x['creation_date'], '%Y-%m-%dT%H:%M:%S.%f%z'), reverse=False)
        index = 0        
        while True:
            self.response = graberServices_instance.GetReposne(request_param=graberServices_instance.SetParam(index))
            new_content = graberServices_instance.ParseResults(self.response, self.target_list) 
           
            self.new_content_array += new_content
            index = index + 40           
            
            if len(self.response['search_objects']) == 0:
                break
               
            if len(new_content) > 0:
                if not self.loaded_contnet_exist:  
                    if len(new_sorted_objects) > 0:
                        if self.content_is_older_than(new_sorted_objects[0]['creation_date'], self.max_history_days):
                            break  
                else:                   
                    if datetime.fromisoformat(sorted_objects[0]['creation_date']) >=  datetime.fromisoformat(new_sorted_objects[0]['creation_date']):
                        break
             
      

        self.finalContent = file_services_instance.Merge_content(self.loaded_contnet, self.new_content_array)
        file_services_instance.Save_content_to_file(self.finalContent, Constants.History_file_name)

        file_services_instance.Delete_old_files(self.finalContent)
        file_services_instance.Download_missed_photos(self.finalContent)
        return  self.finalContent
    
    def content_is_older_than(self, date_str, days):
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        time_difference = datetime.now(date_object.tzinfo) - date_object
        return time_difference.days > days
    
    def delete_old_records_in_histry(self, contents, days):
        if self.loaded_contnet is None or len(self.loaded_contnet) == 0:      
            return None
        for content in contents:  
            date_object = content['creation_date']
            if(self.content_is_older_than(date_object, days)):
                contents.remove(content)
        return contents