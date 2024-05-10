import customtkinter
from helper import Helper

class BaseView:
    def validate_int(self, textbox):
        value = Helper.remove_newline_symbol(textbox.get("0.0", "end"))
        print(textbox.cget("fg_color"))
        if value.isdigit():
            textbox.configure(state = customtkinter.NORMAL, fg_color= ['#F9F9FA', '#1D1E1E'])   
            return True
        else:       
            textbox.configure(state = customtkinter.NORMAL, fg_color= "red")   
            return False          