import customtkinter
from helper import Helper
from constants import Constants

class ParamTabView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object
    
    def init(self, root):  
        self.rootFrame = root                   
        self.rootFrame.tabview = customtkinter.CTkTabview(self.rootFrame)
        self.rootFrame.tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew", columnspan=4)       
             
        for param_key in self.ctx.get_parameter_dicts():
            self.rootFrame.tabview.add(param_key)      
            paramters = self.ctx.get_parameter_byKey(param_key)
            self.create_param_tab(self.rootFrame.tabview.tab(param_key), paramters)
            self.rootFrame.tabview.set(param_key)

        self.rootFrame.tabview.add("+")            
        self.rootFrame.tabview.tab("+")
        self.create_add_tab(self.rootFrame.tabview.tab("+"))

    def create_param_tab(self, tabFrame, paramters):
        _search_radio_button_var = customtkinter.IntVar(value=paramters._search_type)
        _content_fileter_checkbox_var = customtkinter.StringVar(value=paramters._content_filter_checkBox)       
        _price_filter_checkbox_var = customtkinter.StringVar(value=paramters._price_filter_checkbox)      
        _search_text = paramters._search_text
        _content_filter_text = paramters._content_filter_text
        _price_limit_from = paramters._price_limit_from
        _price_limit_to = paramters._price_limit_to
        _guid = paramters._searchGuid

        price_filter_checkbox_comand = object
        #self.rootFrame.tabview.add(tabName)
        tabFrame.grid_columnconfigure(0, weight=1)
        tabFrame.columnconfigure(1, weight=0)
        tabFrame.columnconfigure(2, weight=1)
        tabFrame.columnconfigure(3, weight=0)
        tabFrame.columnconfigure(2, weight=1)
        

        #Search radio button group
        search_radio_button_group_row = 0

        tabFrame.radiobutton_frame = customtkinter.CTkFrame(tabFrame)
        tabFrame.radiobutton_frame.grid(row=search_radio_button_group_row, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew", columnspan=4)

        tabFrame.search_radio_button_1 = customtkinter.CTkRadioButton(master=tabFrame.radiobutton_frame, text="Direct search", variable=_search_radio_button_var, value=Constants.SearchType.Direct_search)
        tabFrame.search_radio_button_1.grid(row=0, column=0, pady=10, padx=20, sticky="n")
        search_radio_button_2 = customtkinter.CTkRadioButton(master=tabFrame.radiobutton_frame, text="History search", variable=_search_radio_button_var, value=Constants.SearchType.History_search)
        search_radio_button_2.grid(row=0, column=1, pady=10, padx=20, sticky="nsew")
        tabFrame.radiobutton_frame.grid_columnconfigure(0, weight=1)
        tabFrame.radiobutton_frame.grid_columnconfigure(1, weight=1)

        # #Main filter row
        main_filter_row = search_radio_button_group_row + 1

        tabFrame.main_filter_label = customtkinter.CTkLabel(tabFrame, text="Filter", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"))    
        tabFrame.main_filter_label.grid(row=main_filter_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=1)            
        
        tabFrame.main_filter_textbox = customtkinter.CTkTextbox(tabFrame, corner_radius=0, height=20, activate_scrollbars= False)
        tabFrame.main_filter_textbox.grid(row=main_filter_row, column=1, sticky="nsew",padx=5, pady=5, columnspan=3)              
        tabFrame.main_filter_textbox.insert("0.0", _search_text)
    
        #Content filters checkbox
        content_checkBox_row = main_filter_row + 1
        tabFrame.content_checkBox = customtkinter.CTkCheckBox(tabFrame, text="Content filter", command=self.content_fileter_checkbox_event, variable=_content_fileter_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        tabFrame.content_checkBox.grid(row=content_checkBox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)        
        
        #Content filters row
        content_fileter_row = content_checkBox_row + 1
        tabFrame.content_fileter_label = customtkinter.CTkLabel(tabFrame, text="Content filter", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"))    
        tabFrame.content_fileter_label.grid(row=content_fileter_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=1)            
        
        tabFrame.content_fileter_textbox = customtkinter.CTkTextbox(tabFrame, corner_radius=0, height=20, activate_scrollbars= False )
        tabFrame.content_fileter_textbox.grid(row=content_fileter_row, column=1, sticky="nsew",padx=5, pady=5, columnspan=3)              
        tabFrame.content_fileter_textbox.insert("0.0", _content_filter_text )      

        #Price filter checkbox
        price_filter_checkbox_row = content_fileter_row + 1 
        
        tabFrame.price_filter_checkbox = customtkinter.CTkCheckBox(tabFrame, text="Price filter", command=price_filter_checkbox_comand, variable=_price_filter_checkbox_var, onvalue=customtkinter.ACTIVE, offvalue=customtkinter.NORMAL)
        tabFrame.price_filter_checkbox.grid(row=price_filter_checkbox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)         

        #Price limit
        price_limit_row = price_filter_checkbox_row + 1
        tabFrame.price_limit_from_label = customtkinter.CTkLabel(tabFrame, text="Price From", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"))    
        tabFrame.price_limit_from_label.grid(row=price_limit_row, column=0, sticky="nsew", padx=5, pady=5)            
        
        tabFrame.price_limit_from_textbox = customtkinter.CTkTextbox(tabFrame, corner_radius=0, height=20, activate_scrollbars= False, width=80)
        tabFrame.price_limit_from_textbox.grid(row=price_limit_row, column=1, sticky="nsew",padx=5, pady=5)              
        tabFrame.price_limit_from_textbox.insert("0.0", _price_limit_from )

        tabFrame.price_limit_to_label = customtkinter.CTkLabel(tabFrame, text="To", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"), width=20 )    
        tabFrame.price_limit_to_label.grid(row=price_limit_row, column=2, sticky="nsew", padx=5, pady=5)    

        tabFrame.price_limit_to_textbox = customtkinter.CTkTextbox(tabFrame, corner_radius=0, height=20, activate_scrollbars= False  )
        tabFrame.price_limit_to_textbox.grid(row=price_limit_row, column=3, sticky="nsew",padx=5, pady=5)              
        tabFrame.price_limit_to_textbox.insert("0.0", _price_limit_to)
        price_filter_checkbox_comand = lambda checkBox=tabFrame.price_filter_checkbox, priceFrom = tabFrame.price_limit_from_textbox, priceTo = tabFrame.price_limit_to_textbox: self.price_filter_checkbox_event(checkBox, priceFrom, priceTo)
        price_filter_checkbox_comand()

        #Delete button
        delete_button_row = price_limit_row + 1 
        tabFrame.price_limit_to_label = customtkinter.CTkLabel(tabFrame, text=_guid, compound="left", height=20, font=customtkinter.CTkFont(size=8), text_color= "Grey", width=20 )    
        tabFrame.price_limit_to_label.grid(row=delete_button_row, column=0, sticky="nsew", padx=5, pady=5)    


        delete_button_command = lambda tab_name = "tabFrame.new_tab_textbox.get)": self.delete_tab(tab_name)
        self.rootFrame.save_button = customtkinter.CTkButton(tabFrame, text="Delete", width=30, height=20,  command=delete_button_command)
        self.rootFrame.save_button.grid(row=delete_button_row, column=1, sticky="nsew",padx=10, pady=10, columnspan=3)        

        print ("Tab with name: '" + tabFrame.master._current_name + "' created")                
                         
    def delete_tab(self, tabFrame):
        print ("delete "+ tabFrame)

    def create_add_tab(self, tabFrame):

        tabFrame.grid_columnconfigure(0, weight=1)
        tabFrame.columnconfigure(1, weight=0)

        new_tab_textbox_row = 0
        tabFrame.new_tab_textbox_label = customtkinter.CTkLabel(tabFrame, text="New search name", compound="left", height=20, font=customtkinter.CTkFont(size=12, weight="bold"))    
        tabFrame.new_tab_textbox_label.grid(row=new_tab_textbox_row, column=0, sticky="nsew", padx=5, pady=5, columnspan=1)          

        tabFrame.new_tab_textbox = customtkinter.CTkTextbox(tabFrame, corner_radius=0, height=20, activate_scrollbars= False, wrap="none" )
        tabFrame.new_tab_textbox.grid(row=new_tab_textbox_row, column=1, sticky="nsew", padx=5, pady=5, columnspan=3)              
        tabFrame.new_tab_textbox.insert("0.0","")   
        
        save_button_row = 1
    
        create_button_command = lambda tab_name = "tabFrame.new_tab_textbox.get)": (           
            self.create_new_tab(tab_name),
            tabFrame.new_tab_textbox.delete("1.0", "end")
            )
        tabFrame.create_button = customtkinter.CTkButton(tabFrame, text="Create", width=30, height=20,  command=create_button_command)
        tabFrame.create_button.grid(row=save_button_row, column=0, sticky="nsew",padx=10, pady=10, columnspan=4)

    def create_new_tab(self, new_tab_name):          
        vss = self.rootFrame.tabview.tab("+").new_tab_textbox.get("0.0", "end")
        new_tab_name = Helper.remove_newline_symbol(vss)          
        self.rootFrame.tabview.add(new_tab_name)          

        self.ctx.create_param_dict(new_tab_name)
        parameters = self.ctx.get_parameter_byKey(new_tab_name)
        self.create_param_tab(self.rootFrame.tabview.tab(new_tab_name), parameters)
        self.rootFrame.tabview.set(new_tab_name)

        creat_tab_index = self.rootFrame.tabview.index("+")
        last_tab_index = creat_tab_index+1
        self.rootFrame.tabview.move(last_tab_index, "+")

    def content_fileter_checkbox_event(self):
        if self.content_fileter_checkbox_var.get() == customtkinter.ACTIVE:
            self.rootFrame.content_fileter_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("content_fileter_checkbox_event: ", customtkinter.ACTIVE)
        else:
            self.rootFrame.content_fileter_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("content_fileter_checkbox_event: ", customtkinter.NORMAL)

    def price_filter_checkbox_event(self, check_box, price_limit_from_textbox, price_limit_to_textbox):
        if check_box.get() == customtkinter.ACTIVE:
            price_limit_from_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            price_limit_to_textbox.configure(state = customtkinter.NORMAL, text_color= "White")   
            print("price_filter_checkbox_event: ", customtkinter.ACTIVE)
        else:
            price_limit_from_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            price_limit_to_textbox.configure(state = customtkinter.DISABLED, text_color= "Grey") 
            print("price_filter_checkbox_event: ", customtkinter.NORMAL)

   