import os
import requests
import uuid

class ImageService:
    def SavePhotofromWeb(self, url, file_name, temp_folder="temp"):
         # Ensure the temp folder exists
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder, exist_ok=True) # <--- MODIFIED HERE

        # Generate a unique ID for the file      
        if not file_name:
            file_name = str(uuid.uuid4())[:8]    

        # Get the file extension from the URL
        file_extension = url.split(".")[-1]

        # Construct the file path
        file_path = os.path.join(temp_folder, f"{file_name}.{file_extension}")
        if not os.path.exists(file_path):
            try:
                # Make a GET request to download the image
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

                # Save the image to the temp folder
                with open(file_path, "wb") as file:
                    file.write(response.content)

                print(f"Image downloaded and saved at: {file_path}")
                return file_path

            except requests.exceptions.RequestException as e:
                print(f"Error downloading image: {e}")
                return None