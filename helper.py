
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