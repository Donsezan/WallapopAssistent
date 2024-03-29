from Services.GraberServices import GraberServices
from Services.FileServices import FileServices
from constants import Constants
from datetime import datetime 

class Main_logic:
    def __init__(self, ctx):
        self.ctx = ctx
        self.target_list = ""
        self.loaded_contnet_exist = False
        #["NUC","Latitude", "thinkpad", "Dell", "x390", "HP"]

    def Init(self):     
        file_services_instance = FileServices()
 

        self.ctx.rehydrate_json(file_services_instance.Rehidrate_from_file(Constants.Parameters_file_name))
        self.target_list = self.ctx.get_search_text().split(Constants.SearchString_Siparator)
       
        sorted_objects = []

        self.loaded_contnet = file_services_instance.Rehidrate_from_file(Constants.History_file_name)
        self.loaded_contnet = self.delete_old_records_in_histry(self.loaded_contnet,  self.ctx.get_history_digging_days())
      
        if self.loaded_contnet is not None and len(self.loaded_contnet) != 0:    
            self.loaded_contnet_exist = True  
            sorted_objects = self.sort_content_by_date(self.loaded_contnet)
        else:
            self.loaded_contnet_exist = False             

        # Get the latest object       
        self.new_content_array = self.direct_load_content(sorted_objects)
             
      
        self.finalContent = file_services_instance.Merge_content(self.loaded_contnet, self.new_content_array)
        file_services_instance.Save_content_to_file(self.finalContent, Constants.History_file_name)

        if self.ctx.get_content_filter_checkBox() == Constants.CheackBox_enabled_status:
           self.finalContent = self.filter_content(self.finalContent)
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
    
    def direct_load_content(self, sorted_objects):
        graberServices_instance = GraberServices()
        dip_limit = 5
        new_content_array = []
        index = 1        
        while True:
            # new_content = self.get_from_last_content(graberServices_instance, index)
            new_content = self.get_from_directsearch_content(graberServices_instance, index, self.target_list[0])

            new_content_array += new_content
            index = index + 1        
            
            if len(self.response['search_objects']) == 0:
                break

            if index > dip_limit:
                break               

            if len(new_content) > 0:
                new_sorted_content =  self.sort_content_by_date(new_content)  
                new_content_reachedLimit = self.content_is_older_than(new_sorted_content[-1]['modification_date'], self.ctx.get_history_digging_days())
                if new_content_reachedLimit:
                    break
                if self.loaded_contnet_exist:  
                    if len(sorted_objects) > 0:  
                        if datetime.fromisoformat(sorted_objects[0]['modification_date']) >=  datetime.fromisoformat(new_sorted_content[-1]['modification_date']):
                            break
        return new_content_array             

    def get_from_last_content(self, graberServices, index):
        self.response = graberServices.GetReposne(request_param=graberServices.SetParam(index * 40))
        new_content = graberServices.ParseResults(self.response, self.target_list) 
        return new_content
    
    def get_from_directsearch_content(self, graberServices, index, target_text):
        self.response = graberServices.GetReposne(request_param=graberServices.SetParam_for_direct(target_text, index))
        new_content = graberServices.ParseResults(self.response, None) 
        return new_content

    def filter_content(self, contents):
        for filter_text in self.ctx.get_content_filter_text().split(Constants.SearchString_Siparator):  
             contents = [obj for obj in contents if filter_text in obj['description'].lower()]
        return contents
    
    def sort_content_by_date(self, content):
        return sorted(content, key=lambda x: datetime.strptime(x['creation_date'], '%Y-%m-%dT%H:%M:%S.%f%z'), reverse=True)