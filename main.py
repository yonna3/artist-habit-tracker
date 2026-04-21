import tkinter as tk
from app import HabitTrackerApp
# THE EXECUTION (The Engine Start)
if __name__ == "__main__":
    root = tk.Tk()
    # Now HabitTrackerApp is defined above, so it won't throw an error!
    app = HabitTrackerApp(root)
    root.mainloop()