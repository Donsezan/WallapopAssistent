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
        content_buttons_row_to_use = 0

        if is_offline:
            self.offline_message_label = customtkinter.CTkLabel(
                self.rootFrame, 
                text="Offline/Connection Problem: Displaying cached content.",
                text_color="orange",
                font=customtkinter.CTkFont(size=14, weight="bold")
            )
            self.offline_message_label.grid(row=0, column=0, sticky="new", padx=10, pady=(5, 5))
            content_buttons_row_to_use = 1
        
        # --- Existing Content Button Frame Handling ---
        if self.rootFrame.content_button_frame is not None:
            self.rootFrame.content_button_frame.destroy()  
        
        self.rootFrame.content_button_frame = customtkinter.CTkFrame(self.rootFrame, corner_radius=0, fg_color="transparent")
        self.rootFrame.content_button_frame.grid(row=content_buttons_row_to_use, column=0, sticky="nsew")
        
        self.rootFrame.content_button_frame.grid_columnconfigure(0, weight=1)
        self.rootFrame.content_button_frame.grid_columnconfigure(1, weight=1)
        self.rootFrame.content_button_frame.grid_columnconfigure(2, weight=1)

        # --- Content Filtering based on Selected Tab ---
        selected_tab_name = self.mainTabView.rootFrame.tabview.get()
        processed_content = finalContent

        if selected_tab_name != "All":
            param_key = selected_tab_name
            if param_key in self.ctx.MainParameters.get_dict():
                fs_instance = FiltersServices()
                try:
                    processed_content = fs_instance.filteringContent(
                        contents=finalContent,
                        titlePatern=Helper.split_string(self.ctx.MainParameters.get_search_text(param_key)),
                        isDiscriptionCheck=self.ctx.MainParameters.get_content_filter_checkBox(param_key) == Constants.CheackBox_enabled_status,
                        discriptionPatern=Helper.split_string(self.ctx.MainParameters.get_content_filter_text(param_key)),
                        isPriceCheck=self.ctx.MainParameters.get_price_filter_checkbox(param_key) == Constants.CheackBox_enabled_status,
                        priceRange=[
                            self.ctx.MainParameters.get_price_limit_from(param_key),
                            self.ctx.MainParameters.get_price_limit_to(param_key)
                        ]
                    )
                except Exception as e:
                    print(f"Error during filtering content for tab {param_key}: {e}")
                    processed_content = []
            else:
                # This case means tab name is not "All" and not a recognized param_key
                print(f"Warning: Tab '{selected_tab_name}' not found in MainParameters. Displaying no content for this tab.")
                processed_content = [] # Default to no content for unknown specific tabs

        # --- Sort and Prepare for Display ---
        if processed_content is not None:
            processed_content = Helper.sort_content_by_date(processed_content)
        
        # Update the frame's content reference, used by other parts or for debugging
        self.rootFrame.content = processed_content

        # --- Handle Empty Content ---
        if processed_content is None or len(processed_content) == 0:
            message_text = "No content available for this tab."
            # is_offline is defined at the beginning of the method
            if is_offline:
                message_text = "No cached content available for this tab."

            empty_label = customtkinter.CTkLabel(self.rootFrame.content_button_frame, text=message_text)
            empty_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
            return

        # --- Draw Buttons ---
        row_val = 0
        col_val = 0
        for item_content in processed_content:
            image_path = os.path.join(Constants.Temp_folder, item_content['web_slug'] + ".jpg")
            web_slug = item_content['web_slug']
            webLinlk = "https://es.wallapop.com/item/" + web_slug

            # Ensure title and price are strings before formatting
            title_str = str(item_content.get('title', 'N/A')) # Use .get for safety
            price_str = str(item_content.get('price', 'N/A')) # Use .get for safety

            title = title_str[:15]
            price = price_str
            finalName = f"{title}\n{price}"

            button_image = None
            try:
                if os.path.exists(image_path):
                    button_image = customtkinter.CTkImage(Image.open(image_path), size=(100, 100))
                else:
                    # Optionally print/log: print(f"Image not found: {image_path}")
                    pass # No image, button_image remains None
            except Exception as e:
                print(f"Error loading image {image_path}: {e}. Button will be created without image.")
                button_image = None # Ensure it's None on error

            button_command = lambda link=webLinlk: self.button_event(link)
            button = customtkinter.CTkButton(
                self.rootFrame.content_button_frame,
                text=finalName,
                image=button_image,
                compound="top",
                command=button_command
            )
            button.grid(row=row_val, column=col_val, padx=20, pady=20)
            col_val += 1
            if col_val == 3:
                col_val = 0
                row_val += 1

    def button_event(self, url):
        webbrowser.open_new(url)