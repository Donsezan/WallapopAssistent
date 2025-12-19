import customtkinter
from helper import Helper
from constants import Constants
from Views.confirmationDialog import ConfirmationDialog

class ParamTabView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object
    
    def init(self, root):  
        self.rootFrame = root                   
        self.rootFrame.tabview = customtkinter.CTkTabview(self.rootFrame, fg_color=Constants.Colors.CardBackground, segmented_button_fg_color=Constants.Colors.Background, segmented_button_selected_color=Constants.Colors.Primary, segmented_button_selected_hover_color="#0e9c8b")
        self.rootFrame.tabview.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")       
             
        for param_key in self.ctx.TempParameters.get_dict():
            self.rootFrame.tabview.add(param_key)      
            paramters = self.ctx.TempParameters.get_parameter_byKey(param_key)
            self.create_param_tab(self.rootFrame.tabview.tab(param_key), paramters)

        self.rootFrame.tabview.add("+")            
        self.create_add_tab(self.rootFrame.tabview.tab("+"))

    def create_param_tab(self, tabFrame, paramters):
        tabFrame.search_radio_button_var = customtkinter.IntVar(value=paramters._search_type)
        tabFrame.content_fileter_checkbox_var = customtkinter.StringVar(value=paramters._content_filter_checkBox)       
        tabFrame.price_filter_checkbox_var = customtkinter.StringVar(value=paramters._price_filter_checkbox)      
        tabFrame._search_text = paramters._search_text
        tabFrame._content_filter_text = paramters._content_filter_text
        tabFrame._price_limit_from = paramters._price_limit_from
        tabFrame._price_limit_to = paramters._price_limit_to
        tabFrame._guid = paramters._searchGuid

        price_filter_checkbox_comand = object
        # Clean Grid Layout
        tabFrame.grid_columnconfigure(0, weight=1)
        tabFrame.grid_columnconfigure(1, weight=1)
        
        # --- Search Type Selection ---
        
        type_frame = customtkinter.CTkFrame(tabFrame, fg_color="transparent")
        type_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(20, 10))
        
        tabFrame.search_radio_button_1 = customtkinter.CTkRadioButton(master=type_frame, text="Direct Search", variable=tabFrame.search_radio_button_var, value=Constants.SearchType.Direct_search, fg_color=Constants.Colors.Primary, text_color=Constants.Colors.TextPrimary)
        tabFrame.search_radio_button_1.pack(side="left", padx=(0, 20))
        search_radio_button_2 = customtkinter.CTkRadioButton(master=type_frame, text="History Search", variable=tabFrame.search_radio_button_var, value=Constants.SearchType.History_search, fg_color=Constants.Colors.Primary, text_color=Constants.Colors.TextPrimary)
        search_radio_button_2.pack(side="left")

        # --- Keyword Search ---
        keyword_label = customtkinter.CTkLabel(tabFrame, text="Search Keywords", font=customtkinter.CTkFont(size=12, weight="bold"), text_color=Constants.Colors.TextPrimary)
        keyword_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        
        tabFrame.main_filter_textbox = customtkinter.CTkTextbox(tabFrame, corner_radius=5, height=80, border_width=1, border_color="gray80", fg_color="white", text_color="black")
        tabFrame.main_filter_textbox.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        tabFrame.main_filter_textbox.insert("0.0", tabFrame._search_text)

        # --- Content Filter ---
        content_fileter_checkbox_clomand = lambda: self.content_fileter_checkbox_event(tabFrame)
        tabFrame.content_checkBox = customtkinter.CTkCheckBox(tabFrame, text="Exclude Keywords (Content Filter)", command=content_fileter_checkbox_clomand, variable=tabFrame.content_fileter_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL, fg_color=Constants.Colors.Primary, text_color=Constants.Colors.TextPrimary)
        tabFrame.content_checkBox.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))
        
        tabFrame.content_fileter_textbox = customtkinter.CTkTextbox(tabFrame, corner_radius=5, height=60, border_width=1, border_color="gray80", fg_color="white", text_color="black")
        tabFrame.content_fileter_textbox.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        tabFrame.content_fileter_textbox.insert("0.0", tabFrame._content_filter_text)

        # --- Price Filter ---
        price_filter_checkbox_comand = lambda: self.price_filter_checkbox_event(tabFrame)
        tabFrame.price_filter_checkbox = customtkinter.CTkCheckBox(tabFrame, text="Price Range Filter", command=price_filter_checkbox_comand, variable=tabFrame.price_filter_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL, fg_color=Constants.Colors.Primary, text_color=Constants.Colors.TextPrimary)
        tabFrame.price_filter_checkbox.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        price_limit_frame = customtkinter.CTkFrame(tabFrame, fg_color="transparent")
        price_limit_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        
        tabFrame.price_limit_from_label = customtkinter.CTkLabel(price_limit_frame, text="Min:", font=customtkinter.CTkFont(size=12), text_color=Constants.Colors.TextPrimary)
        tabFrame.price_limit_from_label.pack(side="left", padx=(0, 5))
        
        tabFrame.price_limit_from_textbox = customtkinter.CTkTextbox(price_limit_frame, corner_radius=5, height=28, width=80, border_width=1, border_color="gray80", fg_color="white", text_color="black", activate_scrollbars=False)
        tabFrame.price_limit_from_textbox.pack(side="left")
        tabFrame.price_limit_from_textbox.insert("0.0", tabFrame._price_limit_from)

        tabFrame.price_limit_to_label = customtkinter.CTkLabel(price_limit_frame, text="Max:", font=customtkinter.CTkFont(size=12), text_color=Constants.Colors.TextPrimary)
        tabFrame.price_limit_to_label.pack(side="left", padx=(15, 5))
        
        tabFrame.price_limit_to_textbox = customtkinter.CTkTextbox(price_limit_frame, corner_radius=5, height=28, width=80, border_width=1, border_color="gray80", fg_color="white", text_color="black", activate_scrollbars=False)
        tabFrame.price_limit_to_textbox.pack(side="left")
        tabFrame.price_limit_to_textbox.insert("0.0", tabFrame._price_limit_to)

        # --- Footer (Delete & ID) ---
        footer_frame = customtkinter.CTkFrame(tabFrame, fg_color="transparent")
        footer_frame.grid(row=7, column=0, columnspan=2, sticky="ew", padx=10, pady=20)
        
        tabFrame.guid_label = customtkinter.CTkLabel(footer_frame, text=f"ID: {tabFrame._guid}", font=customtkinter.CTkFont(size=10), text_color="gray60")
        tabFrame.guid_label.pack(side="left")

        delete_button_command = lambda: self.delete_tab()
        self.rootFrame.delete_button = customtkinter.CTkButton(footer_frame, text="Delete Search", width=120, height=30, fg_color=Constants.Colors.TextError, hover_color="#c0392b", command=delete_button_command)
        self.rootFrame.delete_button.pack(side="right")
        
        self.content_fileter_checkbox_event(tabFrame)
        self.price_filter_checkbox_event(tabFrame)
                         
    def delete_tab(self):
        def on_yes():
            tabName = self.rootFrame.tabview.get()
            self.rootFrame.tabview.delete(tabName)
            self.ctx.TempParameters.remove_dict(tabName)
            print ("Tab deleted: "+ tabName)
            
        ConfirmationDialog(title="Delete Search", text="Are you sure you want to delete this search tab?", on_yes=on_yes)

    def create_add_tab(self, tabFrame):
        tabFrame.grid_columnconfigure(0, weight=1)
        
        center_frame = customtkinter.CTkFrame(tabFrame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", padx=20, pady=20)

        label = customtkinter.CTkLabel(center_frame, text="Create New Search Context", font=customtkinter.CTkFont(size=16, weight="bold"), text_color=Constants.Colors.TextPrimary)
        label.pack(pady=(40, 10))

        tabFrame.new_tab_textbox = customtkinter.CTkTextbox(center_frame, corner_radius=5, height=40, width=300, border_width=1, border_color="gray80", fg_color="white", text_color="black")
        tabFrame.new_tab_textbox.pack(pady=10)
        tabFrame.new_tab_textbox.insert("0.0","")  

        create_button_command = lambda: (self.create_new_tab())
        tabFrame.create_button = customtkinter.CTkButton(center_frame, text="Create", width=150, height=40, fg_color=Constants.Colors.Primary, command=create_button_command)
        tabFrame.create_button.pack(pady=20)

    def create_new_tab(self):          
        add_tab = self.rootFrame.tabview.tab("+")
        new_tab_name_raw = add_tab.new_tab_textbox.get("0.0", "end")
        new_tab_name = Helper.remove_newline_symbol(new_tab_name_raw)       
        if not new_tab_name.strip() != '':
           add_tab.new_tab_textbox.configure(border_color = Constants.Colors.TextError)   
           return
        else:
            add_tab.new_tab_textbox.configure(border_color = "gray80")   

        add_tab.new_tab_textbox.delete("1.0", "end")  
        self.rootFrame.tabview.add(new_tab_name)          

        self.ctx.TempParameters.create_dict(new_tab_name)
        parameters = self.ctx.TempParameters.get_parameter_byKey(new_tab_name)
        self.create_param_tab(self.rootFrame.tabview.tab(new_tab_name), parameters)
        self.rootFrame.tabview.set(new_tab_name)

        creat_tab_index = self.rootFrame.tabview.index("+")
        last_tab_index = creat_tab_index+1
        self.rootFrame.tabview.move(last_tab_index, "+")

    def validate_fields(self, tab):
        all_prices_valid = True
        if tab.price_filter_checkbox_var.get() == customtkinter.ACTIVE:
            if not (Helper.validate_int(tab.price_limit_from_textbox) and Helper.validate_int(tab.price_limit_to_textbox)):                    
                all_prices_valid = False 
        return all_prices_valid
   
    def content_fileter_checkbox_event(self, tabFrame):
        if tabFrame.content_fileter_checkbox_var.get() == customtkinter.ACTIVE:
            tabFrame.content_fileter_textbox.configure(state = customtkinter.NORMAL, fg_color="white", text_color="black")   
        else:
            tabFrame.content_fileter_textbox.configure(state = customtkinter.DISABLED, fg_color="gray90", text_color="gray60") 

    def price_filter_checkbox_event(self, tabFrame):
        if tabFrame.price_filter_checkbox_var.get() == customtkinter.ACTIVE:
            tabFrame.price_limit_from_textbox.configure(state = customtkinter.NORMAL, fg_color="white", text_color="black")   
            tabFrame.price_limit_to_textbox.configure(state = customtkinter.NORMAL, fg_color="white", text_color="black")   
        else:
            tabFrame.price_limit_from_textbox.configure(state = customtkinter.DISABLED, fg_color="gray90", text_color="gray60") 
            tabFrame.price_limit_to_textbox.configure(state = customtkinter.DISABLED, fg_color="gray90", text_color="gray60") 

    def save_fileds_to_dict(self, tab, tab_name):
        self.ctx.TempParameters.set_search_type(tab_name, tab.search_radio_button_var.get())
        self.ctx.TempParameters.set_search_text(tab_name, tab.main_filter_textbox.get("0.0", "end"))

        content_fileter_checkbox = tab.content_fileter_checkbox_var.get()
        self.ctx.TempParameters.set_content_filter_checkBox(tab_name, content_fileter_checkbox)
        if content_fileter_checkbox == customtkinter.ACTIVE:
            self.ctx.TempParameters.set_content_filter_text(tab_name, tab.content_fileter_textbox.get("0.0", "end"))

        price_filter_checkbox = tab.price_filter_checkbox_var.get()
        self.ctx.TempParameters.set_price_filter_checkbox(tab_name, price_filter_checkbox)
        if price_filter_checkbox == customtkinter.ACTIVE:
            self.ctx.TempParameters.set_price_limit_from(tab_name, tab.price_limit_from_textbox.get("0.0", "end"))
            self.ctx.TempParameters.set_price_limit_to(tab_name, tab.price_limit_to_textbox.get("0.0", "end"))
   