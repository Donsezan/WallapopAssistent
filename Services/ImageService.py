import os
import requests
import uuid

class ImageService:
    def SavePhotofromWeb(self, actual_url, intended_folder_path, intended_file_name="temp"):
        # Parameter 'actual_url' is the URL.
        # Parameter 'intended_folder_path' is the folder where the image should be saved (was 'file_name' in old signature).
        # Parameter 'intended_file_name' is the desired filename (was 'temp_folder' in old signature).

        # Ensure the target folder exists
        if not os.path.exists(intended_folder_path):
            os.makedirs(intended_folder_path)

        # Determine file extension from URL
        try:
            url_path_part = actual_url.split('?')[0] # Remove query parameters
            _, file_extension = os.path.splitext(url_path_part)
            if not file_extension or len(file_extension) > 5: # Basic sanity check
                file_extension = ".jpg" # Default if no sensible extension
        except:
            file_extension = ".jpg" # Default on any error

        # Generate a unique name if 'intended_file_name' is the default "temp" (meaning it wasn't provided by caller)
        # or if intended_file_name is None or empty (though current tests pass actual filenames)
        final_file_name = ""
        if intended_file_name == "temp" or not intended_file_name:
            final_file_name = str(uuid.uuid4().hex) + file_extension
        else:
            # If intended_file_name already has an extension, use it. Otherwise, add the one from URL.
            name_part, ext_part = os.path.splitext(intended_file_name)
            if not ext_part:
                final_file_name = intended_file_name + file_extension
            else:
                final_file_name = intended_file_name

        # Construct the full file path
        file_path = os.path.join(intended_folder_path, final_file_name)

        # The original code had a check `if not os.path.exists(file_path):`
        # This implies if file exists, it does nothing. Tests expect overwrite for existing files.
        # So, removing that check to allow overwriting.

        try:
            # Make a GET request to download the image
            response = requests.get(actual_url, timeout=10) # Added timeout=10
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

            # Save the image
            with open(file_path, "wb") as file:
                file.write(response.content)

            # These lines should be part of the try block, but outside the with block.
            print(f"Image downloaded and saved at: {file_path}")
            return file_path

        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            return None
        except Exception as e: # General exception handler
            print(f"An unexpected error occurred saving image {actual_url}: {e}")
            return None