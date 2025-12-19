import os
import sys
import customtkinter
import webbrowser

from constants import Constants
from PIL import Image
from helper import Helper
from Views.mainTabView import MainTabView
from Services.FiltersServices import FiltersServices

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)

class MainView:
    def __init__(self, ctx):
        self.ctx = ctx      
        self.mainTabView = MainTabView(self.ctx)
        self.offline_message_label = None        

    def init(self, root):
        self.rootFrame = root  
        self.rootFrame.grid_columnconfigure(0, weight=1)  # Configure column 0 of rootFrame to expand
        self.rootFrame.grid_rowconfigure(0, weight=0) # Row for offline message (minimal height)
        self.rootFrame.grid_rowconfigure(1, weight=1) # Row for content buttons (takes remaining space)
        self.rootFrame.content_button_frame = None    
        self.rootFrame.grid(row=0, column=1, sticky="nsew")    
        self.mainTabView.init(self.rootFrame)   

    def draw_content__buttons(self, finalContent):
        # --- Offline Message Handling ---
        if hasattr(self, 'offline_message_label') and self.offline_message_label:
            self.offline_message_label.destroy()
            self.offline_message_label = None

        is_offline = self.ctx.get_offline_error()
        self.ctx.set_content_buttons_row_to_use(0)

        if is_offline:
            self.offline_message_label = customtkinter.CTkLabel(
                self.rootFrame, 
                text="Offline/Connection Problem: Displaying cached content.",
                text_color="orange",
                font=customtkinter.CTkFont(size=14, weight="bold")
            )
            self.offline_message_label.grid(row=0, column=0, sticky="new", padx=10, pady=(5, 5))
            self.ctx.set_content_buttons_row_to_use(1)
        
        # --- Update TabView Position ---
        # Ensure the tabview is at the correct row (0 or 1)
        if hasattr(self.mainTabView, 'rootFrame') and hasattr(self.mainTabView.rootFrame, 'tabview'):
             self.mainTabView.rootFrame.tabview.grid(row=self.ctx.get_content_buttons_row_to_use(), column=0, padx=(20, 20), pady=(0, 0), sticky="nsew", columnspan=4)
        
        # --- REMOVED Legacy Content Button Frame Handling ---
        # MainTabView is responsible for displaying content inside the tabs.
        # The previous logic here was creating a conflicting overlap.
        
        if self.rootFrame.content_button_frame is not None:
            self.rootFrame.content_button_frame.destroy() 
            self.rootFrame.content_button_frame = None

    def button_event(self, url):
        webbrowser.open_new(url)
