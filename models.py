import datetime

class Habit:
    """
    The blueprint for a single art habit. 
    It handles its own data tracking, streak logic, and preparation for storage.
    """
    def __init__(self, name: str, category: str, target_minutes: int = 30):
        # Basic identity of the habit
        self.name = name
        self.category = category 
        self.target_minutes = target_minutes

        # Data Tracking: 
        # We use a dictionary for 'history' because it allows O(1) time complexity 
        # when checking if a specific date exists. 
        # Format: { "YYYY-MM-DD": minutes_spent }
        self.history = {}
        
        # Track when the journey started
        self.created_at = datetime.date.today().isoformat()

    def log_minutes(self, minutes: int, date_str: str = None):
        """
        Adds time to a specific date. If no date is provided, it defaults to today.
        This allows for flexibility if the user wants to log time for a missed day.
        """
        if minutes < 0:
            raise ValueError("Time cannot be negative. We can't un-draw a sketch!")
            
        if date_str is None:
            date_str = datetime.date.today().isoformat()
            
        # Accumulate minutes if the user logs multiple sessions in one day
        self.history[date_str] = self.history.get(date_str, 0) + minutes

    def get_streak(self) -> int:
        """
        Calculates the current consecutive day streak.
        A day only counts toward the streak if the 'target_minutes' goal was met.
        """
        if not self.history:
            return 0

        today = datetime.date.today()
        streak = 0
        current_check = today

        # We step backward through time, day by day, as long as the goal was reached
        while current_check.isoformat() in self.history:
            if self.history[current_check.isoformat()] >= self.target_minutes:
                streak += 1
                current_check -= datetime.timedelta(days=1)
            else:
                # If a day exists but the goal wasn't met, the streak breaks
                break

        return streak

    def get_total_minutes(self) -> int:
        """Returns the lifetime total of all time spent on this specific habit."""
        return sum(self.history.values())
    
    # --- DATA SERIALIZATION ---
    # These methods allow us to convert our Python Objects into JSON-friendly 
    # formats and back again, ensuring our data saves when the app closes.

    def to_dict(self) -> dict:
        """Converts the Habit object into a dictionary for JSON storage."""
        return {
            "name": self.name,
            "category": self.category,
            "target_minutes": self.target_minutes,
            "created_at": self.created_at,
            "history": self.history
        }

    @classmethod 
    def from_dict(cls, data: dict): 
        """Reconstructs a Habit object from a dictionary loaded from JSON."""
        habit = cls(data["name"], data["category"], data["target_minutes"])
        habit.created_at = data["created_at"]
        habit.history = data["history"]
        return habit