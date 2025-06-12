import os
import customtkinter
import webbrowser

from PIL import Image
from helper import Helper
from constants import Constants

class MainTabView:
    def __init__(self, ctx):
        self.ctx = ctx
        self.rootFrame = object
    
    def init(self, root):  
        self.rootFrame = root  

        if hasattr(self.rootFrame, 'tabview') and self.rootFrame.tabview is not None:
            self.rootFrame.tabview.destroy()

        self.rootFrame.tabview = customtkinter.CTkTabview(self.rootFrame)
        self.rootFrame.tabview.grid(row=self.ctx.get_content_buttons_row_to_use(), column=0, padx=(20, 20), pady=(0, 0), sticky="nsew", columnspan=4)       

        self.rootFrame.tabview.add("All")      
        self.fill_content_tab(self.rootFrame.tabview.tab("All"), self.ctx.MainParameters.get_all_content())

        for param_key in self.ctx.TempParameters.get_dict():
            self.rootFrame.tabview.add(param_key)      
            content = self.ctx.TempParameters.get_content(param_key)
            self.fill_content_tab(self.rootFrame.tabview.tab(param_key), content)


        #      if self.rootFrame.tabview.tab(name) is not None:
        #    self.rootFrame.tabview.delete(name)  
        #   if finalContent is None or len(finalContent) == 0:
        #     return
    # def destory(self, root):
    #     root.destroy()
      
    def fill_content_tab(self, tabFrame, content):   
        content = Helper.sort_content_by_date(content)
        row_val = 0
        col_val = 0
        grid_tabFrame = customtkinter.CTkFrame(tabFrame, corner_radius=0, fg_color="transparent")
        grid_tabFrame.grid(row=0, column=0, sticky="nsew")
        grid_tabFrame.grid_columnconfigure(0, weight=1)
        grid_tabFrame.grid_columnconfigure(1, weight=1)
        grid_tabFrame.grid_columnconfigure(2, weight=1)

        for content in content:     
            print(content['title'])
            result =  os.path.join(Constants.Temp_folder, content['web_slug']+".jpg")    
            web_slug = content['web_slug']
            webLinlk = "https://es.wallapop.com/item/" + web_slug
            title = content['title'][:15]
            price = content['price']
            finalName = f"{title}\n{price}"
            self.temp_img = customtkinter.CTkImage(Image.open(result), size=(100, 100))         

            button_command = lambda link=webLinlk: self.button_event(link)
            button = customtkinter.CTkButton(grid_tabFrame, text=finalName, image=self.temp_img, compound="top", command = button_command)
            button.grid(row=row_val, column=col_val, padx=20, pady=20)
            col_val += 1
            if col_val == 3:
                col_val = 0
                row_val += 1   

    def button_event(self, url):
        webbrowser.open_new(url)