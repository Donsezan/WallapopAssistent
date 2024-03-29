import customtkinter
import os
import threading
import time

from main_logic import Main_logic
from PIL import Image
from Views.paramView import ParamView
from context import Context
from constants import Constants

import webbrowser

class App(customtkinter.CTk):  

    def __init__(self):
        super().__init__()
        self.ctx = Context()  
        self.main_logic = Main_logic(self.ctx)
        self.secondFrame = ParamView(self.ctx)  

        params: dict | None = None,      
        self._params = params
        self.stop_event = threading.Event()
        self.update_thread = None

        self.title("Wallapop assistent")
        self.geometry("800x600")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo-wallapop.png")), size=(183, 48))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(3, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text=" ", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.refresh_button = customtkinter.CTkButton(self.navigation_frame, text=Constants.Buttons.Refresh_button_normal_text, width=30, height=40, command=self.refresh_button_event)
        self.refresh_button.grid(row=4, column=0, sticky="nsew",padx=20, pady=20)


        # create home frame  
        self.home_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

       
        finalContent = self.main_logic.Init()
        self.draw_content__buttons(finalContent)
 
        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.select_frame_by_name("home")
      
    def draw_content__buttons(self, finalContent):
        row_val = 0
        col_val = 0
        self.content_button_frame = customtkinter.CTkFrame(self.home_frame, corner_radius=0, fg_color="transparent")
        self.content_button_frame.grid(row=0, column=0, sticky="nsew")
        self.content_button_frame.grid_columnconfigure(0, weight=1)
        self.content_button_frame.grid_columnconfigure(1, weight=1)
        self.content_button_frame.grid_columnconfigure(2, weight=1)

        for content in finalContent:        
            # print(content)    
            print(content['title'])
            result =  os.path.join("temp", content['web_slug']+".jpg")    
            web_slug = content['web_slug']
            webLinlk = "https://es.wallapop.com/item/" + web_slug
            title = content['title'][:15]
            price = content['price']
            finalName = f"{title}\n{price}"
            self.temp_img = customtkinter.CTkImage(Image.open(result), size=(100, 100))         

            button_command = lambda link=webLinlk: self.button_event(link)
            button = customtkinter.CTkButton(self.content_button_frame, text=finalName, image=self.temp_img, compound="top", command = button_command)
            button.grid(row=row_val, column=col_val, padx=20, pady=20)
            col_val += 1
            if col_val == 3:
                col_val = 0
                row_val += 1   

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")  
            self.refresh_button.configure(state = customtkinter.NORMAL, fg_color=Constants.Buttons.Button_enable_color, text=Constants.Buttons.Refresh_button_normal_text)
            if self.ctx.get_auto_refresh_checkbox() == Constants.CheackBox_enabled_status:
                if not self.update_thread or not self.update_thread.is_alive():
                    self.stop_event.clear()
                    self.update_thread = threading.Thread(target=self.update_button_text, args=(self.refresh_button, self.stop_event), daemon=True)
                    self.update_thread.start()
                else:
                    self.stop_event.clear()

        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.stop_event.set()
            self.refresh_button.configure(state = customtkinter.DISABLED, fg_color= Constants.Buttons.Button_disable_color, text=Constants.Buttons.Refresh_button_pause_text) 
            
            self.secondFrame.init(self.second_frame)
            #self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def button_event(self, url):
        webbrowser.open_new(url)
        
    def refresh_button_event(self):
        self.stop_event.set()  
        self.refresh_button.configure(state = customtkinter.DISABLED, fg_color= Constants.Buttons.Button_disable_color, text=Constants.Buttons.Refresh_button_working_text) 
        self.update_idletasks()
        new_content = self.main_logic.get_content()
        self.content_button_frame.destroy()       
        self.draw_content__buttons(new_content)
        self.refresh_button.configure(state = customtkinter.NORMAL, fg_color=Constants.Buttons.Button_enable_color, text=Constants.Buttons.Refresh_button_normal_text)
        if self.ctx.get_auto_refresh_checkbox() == Constants.CheackBox_enabled_status:
            if not self.update_thread or not self.update_thread.is_alive():
                self.stop_event.clear()
                self.update_thread = threading.Thread(target=self.update_button_text, args=(self.refresh_button, self.stop_event), daemon=True)
                self.update_thread.start()
            else:
                self.stop_event.clear()
        print("refresh")
        
    def update_button_text(self, button, stop_event):
        limit = int(self.ctx.get_refresh_time())
        count = limit
        while not stop_event.is_set():            
            button.configure(text=f"Update in: {count}")
            count -= 1
            time.sleep(1)  
            if count == 0:
                self.refresh_button_event()
                count = limit
    
if __name__ == "__main__":
    app = App()
    app.mainloop()
