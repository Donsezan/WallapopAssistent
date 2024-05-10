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
        self.ctx.rehydrate_json(self.file_services_instance.Rehidrate_from_file(Constants.Parameters_file_name))               
        loaded_contnet = self.file_services_instance.Rehidrate_from_file(Constants.History_file_name)    
            
 
        #Filter out old content section   
        previos_sorted_content = dict 
        if loaded_contnet is not None and bool(loaded_contnet):
            syncked = self._syncContentWithSettings(contents_dicts=loaded_contnet)
            for key, value in syncked:                    
                filterdByDate = self._delete_old_records_in_histry(value,  self.ctx.get_history_digging_days()) 
                filterdByDate_syncked_filtredByContent = self._filterContent(contents=filterdByDate, key=key)
                final_soreted_value = Helper.sort_content_by_date(filterdByDate_syncked_filtredByContent)
                previos_sorted_content[key] = final_soreted_value
            

        self.ctx.set_all_content(previos_sorted_content) 
        self.ctx.set_context_rehydrate_state(True)     
        return previos_sorted_content
    
    def get_content(self):   
        new_content = {}
        final_content = {}
        changing_exist = False

        existing_content = self.ctx.get_all_content()  

        if(self.ctx.get_updated_paramter_status()):
            content = self._syncContentWithSettings(contents_dicts=existing_content)
            for key, value in content: 
                filterd_content= self._filterContent(contents=value, key=key)               
                existing_content[key]=filterd_content
                self.ctx.set_updated_paramter_status(False) 
     

        for param_key in self.ctx.get_parameter_dicts(): 
            downloaded_content = self.load_content(sorted_objects=Helper.getByKey(existing_content, param_key), key=param_key)              
            downloaded_filtred_content = self._filterContent(contents=downloaded_content, key=param_key)

            #Filter new content section         
            existing_content_byKey = Helper.getByKey(existing_content, param_key)    
            if len( Helper.find_differences_in_array(downloaded_filtred_content, existing_content_byKey) ) > 0:
                finalContent = self.file_services_instance.Merge_content(existing_content_byKey, downloaded_filtred_content)               
                self.file_services_instance.Delete_old_files(finalContent)
                self.file_services_instance.Download_missed_photos(finalContent)
                new_content[param_key] = Helper.sort_content_by_date(finalContent, reversed = True)
                changing_exist = True

        if changing_exist:
            self.file_services_instance.Save_content_to_file(final_content, Constants.History_file_name)
            final_content = new_content
        else:
            final_content = existing_content

        self.ctx.set_all_content(final_content)
        return final_content

    def _filterContent(self, contents, key):

        return self.filtering_services_instance.filteringContent(contents=contents,
                                                                            titlePatern=Helper.split_string(self.ctx.get_search_text(key)),
                                                                            isDiscriptionCheck= self.ctx.get_content_filter_checkBox(key) == Constants.CheackBox_enabled_status,
                                                                            discriptionPatern=Helper.split_string(self.ctx.get_content_filter_text(key)),
                                                                            isPriceCheck=self.ctx.get_price_filter_checkbox(key) == Constants.CheackBox_enabled_status,
                                                                            priceRange=[self.ctx.get_price_limit_from(key),
                                                                            self.ctx.get_price_limit_to(key)])

    def _syncContentWithSettings(self, contents_dicts):
        result = {} 
        for key in self.ctx.get_parameter_dicts():       
            if key in contents_dicts:
                result[key] = contents_dicts[key]
        return result

    def _content_is_older_than(self, date_str, days):
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        time_difference = datetime.now(date_object.tzinfo) - date_object
        return time_difference.days > days
    
    def _delete_old_records_in_histry(self, contents, days):
        if contents is None or len(contents) == 0:      
            return None
        for content in contents:  
            date_object = content['creation_date']
            if(self._content_is_older_than(date_object, days)):
                contents.remove(content)
        return contents
    
    def load_content(self, sorted_objects, key):
        if __debug__:
            return self.file_services_instance.Rehidrate_from_file('sample_content.json')
        previos_atempt_sucseed = True

        graberServices_instance = GraberServices()
        self.target_list = self.ctx.get_search_text(key).split(Constants.SearchString_Siparator)    
        #dip_limit = 500
        new_content_array = []
        index = 1        
        while True:
            new_content = []
            if self.ctx.get_search_type(key) == Constants.SearchType.Direct_search:
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
                new_content_reachedLimit = self._content_is_older_than(new_sorted_content[-1]['modification_date'], self.ctx.get_history_digging_days())
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
    
  