
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