# 🎨 Artist Habit Tracker 

A minimalist desktop application built with Python and Tkinter, designed to help digital artists build consistency through data-driven habit tracking. 

## Technical Overview
This project was developed as a 7-day **sprint** to create a functional, persistent productivity tool for artists. The architecture follows a modular approach to separate data logic from the user interface. 

## Features
* **Minimalist Design:** A simple dark theme that won't strain your eyes during late-night drawing sessions.
* **Smart Streaks:** Tracks how many days in a row you have been hitting your habit goals, indicated by a dynamic flame icon.
* **Progress Bars:** Visual feedback for your daily goals so that you know exactly how much time you have remaining.
* **Auto-Saving:** Everything you log is saved automatically to a local file, ensuring your data persists across sessions.

## What I Learned
During this 7-day sprint, I practiced several key software engineering concepts:
* **Object-Oriented Programming:** Implemented a `Habit` class to manage internal logic, such as history tracking and streak calculations.
* **Data Persistence:** Utilized JSON serialization to ensure user data remains secure and accessible even after the application is closed.
* **GUI Layouts:** Mastered Tkinter's `Canvas` and `Frame` widgets to create a responsive, scrollable list that maintains its alignment.

## How to Use It:
1. **Clone it:** `git clone https://github.com/yonna3/artist-habit-tracker.git`
2. **Run it:** Make sure you have Python installed, then run `python main.py` in your terminal.
3. **Start Tracking:** Add a habit (like "Anatomy Study"), set a goal in minutes, and start logging your time!

## Project Files
- `app.py`: Handles the GUI, event loops, and window layout.
- `models.py`: Contains the core logic for habits and streaks.
- `storage.py`: Manages the saving and loading of data to the JSON file.
