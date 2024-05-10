
import sys
import os
import customtkinter

from Views.baseView import BaseView
from Views.paramTabView import ParamTabView
from Services.FileServices import FileServices


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from constants import Constants

class ParamView(BaseView):
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object 
        self.paramTabView = ParamTabView(self.ctx)       
        self.file_services_instance = FileServices()
 

    def init(self, root):
        self.rootFrame = root   
        global_padx = 20

        self.auto_refresh_checkbox_var = customtkinter.StringVar(value=self.ctx.get_auto_refresh_checkbox())      
        self.notification_toastup_checkbox_var = customtkinter.StringVar(value=self.ctx.get_notification_toastup_checkbox())
        self.notification_soundnote_checkbox_var = customtkinter.StringVar(value=self.ctx.get_notification_soundnote_checkbox())
        self.rootFrame.grid(row=0, column=1, rowspan=1, sticky="nsew")

        self.rootFrame.columnconfigure(1, weight=0)
        self.rootFrame.columnconfigure(2, weight=1)
        self.rootFrame.columnconfigure(3, weight=0)
        self.rootFrame.columnconfigure(2, weight=1)

        self.paramTabView.init(self.rootFrame)

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
        self.rootFrame.refresh_time_textbox.insert("0.0", self.ctx.get_refresh_time() )   
       
        #History diggind days row
        history_diggind_days_row = refresh_time_row + 1
        self.rootFrame.history_digging_days_label = customtkinter.CTkLabel(self.rootFrame, text="History digging days ", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.history_digging_days_label.grid(row=history_diggind_days_row, column=0, sticky="nsew", padx=global_padx, pady=10,columnspan=1)            
        
        self.rootFrame.history_digging_days_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.history_digging_days_textbox.grid(row=history_diggind_days_row, column=1, sticky="nsew",padx=global_padx, pady=10, columnspan=3) 
        self.rootFrame.history_digging_days_textbox.insert("0.0", self.ctx.get_history_digging_days() )  

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

    def save_field_event(self):
        if not self.is_valid_digit_fields():
            return

        self.ctx.set_search_type(self.search_radio_button_var.get())
        self.ctx.set_search_text(self.rootFrame.main_filter_textbox.get("0.0", "end"))
        self.ctx.set_content_filter_checkBox(self.content_fileter_checkbox_var.get())
        if self.content_fileter_checkbox_var.get() == customtkinter.ACTIVE:
            self.ctx.set_content_filter_text(self.rootFrame.content_fileter_textbox.get("0.0", "end"))
        
        self.ctx.set_price_filter_checkbox(self.price_filter_checkbox_var.get())
        if self.price_filter_checkbox_var.get() == customtkinter.ACTIVE:
            self.ctx.set_price_limit_from(self.rootFrame.price_limit_from_textbox.get("0.0", "end"))
            self.ctx.set_price_limit_to(self.rootFrame.price_limit_to_textbox.get("0.0", "end"))

        self.ctx.set_auto_refresh_checkbox(self.auto_refresh_checkbox_var.get())
        if self.auto_refresh_checkbox_var.get() == customtkinter.ACTIVE:
            self.ctx.set_refresh_time(self.rootFrame.refresh_time_textbox.get("0.0", "end"))
              
        self.ctx.set_history_digging_days(self.rootFrame.history_digging_days_textbox.get("0.0", "end"))
        self.ctx.set_notification_toastup_checkbox(self.notification_toastup_checkbox_var.get())
        self.ctx.set_notification_soundnote_checkbox(self.notification_soundnote_checkbox_var.get())                 
        self.ctx.set_updated_paramter_status(True)
      
        print("set_search_type:", self.ctx.get_search_type())
        print("search_text:", self.ctx.get_search_text())
        print("content_filter_checBox:", self.ctx.get_content_filter_checkBox())
        print("content_filter_text:", self.ctx.get_content_filter_text())        
        print("price_filter_checkbox_var:", self.ctx.get_price_filter_checkbox())
        print("price_limit_from:", self.ctx.get_price_limit_from())
        print("price_limit_to:", self.ctx.get_price_limit_to())
        print("set_history_digging_days:", self.ctx.get_history_digging_days())
        print("notification_toastup_checkbox:", self.ctx.get_notification_toastup_checkbox())
        print("notification_soundnote_checkbox:", self.ctx.get_notification_soundnote_checkbox())        
        print("auto_refresh_checkbox:", self.ctx.get_auto_refresh_checkbox())        
        print("set_refresh_time:", self.ctx.get_refresh_time())
        self.file_services_instance.Save_content_to_file(self.ctx.to_json(), Constants.Parameters_file_name)
       
    def auto_refresh_checkbox_event(self):
        if self.auto_refresh_checkbox_var.get() == customtkinter.ACTIVE:
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("auto_refresh_checkbox_event: ", customtkinter.ACTIVE)
        else:
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("auto_refresh_checkbox_event: ", customtkinter.NORMAL)
    
    def is_valid_digit_fields(self):
        # if self.price_filter_checkbox_var.get() == customtkinter.NORMAL:
        #     if not (self.validate_int(self.rootFrame.price_limit_from_textbox) and self.validate_int(self.rootFrame.price_limit_to_textbox)):
        #         return False        
        if not self.validate_int(self.rootFrame.refresh_time_textbox):
            return False        
        return True
    
        



    
