import customtkinter
import sys
import os
from Services.FileServices import FileServices
from helper import Helper

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from constants import Constants

class ParamView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object        
        self.file_services_instance = FileServices()

    def init(self, root):
        self.rootFrame = root   
        self.search_radio_button_var = customtkinter.IntVar(value=self.ctx.get_search_type())
        self.content_fileter_checkbox_var = customtkinter.StringVar(value=self.ctx.get_content_filter_checkBox())       
        self.price_filter_checkbox_var = customtkinter.StringVar(value=self.ctx.get_price_filter_checkbox())      
        self.auto_refresh_checkbox_var = customtkinter.StringVar(value=self.ctx.get_auto_refresh_checkbox())      
        self.notification_toastup_checkbox_var = customtkinter.StringVar(value=self.ctx.get_notification_toastup_checkbox())
        self.notification_soundnote_checkbox_var = customtkinter.StringVar(value=self.ctx.get_notification_soundnote_checkbox())
        self.rootFrame.grid(row=0, column=1, rowspan=1, sticky="nsew")

        self.rootFrame.columnconfigure(1, weight=0)
        self.rootFrame.columnconfigure(2, weight=1)
        self.rootFrame.columnconfigure(3, weight=0)
        self.rootFrame.columnconfigure(2, weight=1)
              
        #Search radio button group
        search_radio_button_group_row = 0

        self.radiobutton_frame = customtkinter.CTkFrame(self.rootFrame)
        self.radiobutton_frame.grid(row=search_radio_button_group_row, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew", columnspan=4)

        self.search_radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Direct search", variable=self.search_radio_button_var, value=Constants.SearchType.Direct_search)
        self.search_radio_button_1.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        self.search_radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="History search", variable=self.search_radio_button_var, value=Constants.SearchType.History_search)
        self.search_radio_button_2.grid(row=0, column=1, pady=10, padx=20, sticky="nsew")
        self.radiobutton_frame.grid_columnconfigure(0, weight=1)
        self.radiobutton_frame.grid_columnconfigure(1, weight=1)

        #Main filter row
        main_filter_row = 1

        self.rootFrame.main_filter_label = customtkinter.CTkLabel(self.rootFrame, text="Filter", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"))    
        self.rootFrame.main_filter_label.grid(row=main_filter_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=1)            
        
        self.rootFrame.main_filter_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False)
        self.rootFrame.main_filter_textbox.grid(row=main_filter_row, column=1, sticky="nsew",padx=5, pady=5, columnspan=3)              
        self.rootFrame.main_filter_textbox.insert("0.0", self.ctx.get_search_text())
    
        #Content filters checkbox
        content_checkBox_row = 2
        self.rootFrame.content_checkBox = customtkinter.CTkCheckBox(self.rootFrame, text="Content filter", command=self.content_fileter_checkbox_event, variable=self.content_fileter_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.content_checkBox.grid(row=content_checkBox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)        
        
        #Content filters row
        content_fileter_row = 3
        self.rootFrame.content_fileter_label = customtkinter.CTkLabel(self.rootFrame, text="Content filter", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"))    
        self.rootFrame.content_fileter_label.grid(row=content_fileter_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=1)            
        
        self.rootFrame.content_fileter_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.content_fileter_textbox.grid(row=content_fileter_row, column=1, sticky="nsew",padx=5, pady=5, columnspan=3)              
        self.rootFrame.content_fileter_textbox.insert("0.0", self.ctx.get_content_filter_text() )      

        #Price filter checkbox
        price_filter_checkbox_row = 4
        self.rootFrame.price_filter_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Price filter", command=self.price_filter_checkbox_event, variable=self.price_filter_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.price_filter_checkbox.grid(row=price_filter_checkbox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)         

        #Price limit
        price_limit_row = 5
        self.rootFrame.price_limit_from_label = customtkinter.CTkLabel(self.rootFrame, text="Price From", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"))    
        self.rootFrame.price_limit_from_label.grid(row=price_limit_row, column=0, sticky="nsew", padx=5, pady=5)            
        
        self.rootFrame.price_limit_from_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False, width=80)
        self.rootFrame.price_limit_from_textbox.grid(row=price_limit_row, column=1, sticky="nsew",padx=5, pady=5)              
        self.rootFrame.price_limit_from_textbox.insert("0.0", self.ctx.get_price_limit_from() )

        self.rootFrame.price_limit_to_label = customtkinter.CTkLabel(self.rootFrame, text="To", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"), width=20 )    
        self.rootFrame.price_limit_to_label.grid(row=price_limit_row, column=2, sticky="nsew", padx=5, pady=5)    

        self.rootFrame.price_limit_to_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False  )
        self.rootFrame.price_limit_to_textbox.grid(row=price_limit_row, column=3, sticky="nsew",padx=5, pady=5)              
        self.rootFrame.price_limit_to_textbox.insert("0.0", self.ctx.get_price_limit_to() )
        self.price_filter_checkbox_event()

        #Auto refresh checkbox
        auto_refresh_checkbox_row = 6
        self.rootFrame.auto_refresh_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Auto refresh", command=self.auto_refresh_checkbox_event, variable=self.auto_refresh_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.auto_refresh_checkbox.grid(row=auto_refresh_checkbox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)   
       
        #Refresh time row
        refresh_time_row = 7
        self.rootFrame.refresh_time_label = customtkinter.CTkLabel(self.rootFrame, text="Refresh time sec", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.refresh_time_label.grid(row=refresh_time_row, column=0, sticky="nsew", padx=10, pady=10,columnspan=1)            
        
        self.rootFrame.refresh_time_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.refresh_time_textbox.grid(row=refresh_time_row, column=1, sticky="nsew",padx=10, pady=10, columnspan=3) 
        self.rootFrame.refresh_time_textbox.insert("0.0", self.ctx.get_refresh_time() )   
       
        #History diggind days row
        history_diggind_days_row = 8
        self.rootFrame.history_digging_days_label = customtkinter.CTkLabel(self.rootFrame, text="History digging days", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.history_digging_days_label.grid(row=history_diggind_days_row, column=0, sticky="nsew", padx=10, pady=10,columnspan=1)            
        
        self.rootFrame.history_digging_days_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.history_digging_days_textbox.grid(row=history_diggind_days_row, column=1, sticky="nsew",padx=10, pady=10, columnspan=3) 
        self.rootFrame.history_digging_days_textbox.insert("0.0", self.ctx.get_history_digging_days() )  

        #Notification toast-up checkbox
        notification_toastup_checkbox_row = 9
        self.rootFrame.notification_toastup_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Notification toast-up", variable=self.notification_toastup_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.notification_toastup_checkbox.grid(row=notification_toastup_checkbox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)   

        #Notification sound note checkbox
        notification_soundnote_checkbox_row = 10
        self.rootFrame.notification_toastup_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Notification sound note", variable=self.notification_soundnote_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        self.rootFrame.notification_toastup_checkbox.grid(row=notification_soundnote_checkbox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)       

        #Save button
        save_button_row = 11
        self.rootFrame.save_button = customtkinter.CTkButton(self.rootFrame, text="Save", width=30, height=20,  command=self.save_field_event)
        self.rootFrame.save_button.grid(row=save_button_row, column=0, sticky="nsew",padx=10, pady=10, columnspan=4)

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

    def content_fileter_checkbox_event(self):
        if self.content_fileter_checkbox_var.get() == customtkinter.ACTIVE:
            self.rootFrame.content_fileter_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("content_fileter_checkbox_event: ", customtkinter.ACTIVE)
        else:
            self.rootFrame.content_fileter_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("content_fileter_checkbox_event: ", customtkinter.NORMAL)

            
    def auto_refresh_checkbox_event(self):
        if self.auto_refresh_checkbox_var.get() == customtkinter.ACTIVE:
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("auto_refresh_checkbox_event: ", customtkinter.ACTIVE)
        else:
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("auto_refresh_checkbox_event: ", customtkinter.NORMAL)

    def price_filter_checkbox_event(self):
        if self.price_filter_checkbox_var.get() == customtkinter.ACTIVE:
            self.rootFrame.price_limit_from_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            self.rootFrame.price_limit_to_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("price_filter_checkbox_event: ", customtkinter.ACTIVE)
        else:
            self.rootFrame.price_limit_from_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            self.rootFrame.price_limit_to_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("price_filter_checkbox_event: ", customtkinter.NORMAL)
    
    def validate_int(self, textbox):
        value = Helper.remove_newline_symbol(textbox.get("0.0", "end"))
        print(textbox.cget("fg_color"))
        if value.isdigit():
            textbox.configure(state = customtkinter.NORMAL, fg_color= ['#F9F9FA', '#1D1E1E'])   
            return True
        else:       
            textbox.configure(state = customtkinter.NORMAL, fg_color= "red")   
            return False
        
    def is_valid_digit_fields(self):
        if self.price_filter_checkbox_var.get() == customtkinter.NORMAL:
            if not (self.validate_int(self.rootFrame.price_limit_from_textbox) and self.validate_int(self.rootFrame.price_limit_to_textbox)):
                return False
        
        if not self.validate_int(self.rootFrame.refresh_time_textbox):
            return False
        
        return True
                
                         


    
