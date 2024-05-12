import re
import customtkinter
from datetime import datetime 

class Helper:
     @classmethod
     def remove_newline_symbol(cls, input):
        #return input.replace('\n', '')
        output = input
        symbol = "\n"
        if isinstance(input, int):
            return output
        if input.endswith(symbol):   
            output = input.replace('\n', '')    
            #output = input[:-len(symbol)]
        return output
     
     def find_differences_in_array(array1, array2):
        if not isinstance(array1, list):
            array1 = []
        if not isinstance(array2, list):
            array2 = []    
        differences = []
        for obj1 in array1:
            found = False
            for obj2 in array2:
                if obj1 == obj2:
                    found = True
                    break
            if not found:
                differences.append(obj1)
        return differences
     
     def split_string(text):
        return re.split(r'[,\s]+', text)
     
     def sort_content_by_date(content, reversed = True):
        return sorted(content, key=lambda x: datetime.strptime(x['creation_date'], '%Y-%m-%dT%H:%M:%S.%f%z'), reverse=reversed)
     
     def getByKey(dictionary, key):
        return dictionary.get(key, None)
          
     def _validationForKey(dictionary, key):
        if not key in dictionary:
            raise ValueError("invalid dictionary key: " + key)
        
     def validate_int(textbox):
        value = Helper.remove_newline_symbol(textbox.get("0.0", "end"))
        print(textbox.cget("fg_color"))
        if value.isdigit():
            textbox.configure(state = customtkinter.NORMAL, fg_color= ['#F9F9FA', '#1D1E1E'])   
            return True
        else:       
            textbox.configure(state = customtkinter.NORMAL, fg_color= "red")   
            return False    