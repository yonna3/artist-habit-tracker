import datetime
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from models import Habit
from storage import StorageManager

class HabitTrackerApp:
    def __init__(self, root):
        # Initializing our custom storage manager and loading existing habit data
        self.storage = StorageManager()
        self.habits = self.storage.load_habits()
        
        # Setting up the main window properties
        self.root = root
        self.root.title("Artist Habit Tracker")
        
        # We lock the window size to 500x600 to ensure the minimalist layout 
        # stays pixel-perfect and consistent on any monitor.
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Color Palette: A custom dark theme designed for long art sessions (low eye strain)
        self.bg_color = "#1e1e2e"       # Deep charcoal background
        self.text_color = "#ffffff"     # Crisp white for readability
        self.accent_color = "#89b4fa"   # Soft pastel blue for primary actions
        self.card_color = "#2b2b3b"     # Slightly lighter gray for habit cards

        self.root.configure(bg=self.bg_color)

        # Header: The app's main title
        self.label = tk.Label(
            self.root,
            text="Artist Daily Habits",
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.label.pack(pady=20)

        # --- PRIMARY ACTION SECTION ---
        # We create a dedicated container at the bottom for the 'Add' button.
        # This keeps the main interaction point consistent and easy to find.
        button_container = tk.Frame(self.root, bg=self.bg_color)
        button_container.pack(side="bottom", fill="x", pady=(10, 30))

        self.style = ttk.Style()
        self.style.theme_use('clam') # 'Clam' allows for more flexible UI element styling

        self.add_button = ttk.Button(
            button_container, 
            text="+ Add New Art Habit", 
            command=self.add_habit_action
        )
        self.add_button.pack(anchor="center") 

        # --- SCROLLABLE HABIT LIST ---
        # The Canvas acts as a 'viewing window' for our list of habits.
        self.canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        # This internal frame is where the actual habit cards are drawn.
        self.habit_frame = tk.Frame(self.canvas, bg=self.bg_color)

        # We dynamically update the scrollable area whenever a new habit is added.
        self.habit_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Centering logic: We place the center of our frame in the center of the canvas (250px).
        self.canvas.create_window((250, 0), window=self.habit_frame, anchor="n", width=440)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Packing the list area to fill the remaining space between the Header and Button.
        self.canvas.pack(fill="both", expand=True) 
        self.scrollbar.pack(side="right", fill="y")

        # Initial draw of the user's habits
        self.refresh_habit_display()

    def add_habit_action(self):
        """Sequence for creating a new habit via user input dialogs."""
        name = simpledialog.askstring("New Habit", "What art habit do you want to start?", parent=self.root)
        if name:
            category = simpledialog.askstring("Category", "Category (Anatomy, Sketch, Color, etc.)")
            if not category: category = "Art" # Fallback category
            
            target = simpledialog.askinteger("Daily Goal", "How many minutes?", initialvalue=30)
            if target:
                new_habit = Habit(name, category, target)
                self.habits.append(new_habit)
                self.storage.save_habits(self.habits) # Persistent save
                self.refresh_habit_display()

    def refresh_habit_display(self):
        """Clears and re-renders the entire habit list to reflect the current state."""
        for widget in self.habit_frame.winfo_children():
            widget.destroy()

        # If the user has no habits, show a friendly 'Empty State' message
        if not self.habits:
            tk.Label(
                self.habit_frame,
                text="No habits yet.\nClick the button below to start the journey! ✨",
                fg="#6c7086", bg=self.bg_color, pady=50, font=("Helvetica", 10)
            ).pack(fill="x")
            return

        for habit in self.habits:
            # Card UI Styling
            card_bg = "#2b2b3b"
            subtext_color = "#6c7086"
            progress_bg = "#45475a"
            success_green = "#a6e3a1"

            # The Card: A container for a single habit's info and buttons
            card = tk.Frame(self.habit_frame, bg=card_bg, padx=15, pady=12)
            card.pack(fill="x", pady=4, padx=5)

            # --- Habit Identity (Name & Category) ---
            info_frame = tk.Frame(card, bg=card_bg)
            info_frame.pack(side="left", expand=True)

            tk.Label(info_frame, text=habit.name, fg="white", bg=card_bg, font=("Helvetica", 11, "bold"), justify="center").pack(anchor="center")
            tk.Label(info_frame, text=habit.category.upper(), fg=subtext_color, bg=card_bg, font=("Helvetica", 7, "bold"), justify="center").pack(anchor="center")

            # --- Interaction Buttons (Delete & Log) ---
            tk.Button(card, text="✕", bg=card_bg, fg="#585b70", relief="flat", command=lambda h=habit: self.delete_habit(h)).pack(side="right", padx=(10, 0))
            tk.Button(card, text="+ Log", bg=self.accent_color, fg=self.bg_color, font=("Helvetica", 9, "bold"), relief="flat", command=lambda h=habit: self.log_time_action(h)).pack(side="right", padx=10)
            
            # Displaying the target goal
            tk.Label(card, text=f"{habit.target_minutes}m", fg=subtext_color, bg=card_bg, font=("Helvetica", 9)).pack(side="right", padx=10)
            
            # Streak Logic: Shows visual progress consistency
            streak_count = habit.get_streak()
            # We change colors based on streak length to provide a 'gamified' feel
            streak_color = "#89b4fa" if streak_count < 3 else "#fab387" if streak_count < 7 else "#f9e2af"
            tk.Label(card, text=f"🔥 {streak_count}", fg=streak_color, bg=card_bg, font=("Helvetica", 10, "bold")).pack(side="right", padx=15)

            # --- Visual Progress Bar ---
            today_str = datetime.date.today().isoformat()
            current_mins = habit.history.get(today_str, 0)
            progress = min(current_mins / habit.target_minutes, 1.0)
            
            canvas = tk.Canvas(card, width=60, height=4, bg=self.bg_color, highlightthickness=0)
            canvas.pack(side="right", padx=5)
            
            # Drawing the progress track (background) and the progress fill (foreground)
            canvas.create_rectangle(0, 0, 60, 4, fill=progress_bg, outline="")
            if progress > 0:
                # The bar turns green once the daily goal is 100% complete
                bar_color = success_green if progress >= 1.0 else self.accent_color
                canvas.create_rectangle(0, 0, progress * 60, 4, fill=bar_color, outline="")

    def log_time_action(self, habit):
        """User interaction to add minutes to a specific habit."""
        try: 
            minutes = simpledialog.askinteger("Log Progress", f"How many minutes of {habit.name} today?")
            if minutes is not None:
                habit.log_minutes(minutes)
                self.storage.save_habits(self.habits)
                self.refresh_habit_display()
                
                # Success notification when a goal is met
                if habit.history.get(datetime.date.today().isoformat(), 0) >= habit.target_minutes:
                    messagebox.showinfo("Goal Reached!", f"Great job! You hit your goal for {habit.name}!")
        except ValueError:
            messagebox.showerror("Input error", "Please enter a valid number for minutes.")

    def delete_habit(self, habit_to_remove):
        """Safely removes a habit with a confirmation check."""
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{habit_to_remove.name}'?")
        if confirm:
            if habit_to_remove in self.habits:
                self.habits.remove(habit_to_remove)
            self.storage.save_habits(self.habits)
            self.refresh_habit_display()