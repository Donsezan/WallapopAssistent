import json
import os
from Services.ImageService import ImageService


class FileServices:
    def __init__(self):
            self.temp_folder = "temp"
            self.image_service = ImageService() # Added ImageService instantiation

    def Save_content_to_file(self, data, file_name):
        if data is None or len(data) == 0:
            return "Nothing to save"
        try:
            file_path = os.path.join(self.temp_folder, file_name)
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Object successfully saved to {file_path}")
        except IOError as e:
            print(f"Error saving object to {file_path}: {e}")

    def Rehidrate_from_file(self, file_name):
        try:
            # Open the file in read mode ('r')
            file_path = os.path.join(self.temp_folder, file_name)
            with open(file_path, 'r') as file:
                # Load JSON data from the file
                json_data = json.load(file)
                return json_data

        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
        except json.decoder.JSONDecodeError:
            print(f"Error: Unable to decode JSON in file '{file_name}'. File may be empty or not valid JSON.")

    def Merge_content(self, old_object, new_object):
        if old_object is None and new_object is None:
            return [] # Changed from None to []
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
        for m_obj in merged_objects:  
            print(m_obj["id"])  
        # print(merged_objects)  
        return merged_objects
    
    def Delete_old_images(self, content):
        images = []
        if content is None or len(content) == 0:
            images = []
        else:
            for i in range(len(content)):
                images.append(content[i]['web_slug'])
        files_in_folder = os.listdir(self.temp_folder)
        for file_name in files_in_folder:
                if not file_name.endswith(".json"):
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

    def Delete_old_historys(self, keys):       
        files = os.listdir(self.temp_folder)        
        for file in files:
            if file.startswith("History") and file.endswith(".json"):
                file_stem = os.path.splitext(file)[0]
                history_file_uuid = file_stem.split("_")[-1]
                if history_file_uuid not in keys:
                    file_path = os.path.join(self.temp_folder, file)
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                              
    def Download_missed_photos(self, contents):       
        if contents is None or len(contents) == 0:
            return
        else: 
            for item_content in contents: # Renamed to avoid confusion with the outer 'content' if any
                web_slug = item_content.get('web_slug')
                if not web_slug:
                    print(f"Skipping item due to missing 'web_slug': {item_content}")
                    continue

                # Construct expected file path based on web_slug and default extension .jpg
                # This assumes SavePhotofromWeb will handle adding an appropriate extension if missing.
                # Or that web_slug should be a full filename.
                # For now, let's assume web_slug is a stem and .jpg is desired.
                # This part needs to align with how SavePhotofromWeb constructs filenames.
                # The tests for Download_missed_photos use 'item1.jpg', 'item2.png' based on URL.
                # So, SavePhotofromWeb should derive extension.

                # We need to determine the expected filename *before* checking os.path.exists.
                # The actual filename (including extension) is determined by SavePhotofromWeb.
                # This makes checking for existence beforehand tricky if extension is unknown.
                # Let's assume for now we only check for a .jpg, .png, .gif as common types
                # or rely on SavePhotofromWeb to not re-download if file exists (which it currently does not do).

                # For simplicity, let's assume we need to construct the target filename stem here
                # and SavePhotofromWeb will append the correct extension from the URL.
                # The tests for Download_missed_photos create files like "item2.png", "item1.jpg"
                # So, the file_path check should ideally account for multiple extensions or
                # SavePhotofromWeb should return the actual path it would save to.

                # Given current SavePhotofromWeb, it takes (url, folder_path, file_name_stem_or_full)
                # FileServices calls it with (image_link, self.temp_folder, web_slug)
                # So, web_slug is intended_file_name.

                # The os.path.exists check needs to be more robust or removed if SavePhotofromWeb handles existence.
                # Let's assume common extensions for the check.
                potential_extensions = ['.jpg', '.png', '.gif', '.jpeg']
                image_exists = False
                for ext in potential_extensions:
                    if os.path.exists(os.path.join(self.temp_folder, web_slug + ext)):
                        image_exists = True
                        break

                if not image_exists:
                    images_data = item_content.get('images')
                    if images_data and isinstance(images_data, list) and len(images_data) > 0:
                        image_info = images_data[0]
                        if image_info and isinstance(image_info, dict):
                            xsmall_image_link = image_info.get('xsmall')
                            if xsmall_image_link:
                                xsmall_image_link = xsmall_image_link.split('?', 1)[0]
                                # Call SavePhotofromWeb with (url, folder_path, filename_suggestion)
                                # filename_suggestion here is web_slug. SavePhotofromWeb will add extension.
                                self.image_service.SavePhotofromWeb(xsmall_image_link, self.temp_folder, web_slug)
                            else:
                                print(f"Skipping download for {web_slug} due to missing 'xsmall' image link.")
                        else:
                            print(f"Skipping download for {web_slug} due to invalid image_info structure.")
                    else:
                        print(f"Skipping download for {web_slug} due to missing or invalid 'images' data.")
                    # ImageService.SavePhotofromWeb(xsmall_image_link, content['web_slug']) # Old call

    

        