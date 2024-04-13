import re
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