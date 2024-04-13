from Services.GraberServices import GraberServices
from Services.FileServices import FileServices
from Services.FiltersServices import FiltersServices
from constants import Constants
from datetime import datetime 
from helper import Helper

class Main_logic:
    def __init__(self, ctx):
        self.ctx = ctx
        self.target_list = ""
        self.first_run = True
        self.file_services_instance = FileServices() 
        self.filtering_services_instance = FiltersServices()   
           
    def rehydrate_contnet(self):     
        if (self.ctx.get_context_rehydrate_state()):
            return self.ctx.get_main_content()
        self.target_list = self.ctx.get_search_text().split(Constants.SearchString_Siparator)    
        self.ctx.rehydrate_json(self.file_services_instance.Rehidrate_from_file(Constants.Parameters_file_name))               
        loaded_contnet = self.file_services_instance.Rehidrate_from_file(Constants.History_file_name)

        #Filter old content section  
        previos_sorted_objects = []   
        if loaded_contnet is not None and len(loaded_contnet) != 0:
            loaded_contnet = self.delete_old_records_in_histry(loaded_contnet,  self.ctx.get_history_digging_days())  
            loaded_contnet = self._filterContent(contents=loaded_contnet)
            previos_sorted_objects = Helper.sort_content_by_date(loaded_contnet)     

        self.ctx.set_main_content(previos_sorted_objects) 
        self.ctx.set_context_rehydrate_state(True)     
        return previos_sorted_objects
    
    def get_content(self):   
        previos_sorted_objects = self.ctx.get_main_content()    
        if(self.ctx.get_updated_paramter_status()):
            previos_sorted_objects= self._filterContent(contents=previos_sorted_objects)
            self.ctx.set_updated_paramter_status(False)
            self.ctx.set_main_content(previos_sorted_objects)    
     
        new_content_array = self.load_content(previos_sorted_objects)             
        #Filter new content section
       
        new_content_array = self._filterContent(contents=new_content_array)

        if len( Helper.find_differences_in_array(new_content_array, previos_sorted_objects) ) > 0:
            finalContent = self.file_services_instance.Merge_content(previos_sorted_objects, new_content_array)
            self.file_services_instance.Save_content_to_file(finalContent, Constants.History_file_name)        
            self.file_services_instance.Delete_old_files(finalContent)
            self.file_services_instance.Download_missed_photos(finalContent)
            previos_sorted_objects = finalContent
            self.ctx.set_main_content(Helper.sort_content_by_date(previos_sorted_objects, reversed = True))

        return previos_sorted_objects

    def _filterContent(self, contents):
        return self.filtering_services_instance.filteringContent(contents=contents,
                                                                            titlePatern=Helper.split_string(self.ctx.get_search_text()),
                                                                            isDiscriptionCheck= self.ctx.get_content_filter_checkBox() == Constants.CheackBox_enabled_status,
                                                                            discriptionPatern=Helper.split_string(self.ctx.get_content_filter_text()),
                                                                            isPriceCheck=self.ctx.get_price_filter_checkbox() == Constants.CheackBox_enabled_status,
                                                                            priceRange=[self.ctx.get_price_limit_from(),self.ctx.get_price_limit_to()])


    def content_is_older_than(self, date_str, days):
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        time_difference = datetime.now(date_object.tzinfo) - date_object
        return time_difference.days > days
    
    def delete_old_records_in_histry(self, contents, days):
        if contents is None or len(contents) == 0:      
            return None
        for content in contents:  
            date_object = content['creation_date']
            if(self.content_is_older_than(date_object, days)):
                contents.remove(content)
        return contents
    
    def load_content(self, sorted_objects):
        # if __debug__:
        #     return self.file_services_instance.Rehidrate_from_file('sample_content')
        previos_atempt_sucseed = True

        graberServices_instance = GraberServices()
        self.target_list = self.ctx.get_search_text().split(Constants.SearchString_Siparator)    
        #dip_limit = 500
        new_content_array = []
        index = 1        
        while True:
            new_content = []
            if self.ctx.get_search_type() == Constants.SearchType.Direct_search:
                for target in self.target_list:  
                    new_content += self.get_from_directsearch_content(graberServices_instance, index, target)
            else: 
                new_content = self.get_from_last_content(graberServices_instance, index)
          
            new_content_array += new_content
            index = index + 1        
            
            if len(self.response['search_objects']) == 0:
                if not previos_atempt_sucseed:                   
                    break
                previos_atempt_sucseed = False

            # if index > dip_limit:
            #     break               

            if len(new_content) > 0:
                new_sorted_content =  Helper.sort_content_by_date(new_content)  
                new_content_reachedLimit = self.content_is_older_than(new_sorted_content[-1]['modification_date'], self.ctx.get_history_digging_days())
                if new_content_reachedLimit:
                    break
                if not sorted_objects is None and len(sorted_objects) > 0:    
                    if datetime.fromisoformat(sorted_objects[0]['modification_date']) >=  datetime.fromisoformat(new_sorted_content[-1]['modification_date']):
                        break
        return new_content_array             

    def get_from_last_content(self, graberServices, index):
        self.response = graberServices.GetReposne(request_param=graberServices.SetParam(index * 40))
        new_content = graberServices.ParseResults(self.response, self.target_list) 
        return new_content
    
    def get_from_directsearch_content(self, graberServices, index, target_text):        
        step = index * Constants.Items_per_rotation
        self.response = graberServices.GetReposne(request_param=graberServices.SetParam_for_direct(target_text, index,  step - Constants.Items_per_rotation, step))
        new_content = graberServices.ParseResults(self.response, None) 
        return new_content   

  