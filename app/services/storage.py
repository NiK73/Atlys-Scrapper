import os
import json
from pathlib import Path

class StorageService:
    FILE_PATH = Path("data/storage.json")

    def save(self, product):
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        
        # Open the file in append mode, or create it if it doesn't exist
        try:
            # Read existing data
            if os.path.exists(self.FILE_PATH):
                with open(self.FILE_PATH, "r") as file:
                    # Check if file is empty
                    file_content = file.read()
                    if not file_content:
                        data = []  # File is empty, initialize data as an empty list
                    else:
                        data = json.loads(file_content)  # Load existing data from the file
            else:
                data = []  # If file doesn't exist, initialize as empty list

            # Append the new product to the existing data
            data.append(product)

            # Save the updated list to the file
            with open(self.FILE_PATH, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"Error saving product data: {e}")
