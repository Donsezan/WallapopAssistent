
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

        # Main Layout Configuration
        self.rootFrame.grid_columnconfigure(0, weight=1)
        self.rootFrame.grid_rowconfigure(0, weight=0) # Title / Header
        self.rootFrame.grid_rowconfigure(1, weight=0) # General Settings
        self.rootFrame.grid_rowconfigure(2, weight=1) # TabView (Search Settings)
        self.rootFrame.grid_rowconfigure(3, weight=0) # Save Button

        # --- Header ---
        header_label = customtkinter.CTkLabel(self.rootFrame, text="Settings", font=customtkinter.CTkFont(size=24, weight="bold"), text_color=Constants.Colors.TextPrimary)
        header_label.grid(row=0, column=0, padx=global_padx, pady=(20, 10), sticky="w")

        # --- General Settings Frame ---
        general_settings_frame = customtkinter.CTkFrame(self.rootFrame, fg_color=Constants.Colors.CardBackground, corner_radius=10)
        general_settings_frame.grid(row=1, column=0, padx=global_padx, pady=10, sticky="ew")
        
        general_settings_frame.grid_columnconfigure(0, weight=1)
        general_settings_frame.grid_columnconfigure(1, weight=1)

        # Left Column: Checkboxes
        left_col_frame = customtkinter.CTkFrame(general_settings_frame, fg_color="transparent")
        left_col_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.rootFrame.auto_refresh_checkbox = customtkinter.CTkCheckBox(left_col_frame, text="Auto Refresh", 
                                                                         command=self.auto_refresh_checkbox_event, 
                                                                         variable=self.auto_refresh_checkbox_var, 
                                                                         onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL,
                                                                         fg_color=Constants.Colors.Primary, text_color=Constants.Colors.TextPrimary)
        self.rootFrame.auto_refresh_checkbox.pack(anchor="w", pady=5)

        self.rootFrame.notification_toastup_checkbox = customtkinter.CTkCheckBox(left_col_frame, text="Show Toast Notifications", 
                                                                                 variable=self.notification_toastup_checkbox_var, 
                                                                                 onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL,
                                                                                 fg_color=Constants.Colors.Primary, text_color=Constants.Colors.TextPrimary)
        self.rootFrame.notification_toastup_checkbox.pack(anchor="w", pady=5)

        self.rootFrame.notification_soundnote_checkbox = customtkinter.CTkCheckBox(left_col_frame, text="Play Notification Sound", 
                                                                                   variable=self.notification_soundnote_checkbox_var, 
                                                                                   onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL,
                                                                                   fg_color=Constants.Colors.Primary, text_color=Constants.Colors.TextPrimary)
        self.rootFrame.notification_soundnote_checkbox.pack(anchor="w", pady=5)

        # Right Column: Numeric Inputs
        right_col_frame = customtkinter.CTkFrame(general_settings_frame, fg_color="transparent")
        right_col_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Refresh Time
        self.rootFrame.refresh_time_label = customtkinter.CTkLabel(right_col_frame, text="Refresh Interval (sec):", font=customtkinter.CTkFont(size=12), text_color=Constants.Colors.TextSecondary)    
        self.rootFrame.refresh_time_label.pack(anchor="w")
        self.rootFrame.refresh_time_textbox = customtkinter.CTkTextbox(right_col_frame, corner_radius=5, height=28, width=200, activate_scrollbars=False, border_width=1, border_color="gray80", fg_color="white", text_color="black")
        self.rootFrame.refresh_time_textbox.pack(anchor="w", pady=(0, 10))
        self.rootFrame.refresh_time_textbox.insert("0.0", self.ctx.TempParameters.get_refresh_time() )   

        # History Days
        self.rootFrame.history_digging_days_label = customtkinter.CTkLabel(right_col_frame, text="History Retention (days):", font=customtkinter.CTkFont(size=12), text_color=Constants.Colors.TextSecondary)    
        self.rootFrame.history_digging_days_label.pack(anchor="w")
        self.rootFrame.history_digging_days_textbox = customtkinter.CTkTextbox(right_col_frame, corner_radius=5, height=28, width=200, activate_scrollbars=False, border_width=1, border_color="gray80", fg_color="white", text_color="black")
        self.rootFrame.history_digging_days_textbox.pack(anchor="w")
        self.rootFrame.history_digging_days_textbox.insert("0.0", self.ctx.TempParameters.get_history_digging_days() )  

        # --- Tab View Wrapper ---
        # ParamTabView will attach itself to a container so we can control grid placement better
        tab_view_container = customtkinter.CTkFrame(self.rootFrame, fg_color="transparent")
        tab_view_container.grid(row=2, column=0, sticky="nsew", padx=global_padx, pady=10)
        
        tab_view_container.grid_columnconfigure(0, weight=1)
        tab_view_container.grid_rowconfigure(0, weight=1)
        
        # We need to hack ParamTabView slightly or just let it use the container as 'root' if it supports it.
        # ParamTabView.init expects 'root' and tries to create 'root.tabview'.
        # Let's pass 'tab_view_container' as root.
        self.paramTabView.init(tab_view_container)

        # --- Save Button ---
        self.rootFrame.save_button = customtkinter.CTkButton(self.rootFrame, text="Save Changes", width=200, height=45, 
                                                             fg_color=Constants.Buttons.Button_enable_color, 
                                                             font=customtkinter.CTkFont(size=15, weight="bold"),
                                                             command=self.save_field_event)
        self.rootFrame.save_button.grid(row=3, column=0, sticky="ew", padx=global_padx, pady=20)


        #Call all events to set filds config
        self.auto_refresh_checkbox_event()
        
        self.is_initialized = True

    def save_field_event(self):
        # We passed 'tab_view_container' as root to paramTabView, so tabview is attached to that.
        # But we need access to it. paramTabView attaches 'tabview' to the root we passed.
        # However, self.paramTabView.rootFrame became the container.
        
        # Accessing tabview via the container we created:
        # Since I didn't save the container to self, I should probably rely on self.paramTabView.rootFrame.
        tabs = self.paramTabView.rootFrame.tabview 
        
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
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.NORMAL, fg_color="white", text_color="black")   
            print("auto_refresh_checkbox_event: ", customtkinter.ACTIVE)
        else:
            self.rootFrame.refresh_time_textbox.configure(state = customtkinter.DISABLED, fg_color="gray90", text_color="gray60") 
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
            self.rootFrame.save_button.configure(fg_color= Constants.Buttons.Button_restricted_color, text="Save is blocked: Invalid fields (Check red highlighted inputs)")  
        else:
            self.is_save_bloked = False    
            self.rootFrame.save_button.configure(fg_color= Constants.Buttons.Button_enable_color, text="Save Changes")  

    def update_values(self):
        # Update UI with current values from params
        pass



    
