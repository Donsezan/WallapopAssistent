import customtkinter
import webbrowser
import os

from Context.context import Context
from constants import Constants
from PIL import Image
from helper import Helper

class MainView:
    def __init__(self, ctx):
        self.ctx = ctx        

    def init(self, root):
        self.rootFrame = root  
        self.rootFrame.grid_columnconfigure(0, weight=1)  
        self.rootFrame.content_button_frame = None    
        self.rootFrame.grid(row=0, column=1, sticky="nsew")    

    def draw_content__buttons(self, finalContent):
      
        if self.rootFrame.content_button_frame is not None:
            self.rootFrame.content_button_frame.destroy()  

        finalContent = Helper.sort_content_by_date(finalContent)
        self.rootFrame.content = finalContent
        row_val = 0
        col_val = 0
        self.rootFrame.content_button_frame = customtkinter.CTkFrame(self.rootFrame, corner_radius=0, fg_color="transparent")
        self.rootFrame.content_button_frame.grid(row=0, column=0, sticky="nsew")
        self.rootFrame.content_button_frame.grid_columnconfigure(0, weight=1)
        self.rootFrame.content_button_frame.grid_columnconfigure(1, weight=1)
        self.rootFrame.content_button_frame.grid_columnconfigure(2, weight=1)

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