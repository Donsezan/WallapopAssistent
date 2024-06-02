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
            return
        self.ctx.rehydrate_json(self.file_services_instance.Rehidrate_from_file(Constants.Parameters_file_name))   
        for key, data in  self.ctx.MainParameters.get_dict().items():            
            rehidrated_content = self.file_services_instance.Rehidrate_from_file(Constants.History_file_name(self.ctx.MainParameters.get_SearchGuid(key)))
            if rehidrated_content is None:
                rehidrated_content = []
            # self.ctx.MainParameters.set_content(key, rehidrated_content)          
            content = self.ctx.MainParameters.get_parameter_byKey(key)._content
            content_date = self._delete_old_records_in_histry(content, self.ctx.MainParameters.get_history_digging_days())
            content_date_filtred = self._filterContent(content_date, key)
            content_date_filtred_sorted = Helper.sort_content_by_date(content_date_filtred)
            self.ctx.MainParameters.set_content(key, content_date_filtred_sorted)
        self.ctx.set_context_rehydrate_state(True)     
    
    def Download_content(self):   
        #Start
        changing_exist = []
        if(self.ctx.get_updated_paramter_status()):
            for key, data in  self.ctx.MainParameters.get_dict().items():   
                content_filtred = self._filterContent(data._content, key)
                content_filtred_sorted = Helper.sort_content_by_date(content_filtred)
              
                #ToDoAsync
                downloaded_content = self.load_content(sorted_objects=content_filtred_sorted, key=key)
                downloaded_content_filtred = self._filterContent(downloaded_content, key)
                
                if len( Helper.find_differences_in_array(downloaded_content_filtred, content_filtred_sorted) ) > 0:
                    final_content = self.file_services_instance.Merge_content(content_filtred_sorted, downloaded_content_filtred)
                    self.file_services_instance.Download_missed_photos(final_content)
                    self.file_services_instance.Save_content_to_file(final_content, Constants.History_file_name(data._searchGuid))
                    merged_content = self.file_services_instance.Merge_content(self.ctx.MainParameters.get_content(key), final_content)
                    self.ctx.MainParameters.set_content(key, Helper.sort_content_by_date(merged_content, reversed = True))
                    changing_exist.append(True)
            self.ctx.set_updated_paramter_status(False) 

        if any(changing_exist):
            all_content = self.ctx.MainParameters.get_all_content()       
            self.file_services_instance.Delete_old_images(all_content)

        uuids = []
        if len(self.ctx.MainParameters.get_dict()) != 0:            
            uuids = [obj._searchGuid for obj in self.ctx.MainParameters.get_dict().values()]
        self.file_services_instance.Delete_old_historys(uuids)

    def _filterContent(self, contents, key):

        return self.filtering_services_instance.filteringContent(contents=contents,
                                                                            titlePatern=Helper.split_string(self.ctx.MainParameters.get_search_text(key)),
                                                                            isDiscriptionCheck= self.ctx.MainParameters.get_content_filter_checkBox(key) == Constants.CheackBox_enabled_status,
                                                                            discriptionPatern=Helper.split_string(self.ctx.MainParameters.get_content_filter_text(key)),
                                                                            isPriceCheck=self.ctx.MainParameters.get_price_filter_checkbox(key) == Constants.CheackBox_enabled_status,
                                                                            priceRange=[self.ctx.MainParameters.get_price_limit_from(key),
                                                                            self.ctx.MainParameters.get_price_limit_to(key)])

    def _syncContentWithSettings(self, contents_dicts):
        result = {} 
        for key, data in self.ctx.MainParameters.get_dict().items():       
            if key in contents_dicts:
                result[key] = contents_dicts[key]
        return result

    def _content_is_older_than(self, date_str, days):
        date_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        time_difference = datetime.now(date_object.tzinfo) - date_object
        return time_difference.days > days
    
    def _delete_old_records_in_histry(self, contents, days):
        filtred_content = []
        if len(contents) == 0:
            return filtred_content
       
        for content in contents:
            date_object = content['creation_date']
            if(not self._content_is_older_than(date_object, days)):
                filtred_content.append(content)
        return filtred_content
    
    def load_content(self, sorted_objects, key):
        if __debug__:
            return self.file_services_instance.Rehidrate_from_file('Sample-History.json')
        previos_atempt_sucseed = True

        graberServices_instance = GraberServices()
        self.target_list = self.ctx.MainParameters.get_search_text(key).split(Constants.SearchString_Siparator)    
        #dip_limit = 500
        new_content_array = []
        index = 1        
        while True:
            new_content = []
            if self.ctx.MainParameters.get_search_type(key) == Constants.SearchType.Direct_search:
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
                new_content_reachedLimit = self._content_is_older_than(new_sorted_content[-1]['modification_date'], self.ctx.MainParameters.get_history_digging_days())
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
    
  