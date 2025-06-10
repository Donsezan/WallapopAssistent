import os
import sys
import customtkinter
import webbrowser

from constants import Constants
from PIL import Image
from helper import Helper
from Views.mainTabView import MainTabView

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
        content_buttons_row_to_use = 0 # Default row for content_button_frame

        if is_offline:
            self.offline_message_label = customtkinter.CTkLabel(
                self.rootFrame, 
                text="Offline/Connection Problem: Displaying cached content.",
                text_color="orange", # Using a distinct color
                font=customtkinter.CTkFont(size=14, weight="bold")
            )
            # Place the message in row 0 of self.rootFrame.
            # Ensure self.rootFrame is configured for this (e.g. row 0 for message, row 1 for buttons)
            self.offline_message_label.grid(row=0, column=0, sticky="new", padx=10, pady=(5, 5))
            content_buttons_row_to_use = 1 # Content buttons will now go into row 1
        
        # --- Existing Content Button Frame Handling ---
        if self.rootFrame.content_button_frame is not None:
            self.rootFrame.content_button_frame.destroy()  
        
        # Create the content_button_frame and place it in the determined row
        self.rootFrame.content_button_frame = customtkinter.CTkFrame(self.rootFrame, corner_radius=0, fg_color="transparent")
        self.rootFrame.content_button_frame.grid(row=content_buttons_row_to_use, column=0, sticky="nsew")
        
        # Configure columns for the content_button_frame itself (where the actual buttons go)
        self.rootFrame.content_button_frame.grid_columnconfigure(0, weight=1)
        self.rootFrame.content_button_frame.grid_columnconfigure(1, weight=1)
        self.rootFrame.content_button_frame.grid_columnconfigure(2, weight=1)

        # If offline and no content, the message still shows. If online and no content, nothing shows (as per original logic).
        if finalContent is None or len(finalContent) == 0:
            if is_offline:
                # Optional: Add a specific message to content_button_frame if needed,
                # but the main offline message is already visible above.
                no_cached_label = customtkinter.CTkLabel(self.rootFrame.content_button_frame, text="No cached content available.")
                no_cached_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
            return

        finalContent = Helper.sort_content_by_date(finalContent)
        self.rootFrame.content = finalContent # This seems to store content on the frame, might not be necessary
        
        row_val = 0
        col_val = 0
        for content in finalContent:     
            print(content['title'])
            result =  os.path.join(Constants.Temp_folder, content['web_slug']+".jpg")    
            web_slug = content['web_slug']
            webLinlk = "https://es.wallapop.com/item/" + web_slug
            title = content['title'][:15]
            price = content['price']
            finalName = f"{title}\n{price}"
            self.temp_img = customtkinter.CTkImage(Image.open(result), size=(100, 100))         

            button_command = lambda link=webLinlk: self.button_event(link)
            button = customtkinter.CTkButton(self.rootFrame.content_button_frame, text=finalName, image=self.temp_img, compound="top", command = button_command)
            button.grid(row=row_val, column=col_val, padx=20, pady=20)
            col_val += 1
            if col_val == 3:
                col_val = 0
                row_val += 1   

    def button_event(self, url):
        webbrowser.open_new(url)