import json
import os
from models import Habit

class StorageManager:
    """
    Handles the 'Save' and 'Load' functionality of the app.
    It acts as a translator between our Python Habit objects and the JSON file format.
    """
    def __init__(self, filename="habits.json"):
        # We store the data in a local JSON file. 
        # Keeping the filename as a variable makes it easier to change for testing.
        self.filename = filename
    
    def save_habits(self, habits):
        """
        Takes a list of Habit objects and writes them to a file.
        """
        # We use a list comprehension to convert every Habit object into a dictionary
        # so the 'json' library knows how to format the data.
        data = [habit.to_dict() for habit in habits]

        with open(self.filename, "w") as f:
            # 'indent=4' makes the habits.json file readable by humans, 
            # which is great for debugging!
            json.dump(data, f, indent=4)

    def load_habits(self):
        """
        Retrieves saved data from the file and brings it back to life as Habit objects.
        """
        # Safety Check: If the file doesn't exist (like on the first run), 
        # we return an empty list so the app doesn't crash.
        if not os.path.exists(self.filename):
            return []

        with open(self.filename, "r") as f:
            try:
                data = json.load(f)
                # Re-hydration: We turn the raw dictionary data back into 
                # fully-functional Habit objects using our 'from_dict' method.
                return [Habit.from_dict(item) for item in data]
            except (json.JSONDecodeError, KeyError):
                # If the file is corrupted or formatted incorrectly, 
                # we start fresh with an empty list.
                return []