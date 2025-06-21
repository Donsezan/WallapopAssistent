from Services.GraberServices import GraberServices, APIConnectionError
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
           
    def rehydrate_contnet(self, offline_error=False):     
        if offline_error:
            self.ctx.set_offline_error(True)
        if (self.ctx.get_context_rehydrate_state()):
            return
        self.ctx.rehydrate_json(self.file_services_instance.Rehidrate_from_file(Constants.Parameters_file_name))   
        for key, data in  self.ctx.MainParameters.get_dict().items():            
            rehidrated_content = self.file_services_instance.Rehidrate_from_file(Constants.History_file_name(self.ctx.MainParameters.get_SearchGuid(key)))
            if rehidrated_content is None:
                rehidrated_content = []
            # else:
            #     self.ctx.MainParameters.set_content(key, rehidrated_content)    
          
            #content = self.ctx.MainParameters.get_parameter_byKey(key)._content
            content_date = self._delete_old_records_in_history(rehidrated_content, self.ctx.MainParameters.get_history_digging_days())
            content_date_filtred = self._filterContent(content_date, key)
            content_date_filtred_sorted = Helper.sort_content_by_date(content_date_filtred)
            self.ctx.MainParameters.set_content(key, content_date_filtred_sorted)
        self.ctx.set_context_rehydrate_state(True)     
    
    def Download_content(self, force = False):   
        #Start
        changing_exist = []
        if(self.ctx.get_updated_paramter_status() or force):
            for key, data in  self.ctx.MainParameters.get_dict().items():   
                content_filtred = self._filterContent(data._content, key)
                content_filtred_sorted = Helper.sort_content_by_date(content_filtred)
              
                #ToDo Async
                downloaded_content = self.load_content(sorted_objects=content_filtred_sorted, key=key)
                downloaded_content_filtred = self._filterContent(downloaded_content, key)
                
                diff_in_content = Helper.find_differences_in_array(downloaded_content_filtred, content_filtred_sorted)
                if len(diff_in_content) > 0:
                    final_content = self.file_services_instance.Merge_content(content_filtred_sorted, downloaded_content_filtred)
                    self.file_services_instance.Download_missed_photos(final_content)
                    self.file_services_instance.Save_content_to_file(final_content, Constants.History_file_name(data._searchGuid))
                    merged_content = self.file_services_instance.Merge_content(self.ctx.MainParameters.get_content(key), final_content)
                    self.ctx.MainParameters.set_content(key, Helper.sort_content_by_date(merged_content, reversed = True))
                    changing_exist.append(diff_in_content)
            self.ctx.set_updated_paramter_status(False) 

        if any(changing_exist):
            all_content = self.ctx.MainParameters.get_all_content()       
            self.file_services_instance.Delete_old_images(all_content)

        uuids = []
        if len(self.ctx.MainParameters.get_dict()) != 0:            
            uuids = [obj._searchGuid for obj in self.ctx.MainParameters.get_dict().values()]
        self.file_services_instance.Delete_old_historys(uuids)
        return any(changing_exist)

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
    
    def _delete_old_records_in_history(self, contents, days):
        # This method seems to operate on 'creation_date', ensure this field exists or adapt
        filtred_content = []
        if not contents: # More pythonic check for empty list
            return filtred_content
       
        for content_item in contents: # Renamed 'content' to 'content_item' to avoid conflict
            # Ensure 'creation_date' exists in content_item; use 'modified_at' if that's the standard
            unix_date_to_check = content_item.get('modified_at') # Or 'modified_at'
            if unix_date_to_check and not Helper.unix_data_is_older_than(unix_date_to_check, days):
                filtred_content.append(content_item)
        return filtred_content
    
    def load_content(self, sorted_objects, key):
        graberServices_instance = GraberServices()
        search_text = self.ctx.MainParameters.get_search_text(key)
        self.target_list = search_text.split(Constants.SearchString_Siparator)

        new_content_array = []
        api_error_for_any_target = False

        dip_limit_from_params = self.ctx.MainParameters.get_history_digging_days()

        search_type = self.ctx.MainParameters.get_search_type(key)

        try:
            if search_type == Constants.SearchType.Direct_search:
                for target_keyword in self.target_list:
                    # max_results here applies per keyword
                    current_target_content = graberServices_instance.get_all_results_for_keywords(
                        keywords=target_keyword,
                        target_list=None, # For direct search, ParseResults was called with None
                        max_results=dip_limit_from_params
                    )
                    if not current_target_content and not getattr(graberServices_instance, 'search_id', None):
                        print(f"Warning: API call for keyword '{target_keyword}' might have failed or returned no results and no search_id.")
                        api_error_for_any_target = True
                    new_content_array.extend(current_target_content)
            else: # History search type (or any other type)
                # max_results here applies to the whole query
                fetched_content = graberServices_instance.get_all_results_for_keywords(
                    keywords=search_text,
                    target_list=self.target_list, # For history, ParseResults used self.target_list
                    max_results=dip_limit_from_params
                )
                if not fetched_content and not getattr(graberServices_instance, 'search_id', None):
                    print(f"Warning: API call for search_text '{search_text}' might have failed or returned no results and no search_id.")
                    api_error_for_any_target = True
                new_content_array.extend(fetched_content) # Use extend in case future versions return multiple lists

        except APIConnectionError as e:
            print(f"APIConnectionError occurred during content loading for key {key}: {e}")
            api_error_for_any_target = True
            # new_content_array will contain whatever was fetched before the error

        # Deduplicate new_content_array if items might not be unique (e.g. from multiple keyword searches in direct)
        # This requires items to be hashable or a custom deduplication based on ID
        unique_new_items = []
        seen_ids = set()
        for item in new_content_array:
            item_id = item.get('id') # Assuming items have an 'id' field
            if item_id and item_id not in seen_ids:
                unique_new_items.append(item)
                seen_ids.add(item_id)
            elif not item_id: # If no ID, keep it, can't deduplicate
                 unique_new_items.append(item)
        new_content_array = unique_new_items

        # Sort all newly fetched content by modified_at (descending - newest first)
        # This is crucial for the date-based filtering logic that follows.
        if new_content_array:
            # Ensure 'modified_at' is present and valid for sorting
            # Helper.sort_content_by_date might need to handle items missing this key
            new_content_array = Helper.sort_content_by_date(new_content_array, reversed=True)

        final_results_to_return = sorted_objects
        if new_content_array:
            history_digging_days = self.ctx.MainParameters.get_history_digging_days()
            
            # Assuming sorted_objects is already sorted newest first.
            latest_existing_item_date = None
            if sorted_objects and len(sorted_objects) > 0 and 'modified_at' in sorted_objects[0]:
                try:
                    latest_existing_item_date = sorted_objects[0]['modified_at']
                except ValueError:
                     print(f"Warning: Could not parse modified_at for existing item: {sorted_objects[0]['modified_at']}")


            for item in new_content_array:
                try:
                    item_modification_date_str = item['modified_at']
                    if Helper.unix_data_is_older_than(item_modification_date_str, history_digging_days):
                        # Item is older than history_digging_days, so we stop processing further (list is sorted)
                        break

                    if latest_existing_item_date and item_modification_date_str < latest_existing_item_date:
                        # If the item is older than the latest existing item, we can scip it
                        continue

                    final_results_to_return.append(item)
                except ValueError as ve:
                    print(f"Warning: Could not parse modified_at for new item: {item.get('modified_at')}. Error: {ve}")
                    # Decide whether to include items with unparseable dates or skip them
                    # final_results_to_return.append(item) # Option to include        
        return final_results_to_return
  