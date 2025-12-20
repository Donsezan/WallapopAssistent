import os
import customtkinter
import webbrowser

from PIL import Image
from helper import Helper
from constants import Constants
from Views.ProductCard import ProductCard

class MainTabView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object
        self.image_cache = {} # Cache for CTkImage objects
        self.populated_tabs = set() # Track which tabs have been populated

    def init(self, root):  
        self.rootFrame = root  
        self.image_cache = {} # Reset cache on re-init
        self.populated_tabs = set()

        if hasattr(self.rootFrame, 'tabview') and self.rootFrame.tabview is not None:
            self.rootFrame.tabview.destroy()

        # Add command listener for tab change
        self.rootFrame.tabview = customtkinter.CTkTabview(self.rootFrame, command=self.on_tab_change)
        self.rootFrame.tabview.grid(row=self.ctx.get_content_buttons_row_to_use(), column=0, padx=(20, 20), pady=(0, 0), sticky="nsew", columnspan=4)       

        self.rootFrame.tabview.add("All")      
        # Lazy load: Don't populate "All" immediately unless it's the default.
        # CTkTabview usually selects the first tab by default.
        # We can manually populate it or let the command trigger if it fires on init (it usually doesn't).
        # So we populate "All" manually.
        self.populate_content_tab("All")
        
        for param_key in self.ctx.MainParameters.get_dict():
            self.rootFrame.tabview.add(param_key)
            # content = self.ctx.MainParameters.get_content(param_key)
            # self.fill_content_tab(self.rootFrame.tabview.tab(param_key), content) # REMOVED eager loading

    def on_tab_change(self):
        selected_tab = self.rootFrame.tabview.get()
        if selected_tab not in self.populated_tabs:
            self.populate_content_tab(selected_tab)

    def populate_content_tab(self, tab_name):
        if tab_name in self.populated_tabs:
            return

        print(f"Populating tab: {tab_name}")
        tabFrame = self.rootFrame.tabview.tab(tab_name)
        
        # Determine content
        if tab_name == "All":
            content = self.ctx.MainParameters.get_all_content()
        else:
            content = self.ctx.MainParameters.get_content(tab_name)
            
        if content is None:
            content = []

        # Sort content
        content = Helper.sort_content_by_date(content)

        # Setup Scrollable Frame if needed? 
        # CTkTabview tabs are frames. We can use a scrollable frame inside if content is long.
        # The previous implementation used a normal frame 'grid_tabFrame' inside the tab.
        # If the tabview itself is not scrollable, we might want a scrollable frame.
        # Usually tabs in standard UI are just containers. 
        # The root frame "main_frame" in main.py is a CTkScrollableFrame. 
        # So the tabview is inside a scrollable frame. 
        # This means the inner content will just grow the scrollable area.
        
        grid_tabFrame = customtkinter.CTkFrame(tabFrame, corner_radius=0, fg_color="transparent")
        grid_tabFrame.grid(row=0, column=0, sticky="nsew")
        grid_tabFrame.grid_columnconfigure(0, weight=1) # ProductCard is flexible?
        # To make cards reflow, we need specific column config or a grid manager.
        # Previous code used 3 columns.
        grid_tabFrame.grid_columnconfigure(0, weight=1)
        grid_tabFrame.grid_columnconfigure(1, weight=1)
        grid_tabFrame.grid_columnconfigure(2, weight=1)

        row_val = 0
        col_val = 0

        for item_content in content:     
            # Create ProductCard
            card = ProductCard(grid_tabFrame, content=item_content, image_cache=self.image_cache)
            card.grid(row=row_val, column=col_val, padx=10, pady=10, sticky="nsew")
            
            col_val += 1
            if col_val == 3:
                col_val = 0
                row_val += 1
        
        self.populated_tabs.add(tab_name)

    # Renaming for compatibility if needed, or deleting old method
    # fill_content_tab is replaced by populate_content_tab logic

    def button_event(self, url):
        webbrowser.open_new(url)
