import json
import os
from Services.ImageService import ImageService


class FileServices:
    def __init__(self):
            self.temp_folder = "temp"

    def Save_content_to_file(self, data, file_name):
        if data is None or len(data) == 0:
            return "Nothing to save"
        try:
            file_path = os.path.join(os.getcwd(), file_name)
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=2)
            print(f"Object successfully saved to {file_path}")
        except IOError as e:
            print(f"Error saving object to {file_path}: {e}")

    def Rehidrate_from_file(self, file_name):
        try:
            # Open the file in read mode ('r')
            with open(file_name, 'r') as file:
                # Load JSON data from the file
                json_data = json.load(file)
                return json_data

        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except json.decoder.JSONDecodeError:
            print(f"Error: Unable to decode JSON in file '{file_name}'. File may be empty or not valid JSON.")

    def Merge_content(self, old_object, new_object):
        if old_object is None and new_object is None:
            return None
        elif old_object is None or len(old_object) == 0:
            return new_object
        elif new_object is None or len(new_object) == 0:
            return old_object
        
        # merged_objects = []
        # merged_objects.extend(old_object)
        # for old_obj in old_object:  
        #     for new_obj in new_object:  
        #         if old_obj['id'] != new_obj['id']:
        #             merged_objects.append(new_obj)

        merged_objects = old_object.copy()

        for new_obj in new_object:
            # Check if there is an object with the same id in old_objects
            existing_obj = next((obj for obj in merged_objects if obj.get("id") == new_obj.get("id")), None)

            if existing_obj is None:
                # If no object with the same id exists, add the new object to the list
                merged_objects.append(new_obj)

        # merged_objects = json.dumps(merged_objects, indent=2)
        print("!!!!")        
        for m_obj in merged_objects:  
            print(m_obj["id"])  
        # print(merged_objects)  
        return merged_objects
    def Delete_old_files(self, content):
        images = []
        if content is None or len(content) == 0:
            images = []
        else:
            for i in range(len(content)):
                images.append(content[i]['web_slug'])
        files_in_folder = os.listdir(self.temp_folder)
        for file_name in files_in_folder:
                file_path = os.path.join(self.temp_folder, file_name)
                if file_name.split('.', 1)[0] not in images:   
                    try:
                        os.remove(file_path)
                        print(f"File '{file_path}' deleted successfully.")                        
                    except FileNotFoundError:
                        print(f"Error: File '{file_path}' not found.")                       
                    except Exception as e:
                        print(f"Error: Unable to delete file '{file_path}'.")
                        print(f"Error details: {e}")           
    def Download_missed_photos(self, contents):       
        if contents is None or len(contents) == 0:
            return
        else: 
            for content in contents:   
                file_path = os.path.join(self.temp_folder, content['web_slug']+".jpg")            
                if not os.path.exists(file_path): 
                    xsmall_image_link = content['images'][0]['xsmall'].split('?', 1)[0]
                    ImageService.SavePhotofromWeb(xsmall_image_link, content['web_slug'])

    

        