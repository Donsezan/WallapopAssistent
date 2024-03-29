import os
from windows_toasts import  AudioSource, Toast, ToastAudio, WindowsToaster, ToastDisplayImage

from constants import Constants

class NotificationServises:
    def __init__(self):
        print ("Noted")
    
    def SendNotification(self, contents, with_sound):
        toaster = WindowsToaster('New content')
        newToast = Toast()
        noted = False

        for content in contents:       
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
