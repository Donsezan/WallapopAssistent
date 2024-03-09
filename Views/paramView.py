import customtkinter

class ParamView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object        

    def init(self, root):
        self.rootFrame = root   
        print(self.ctx.get_content_search_checkBox())
        self.content_fileter_checkbox_var = customtkinter.StringVar(value=self.ctx.get_content_search_checkBox())
        self.price_filter_checkbox_var = customtkinter.StringVar(value=self.ctx.get_price_filter_checkbox())

        self.rootFrame.grid(row=0, column=1, rowspan=1, sticky="nsew")
        self.rootFrame.columnconfigure(1, weight=60, uniform="columns")
              
        #Main filter row
        main_filter_row = 0
        self.rootFrame.main_filter_label = customtkinter.CTkLabel(self.rootFrame, text="Filter", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.main_filter_label.grid(row=main_filter_row, column=0, sticky="nsew", padx=10, pady=10)            
        
        self.rootFrame.main_filter_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False)
        self.rootFrame.main_filter_textbox.grid(row=main_filter_row, column=1, sticky="nsew",padx=10, pady=10)              
        self.rootFrame.main_filter_textbox.insert("0.0", self.ctx.get_search_text())

        self.rootFrame.main_filter_button = customtkinter.CTkButton(self.rootFrame, text="Save", width=30, height=20,  command=self.linkField_event)
        self.rootFrame.main_filter_button.grid(row=main_filter_row, column=2, sticky="nsew",padx=10, pady=10)
    
        #Content filters checkbox
        content_checkBox_row = 1
        self.rootFrame.content_checkBox = customtkinter.CTkCheckBox(self.rootFrame, text="Content filter checkbox", command=self.content_fileter_checkbox_event, variable=self.content_fileter_checkbox_var, onvalue=customtkinter.DISABLED, offvalue=customtkinter.NORMAL)
        self.rootFrame.content_checkBox.grid(row=content_checkBox_row, column=0, sticky="nsew", padx=10, pady=10)           

        #Content filters row
        content_fileter_row = 2
        self.rootFrame.content_fileter_label = customtkinter.CTkLabel(self.rootFrame, text="Content filter", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.content_fileter_label.grid(row=content_fileter_row, column=0, sticky="nsew", padx=10, pady=10)            
        
        self.rootFrame.content_fileter_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.content_fileter_textbox.grid(row=content_fileter_row, column=1, sticky="nsew",padx=10, pady=10)              
        self.rootFrame.content_fileter_textbox.insert("0.0", self.ctx.get_content_search_text() )

        self.rootFrame.content_fileter_button = customtkinter.CTkButton(self.rootFrame, text="Save", width=30, height=20, command=self.linkField_event)
        self.rootFrame.content_fileter_button.grid(row=content_fileter_row, column=2, sticky="nsew",padx=10, pady=10)

        #Price filter checkbox
        price_filter_checkbox_row = 3
        self.rootFrame.price_filter_checkbox = customtkinter.CTkCheckBox(self.rootFrame, text="Price filter checkbox", command=self.price_filter_checkbox_event, variable=self.price_filter_checkbox_var, onvalue=customtkinter.DISABLED, offvalue=customtkinter.NORMAL)
        self.rootFrame.price_filter_checkbox.grid(row=price_filter_checkbox_row, column=0, sticky="nsew", padx=10, pady=10)         

        #Price limit
        price_limit_row = 4
        self.rootFrame.price_limit_from_label = customtkinter.CTkLabel(self.rootFrame, text="Price from", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.price_limit_from_label.grid(row=price_limit_row, column=0, sticky="nsew", padx=10, pady=10)            
        
        self.rootFrame.price_limit_from_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.price_limit_from_textbox.grid(row=price_limit_row, column=1, sticky="nsew",padx=10, pady=10)              
        self.rootFrame.price_limit_from_textbox.insert("0.0", self.ctx.get_price_limit_from() )

        self.rootFrame.price_limit_to_label = customtkinter.CTkLabel(self.rootFrame, text="Price to", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.price_limit_to_label.grid(row=price_limit_row, column=2, sticky="nsew", padx=10, pady=10)    

        self.rootFrame.price_limit_to_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.price_limit_to_textbox.grid(row=price_limit_row, column=3, sticky="nsew",padx=10, pady=10)              
        self.rootFrame.price_limit_to_textbox.insert("0.0", self.ctx.get_price_limit_to() )
   
        #Refresh time row
        refresh_time_row = 5
        self.rootFrame.refresh_time_label = customtkinter.CTkLabel(self.rootFrame, text="Refresh time", compound="left", height=20, font=customtkinter.CTkFont(size=15, weight="bold"))    
        self.rootFrame.refresh_time_label.grid(row=refresh_time_row, column=0, sticky="nsew", padx=10, pady=10)            
        
        self.rootFrame.refresh_time_textbox = customtkinter.CTkTextbox(self.rootFrame, corner_radius=0, height=20, activate_scrollbars= False )
        self.rootFrame.refresh_time_textbox.grid(row=refresh_time_row, column=1, sticky="nsew",padx=10, pady=10)              
        self.rootFrame.refresh_time_textbox.insert("0.0", self.ctx.get_refresh_result() )

        self.rootFrame.refresh_time_button = customtkinter.CTkButton(self.rootFrame, text="Save", width=30, height=20,  command=self.linkField_event)
        self.rootFrame.refresh_time_button.grid(row=refresh_time_row, column=2, sticky="nsew",padx=10, pady=10)


    def linkField_event(self):
        self.ctx.set_search_text(self.rootFrame.main_filter_textbox.get("0.0", "end"))
        self.ctx.set_content_search_checkBox(self.content_fileter_checkbox_var.get())
        self.ctx.set_content_search_text(self.rootFrame.content_fileter_textbox.get("0.0", "end"))
        self.ctx.set_refresh_result(self.rootFrame.refresh_time_textbox.get("0.0", "end"))

        print("search_text:", self.ctx.get_search_text())
        print("content_search_checBox:", self.ctx.get_content_search_checkBox())
        print("content_search_text:", self.ctx.get_content_search_text())
        print("set_refresh_result:", self.ctx.get_refresh_result())

    def content_fileter_checkbox_event(self):
        if self.content_fileter_checkbox_var.get() == customtkinter.NORMAL:
            self.rootFrame.content_fileter_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            self.rootFrame.content_fileter_button.configure(state = customtkinter.NORMAL, fg_color=['#3B8ED0', '#1F6AA5'])
            print("content_fileter_checkbox_event: ", customtkinter.NORMAL)
        else:
            self.rootFrame.content_fileter_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            self.rootFrame.content_fileter_button.configure(state = customtkinter.DISABLED, fg_color= "gray30") 
            print("content_fileter_checkbox_event: ", customtkinter.DISABLED)

    def price_filter_checkbox_event(self):
        if self.price_filter_checkbox_var.get() == customtkinter.NORMAL:
            self.rootFrame.price_limit_from_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            self.rootFrame.price_limit_to_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("price_filter_checkbox_event: ", customtkinter.NORMAL)
        else:
            self.rootFrame.price_limit_from_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            self.rootFrame.price_limit_to_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("price_filter_checkbox_event: ", customtkinter.DISABLED)
        
