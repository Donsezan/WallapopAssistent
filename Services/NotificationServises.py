import os
import time
import threading

from windows_toasts import  AudioSource, Toast, ToastAudio, WindowsToaster, ToastDisplayImage

from constants import Constants

class NotificationServises:
    def __init__(self):
        print ("NotificationServises inited")
        self.notification_thread = None
        self.stop_event = threading.Event()
    
    def SendNotification(self, contents, with_sound):
        while self.notification_thread and self.notification_thread.is_alive():        
            self.stop_event.set()

        if not self.notification_thread or not self.notification_thread.is_alive():
            self.stop_event.clear()
                   
            self.notification_thread = threading.Thread(target=self.SendNotifications_thread, args=(self.stop_event, contents, with_sound), daemon=True)
            self.notification_thread.start()

    def SendNotifications_thread(self, stop_event, contents, with_sound):   
        toaster = WindowsToaster('New content')    
        noted = False
        for content in contents:    
            if stop_event.is_set(): 
                break      
            newToast = Toast()               
            newToast.text_fields = [content['title']]
            current_directory = os.path.dirname(os.path.realpath(__file__))
            parent_directory = os.path.dirname(current_directory)
            image_path = os.path.join(parent_directory, Constants.Temp_folder)
            
            newToast.AddImage(ToastDisplayImage.fromPath(os.path.join(image_path, content['web_slug']+".jpg")))
            newToast.launch_action = "https://es.wallapop.com/item/" + content['web_slug']
            if not noted and with_sound:
                newToast.audio = ToastAudio(AudioSource.IM, looping=False)
                noted = True
            toaster.show_toast(newToast)
            time.sleep(1) 
