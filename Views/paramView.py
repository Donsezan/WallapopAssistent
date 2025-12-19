
import sys
import os
import customtkinter
from helper import Helper
from Views.paramTabView import ParamTabView
from Services.FileServices import FileServices


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from constants import Constants

class ParamView():
    def __init__(self, ctx, main_logic):
        self.ctx = ctx
        self.main_logic = main_logic
        self.rootFrame = object 
        self.paramTabView = ParamTabView(self.ctx)       
        self.file_services_instance = FileServices()
        self.is_save_bloked = False
        self.is_initialized = False
 

    def init(self, root):
        self.rootFrame = root
        
        # Ensure the frame is visible (it might have been hidden by grid_forget)
        self.rootFrame.grid(row=0, column=1, rowspan=1, sticky="nsew")

        # Performance Fix: Only initialize widgets once
        if self.is_initialized:
            self.update_values()
            return
            
        global_padx = 20       
        ### Create and use temp parameter dictionary before save
        self.ctx.TempParameters = self.ctx.MainParameters

        self.auto_refresh_checkbox_var = customtkinter.StringVar(value=self.ctx.TempParameters.get_auto_refresh_checkbox())      
        self.notification_toastup_checkbox_var = customtkinter.StringVar(value=self.ctx.TempParameters.get_notification_toastup_checkbox())
        self.notification_soundnote_checkbox_var = customtkinter.StringVar(value=self.ctx.TempParameters.get_notification_soundnote_checkbox())

        self.rootFrame.columnconfigure(1, weight=0)
        self.rootFrame.columnconfigure(2, weight=1)
        self.rootFrame.columnconfigure(3, weight=0)
        self.rootFrame.columnconfigure(2, weight=1)

        self.paramTabView.init(self.rootFrame)
        self.update_values()

        #Auto refresh checkbox
        auto_refresh_checkbox_row = 7
        self.rootFrame.auto_refresh_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Auto refresh", command=self.auto_refresh_checkbox_event, variable=self.auto_refresh_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.auto_refresh_checkbox.grid(row=auto_refresh_checkbox_row, column=0, sticky="nsew", padx=global_padx, pady=5, columnspan=2)   
       
        #Refresh time row
        refresh_time_row = auto_refresh_checkbox_row + 1
        self.rootFrame.refresh_time_label = customtkinter.CTkLabel(self.rootFrame, text="Refresh time (sec)", compound="left", height=20, font=customtkinter.CTkFont(size=14))    
        self.rootFrame.refresh_time_label.grid(row=refresh_time_row, column=0, sticky="w", padx=global_padx, pady=10, columnspan=1)            
        
        self.rootFrame.refresh_time_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=5, height=28, activate_scrollbars= False )
        self.rootFrame.refresh_time_textbox.grid(row=refresh_time_row, column=1, sticky="ew",padx=global_padx, pady=10, columnspan=3) 
        self.rootFrame.refresh_time_textbox.insert("0.0", self.ctx.TempParameters.get_refresh_time() )   
       
        #History digging days row
        history_diggind_days_row = refresh_time_row + 1
        self.rootFrame.history_digging_days_label = customtkinter.CTkLabel(self.rootFrame, text="History retention (days)", compound="left", height=20, font=customtkinter.CTkFont(size=14))    
        self.rootFrame.history_digging_days_label.grid(row=history_diggind_days_row, column=0, sticky="w", padx=global_padx, pady=10,columnspan=1)            
        
        self.rootFrame.history_digging_days_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=5, height=28, activate_scrollbars= False )
        self.rootFrame.history_digging_days_textbox.grid(row=history_diggind_days_row, column=1, sticky="ew",padx=global_padx, pady=10, columnspan=3) 
        self.rootFrame.history_digging_days_textbox.insert("0.0", self.ctx.TempParameters.get_history_digging_days() )  

        #Notification toast-up checkbox
        notification_toastup_checkbox_row = history_diggind_days_row + 1
        self.rootFrame.notification_toastup_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Show toast notifications", variable=self.notification_toastup_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.notification_toastup_checkbox.grid(row=notification_toastup_checkbox_row, column=0, sticky="nsew", padx=global_padx, pady=5, columnspan=2)   

        #Notification sound note checkbox
        notification_soundnote_checkbox_row = notification_toastup_checkbox_row + 1
        self.rootFrame.notification_soundnote_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Play sound on notification", variable=self.notification_soundnote_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.notification_soundnote_checkbox.grid(row=notification_soundnote_checkbox_row, column=0, sticky="nsew", padx=global_padx, pady=5, columnspan=2)       

        #Save button
        save_button_row = notification_soundnote_checkbox_row + 1
        self.rootFrame.save_button = customtkinter.CTkButton(self.rootFrame, text="Save Changes", width=30, height=35, fg_color=Constants.Buttons.Button_enable_color, command=self.save_field_event)
        self.rootFrame.save_button.grid(row=save_button_row, column=0, sticky="ew",padx=global_padx, pady=20, columnspan=4)

        #Call all events to set filds config
        self.auto_refresh_checkbox_event()
        
        self.is_initialized = True

    def save_field_event(self):
        tabs = self.rootFrame.tabview
        price_fields_valid = []
        for name, data in tabs._tab_dict.items():            
            if name == '+':
                continue
            result = self.paramTabView.validate_fields(data)
            price_fields_valid.append(result)
            print("Tab: "+ name +" price field is valid: " + str(result))
        price_fields_valid.extend(self.is_valid_refreshTime_digintTime())
        if not all(price_fields_valid): 
            self.block_save_button(True)       
            return
        else:
            self.block_save_button(False)       
        
        for name, data in tabs._tab_dict.items():
            if name == '+':
                continue
            self.paramTabView.save_fileds_to_dict(tabs.tab(name), name)

        auto_refresh_checkbox = self.auto_refresh_checkbox_var.get()
        self.ctx.TempParameters.set_auto_refresh_checkbox(auto_refresh_checkbox)
        if auto_refresh_checkbox == customtkinter.ACTIVE:
            self.ctx.TempParameters.set_refresh_time(self.rootFrame.refresh_time_textbox.get("0.0", "end"))
              
        self.ctx.TempParameters.set_history_digging_days(self.rootFrame.history_digging_days_textbox.get("0.0", "end"))
        self.ctx.TempParameters.set_notification_toastup_checkbox(self.notification_toastup_checkbox_var.get())
        self.ctx.TempParameters.set_notification_soundnote_checkbox(self.notification_soundnote_checkbox_var.get())                 
        self.ctx.set_updated_paramter_status(True)
 
        #TODO update content       

        if(self.ctx.get_updated_paramter_status()):
            for key, data in  self.ctx.TempParameters.get_dict().items():   
                content_filtred =  self.main_logic._filterContent(data._content, key)
                self.ctx.TempParameters.set_content(key, content_filtred)
        
        ### Set back to main content
        self.ctx.MainParameters = self.ctx.TempParameters
        self.file_services_instance.Save_content_to_file(self.ctx.to_json(), Constants.Parameters_file_name)
       
    def auto_refresh_checkbox_event(self):
        if self.auto_refresh_checkbox_var.get() == customtkinter.ACTIVE:
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("auto_refresh_checkbox_event: ", customtkinter.ACTIVE)
        else:
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("auto_refresh_checkbox_event: ", customtkinter.NORMAL)
    
    def is_valid_refreshTime_digintTime(self):
        result = []
        if self.auto_refresh_checkbox_var.get() == customtkinter.ACTIVE:
           result.append(Helper.validate_int(self.rootFrame.refresh_time_textbox))     
        result.append(Helper.validate_int(self.rootFrame.history_digging_days_textbox))
        return result
    
    def block_save_button(self, is_blocked):
        if self.is_save_bloked == is_blocked:
            return
        if is_blocked:
            self.is_save_bloked = True    
            self.rootFrame.save_button.configure(fg_color= Constants.Buttons.Button_restricted_color, text="Save is blocked: Invalid fields")  
        else:
            self.is_save_bloked = False    
            self.rootFrame.save_button.configure(fg_color= Constants.Buttons.Button_enable_color, text="Save Changes")  

    def update_values(self):
        # Update UI with current values from params
        if hasattr(self, 'rootFrame') and hasattr(self.rootFrame, 'refresh_time_textbox'):
             if self.ctx.TempParameters:
                 # Checkbox needs to be updated too if the model changed externally or reloaded (not common here but safe)
                 pass



    
