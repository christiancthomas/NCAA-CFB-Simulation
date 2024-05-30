import tkinter as tk
from tkinter import scrolledtext
import main  # Import your main.py module

class FootballSimulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("College Football Simulator")
        self.current_week = main.get_current_week()
        self.results = []

        # Create widgets
        self.week_label = tk.Label(master, text=f"Current Week: {self.current_week}")
        self.week_label.pack()

        self.advance_button = tk.Button(master, text="Advance Week", command=self.advance_week)
        self.advance_button.pack()

        self.results_text = scrolledtext.ScrolledText(master, width=50, height=20)
        self.results_text.pack()

        self.display_schedule()

    def advance_week(self):
        main.advance_week()  # Call the function from main.py
        self.current_week = main.get_current_week()
        self.week_label.config(text=f"Current Week: {self.current_week}")
        self.display_schedule()
        self.update_results_display()

    def display_schedule(self):
        schedule = main.get_week_schedule()  # Call the function from main.py
        self.results_text.insert(tk.END, f"\nWeek {self.current_week} Schedule:\n")
        for home, away in schedule:
            self.results_text.insert(tk.END, f"{home} vs {away}\n")

    def update_results_display(self):
        results = main.get_results()  # Call the function from main.py
        self.results_text.insert(tk.END, "\n".join(results) + "\n")
        self.results_text.yview(tk.END)  # Scroll to the end

# Create the main window
root = tk.Tk()
app = FootballSimulatorGUI(root)
root.mainloop()
