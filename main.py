import customtkinter
import os
import threading
import time

from main_logic import Main_logic
from PIL import Image
from Views.paramView import ParamView
from Views.mainView import MainView
from helper import Helper
from Services.NotificationServises import NotificationServises
from Context.context import Context
from constants import Constants


class App(customtkinter.CTk):  

    def __init__(self):
        super().__init__()
        self.ctx = Context()  
        self.main_logic = Main_logic(self.ctx)
        self.mainFrame = MainView(self.ctx)
        self.ParamViewFrame = ParamView(self.ctx, self.main_logic)  
        self.notification = NotificationServises() 

        #params: dict | None = None,      
        self._params :  dict | None = None
        self.stop_event = threading.Event()
        self.update_thread = None
        self.content = None        
        self.current_frame = None

        self.title("Wallapop assistent")
        self.geometry("1000x600")

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

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=Constants.Frames.Home,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text=Constants.Frames.Settings,
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=2, column=0, sticky="ew")

        self.refresh_button = customtkinter.CTkButton(self.navigation_frame, text=Constants.Buttons.Refresh_button_normal_text, width=30, height=40, command=self.refresh_button_event)
        self.refresh_button.grid(row=4, column=0, sticky="nsew",padx=20, pady=20)

        #logic 
        self.main_logic.rehydrate_contnet()    
        self.main_logic.Download_content()

        # create home frame  
        self.main_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.mainFrame.init(self.main_frame)
        self.mainFrame.draw_content__buttons(self.content)          
     
        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        self.select_frame_by_name(Constants.Frames.Home)

    def select_frame_by_name(self, name):

        self.home_button.configure(fg_color=("gray75", "gray25") if name == Constants.Frames.Home else "transparent")
        self.settings_button.configure(fg_color=("gray75", "gray25") if name == Constants.Frames.Settings else "transparent")

        if self.current_frame == name:
            return

        # show selected frame
        if name == Constants.Frames.Home:
            self.current_frame = Constants.Frames.Home
            self.mainFrame.init(self.main_frame)
            self.refresh_button.configure(state = customtkinter.NORMAL, fg_color=Constants.Buttons.Button_enable_color, text=Constants.Buttons.Refresh_button_normal_text)
            if self.ctx.MainParameters.get_auto_refresh_checkbox() == Constants.CheackBox_enabled_status:
                if not self.update_thread or not self.update_thread.is_alive():
                    self.stop_event.clear()
                    self.update_thread = threading.Thread(target=self.update_button_text, args=(self.refresh_button, self.stop_event), daemon=True)
                    self.update_thread.start()
                else:
                    self.stop_event.clear()
        else:
            self.main_frame.grid_forget()
        if name == Constants.Frames.Settings:
            self.current_frame = Constants.Frames.Settings
            self.stop_event.set()
            self.refresh_button.configure(state = customtkinter.DISABLED, fg_color= Constants.Buttons.Button_disable_color, text=Constants.Buttons.Refresh_button_pause_text)             
            self.ParamViewFrame.init(self.second_frame)

        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name(Constants.Frames.Home)

    def settings_button_event(self):
        self.select_frame_by_name(Constants.Frames.Settings)

        
    def refresh_button_event(self):
        self.stop_event.set()  
        self.refresh_button.configure(state = customtkinter.DISABLED, fg_color= Constants.Buttons.Button_disable_color, text=Constants.Buttons.Refresh_button_working_text) 
        self.update_idletasks()
        new_content = self.main_logic.Download_content(True)
        self.mainFrame.init(self.main_frame)
        
        self.refresh_button.configure(state = customtkinter.NORMAL, fg_color=Constants.Buttons.Button_enable_color, text=Constants.Buttons.Refresh_button_normal_text)
        if self.ctx.MainParameters.get_auto_refresh_checkbox() == Constants.CheackBox_enabled_status:
            if not self.update_thread or not self.update_thread.is_alive():
                self.stop_event.clear()
                self.update_thread = threading.Thread(target=self.update_button_text, args=(self.refresh_button, self.stop_event), daemon=True)
                self.update_thread.start()
            else:
                self.stop_event.clear()
        
        if self.ctx.MainParameters.get_notification_toastup_checkbox() == Constants.CheackBox_enabled_status:          
            if any(new_content):
                self.notification.SendNotification(new_content, self.ctx.MainParameters.get_notification_soundnote_checkbox() == Constants.CheackBox_enabled_status)   
        print("-Refresh action")
        
    def update_button_text(self, button, stop_event):
        limit = int(self.ctx.MainParameters.get_refresh_time())
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
