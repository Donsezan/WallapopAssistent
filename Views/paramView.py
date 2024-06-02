
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
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object 
        self.paramTabView = ParamTabView(self.ctx)       
        self.file_services_instance = FileServices()
        self.is_save_bloked = False
 

    def init(self, root):
        self.rootFrame = root   
        global_padx = 20       
        ### Create and use temp parameter dictionary before save
        self.ctx.TempParameters.overide_dict(self.ctx.MainParameters.get_dict())

        self.auto_refresh_checkbox_var = customtkinter.StringVar(value=self.ctx.TempParameters.get_auto_refresh_checkbox())      
        self.notification_toastup_checkbox_var = customtkinter.StringVar(value=self.ctx.TempParameters.get_notification_toastup_checkbox())
        self.notification_soundnote_checkbox_var = customtkinter.StringVar(value=self.ctx.TempParameters.get_notification_soundnote_checkbox())
        self.rootFrame.grid(row=0, column=1, rowspan=1, sticky="nsew")

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
        self.rootFrame.refresh_time_label = customtkinter.CTkLabel(self.rootFrame, text="Refresh time sec      ", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.refresh_time_label.grid(row=refresh_time_row, column=0, sticky="nsew", padx=global_padx, pady=10, columnspan=1)            
        
        self.rootFrame.refresh_time_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.refresh_time_textbox.grid(row=refresh_time_row, column=1, sticky="nsew",padx=global_padx, pady=10, columnspan=3) 
        self.rootFrame.refresh_time_textbox.insert("0.0", self.ctx.TempParameters.get_refresh_time() )   
       
        #History diggind days row
        history_diggind_days_row = refresh_time_row + 1
        self.rootFrame.history_digging_days_label = customtkinter.CTkLabel(self.rootFrame, text="History digging days ", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.history_digging_days_label.grid(row=history_diggind_days_row, column=0, sticky="nsew", padx=global_padx, pady=10,columnspan=1)            
        
        self.rootFrame.history_digging_days_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.history_digging_days_textbox.grid(row=history_diggind_days_row, column=1, sticky="nsew",padx=global_padx, pady=10, columnspan=3) 
        self.rootFrame.history_digging_days_textbox.insert("0.0", self.ctx.TempParameters.get_history_digging_days() )  

        #Notification toast-up checkbox
        notification_toastup_checkbox_row = history_diggind_days_row + 1
        self.rootFrame.notification_toastup_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Notification toast-up", variable=self.notification_toastup_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.notification_toastup_checkbox.grid(row=notification_toastup_checkbox_row, column=0, sticky="nsew", padx=global_padx, pady=5, columnspan=2)   

        #Notification sound note checkbox
        notification_soundnote_checkbox_row = notification_toastup_checkbox_row + 1
        self.rootFrame.notification_toastup_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Notification sound note", variable=self.notification_soundnote_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.notification_toastup_checkbox.grid(row=notification_soundnote_checkbox_row, column=0, sticky="nsew", padx=global_padx, pady=5, columnspan=2)       

        #Save button
        save_button_row = notification_soundnote_checkbox_row + 1
        self.rootFrame.save_button = customtkinter.CTkButton(self.rootFrame, text="Save", width=30, height=20,  command=self.save_field_event)
        self.rootFrame.save_button.grid(row=save_button_row, column=0, sticky="nsew",padx=global_padx, pady=10, columnspan=4)

        #Call all events to set filds config
        self.auto_refresh_checkbox_event()

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
 
        ### Set back to main content
        self.ctx.MainParameters.overide_dict(self.ctx.TempParameters.get_dict())

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
            self.rootFrame.save_button.configure(fg_color= Constants.Buttons.Button_enable_color, text="Save")  

    def update_values(self):
        if self.auto_refresh_checkbox_var == customtkinter.ACTIVE:
            self.rootFrame.refresh_time_textbox.delete()
            self.rootFrame.refresh_time_textbox.insert("0.0", self.ctx.TempParameters.get_refresh_time())

             




    
