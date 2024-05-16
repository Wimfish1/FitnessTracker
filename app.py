import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class FitnessTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fitness Tracker")
        self.root.configure(bg='#f0f0f0')
        self.workouts = []
        self.load_workouts()
        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)
        
        self.tab_workout = ttk.Frame(self.tab_control, style='TFrame')
        self.tab_stats = ttk.Frame(self.tab_control, style='TFrame')

        self.tab_control.add(self.tab_workout, text="Workout")
        self.tab_control.add(self.tab_stats, text="Stats")
        self.tab_control.pack(expand=1, fill="both")

        self.create_workout_tab_ui()
        self.create_stats_tab_ui()

    def create_workout_tab_ui(self):
        self.label_type = ttk.Label(self.tab_workout, text="Workout Type:", style='TLabel', font=('Helvetica', 24, 'bold'))
        self.label_type.pack(pady=20)

        self.entry_type = ttk.Entry(self.tab_workout, font=('Helvetica', 24))
        self.entry_type.pack(pady=20)

        self.label_duration = ttk.Label(self.tab_workout, text="Duration (min):", style='TLabel', font=('Helvetica', 24, 'bold'))
        self.label_duration.pack(pady=20)

        self.entry_duration = ttk.Entry(self.tab_workout, font=('Helvetica', 24))
        self.entry_duration.pack(pady=20)

        self.save_button = ttk.Button(self.tab_workout, text="Save Workout", command=self.save_workout, style='TButton')
        self.save_button.pack(pady=40)

    def create_stats_tab_ui(self):
        self.tree = ttk.Treeview(self.tab_stats, columns=("type", "duration"), show='headings', style='Custom.Treeview')
        self.tree.heading("type", text="Workout Type")
        self.tree.heading("duration", text="Duration (min)")

        self.tree.column("type", anchor=tk.CENTER, width=400)
        self.tree.column("duration", anchor=tk.CENTER, width=400)
        self.tree.pack(expand=1, fill="both", padx=20, pady=20)

        self.delete_button = ttk.Button(self.tab_stats, text="Delete Workout", command=self.delete_workout, style='TButton')
        self.delete_button.pack(pady=40)

        self.display_saved_workouts()

    def save_workout(self):
        workout_type = self.entry_type.get()
        duration = self.entry_duration.get()

        if workout_type and duration:
            self.workouts.append({"type": workout_type, "duration": duration})
            self.display_saved_workouts()
            self.entry_type.delete(0, tk.END)
            self.entry_duration.delete(0, tk.END)
            self.save_workouts()

    def display_saved_workouts(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for workout in self.workouts:
            self.tree.insert("", tk.END, values=(workout["type"], workout["duration"]))

    def delete_workout(self):
        selected_item = self.tree.selection()
        if selected_item:
            workout_values = self.tree.item(selected_item[0])['values']
            workout_dict = {"type": workout_values[0], "duration": workout_values[1]}
            if workout_dict in self.workouts:
                self.workouts.remove(workout_dict)
            self.tree.delete(selected_item)
            self.save_workouts()

    def load_workouts(self):
        if os.path.exists("workouts.json"):
            with open("workouts.json", "r") as file:
                self.workouts = json.load(file)
        else:
            messagebox.showwarning("Warning", "No existing data found. A new file will be created.")
    
    def save_workouts(self):
        with open("workouts.json", "w") as file:
            json.dump(self.workouts, file)

def main():
    root = tk.Tk()

    # Styles
    style = ttk.Style()
    style.configure('TFrame', background='#d1e7dd')
    style.configure('TButton', background='#0f5132', foreground='#ffffff', font=('Helvetica', 24, 'bold'), padding=20)
    style.configure('TLabel', background='#d1e7dd', foreground='#0f5132', font=('Helvetica', 24, 'bold'))
    style.configure('Custom.Treeview', background='#f8f9fa', fieldbackground='#f8f9fa', foreground='#212529', font=('Helvetica', 24))
    style.map('TButton', background=[('active', '#0f5132')], foreground=[('active', '#ffffff')])

    app = FitnessTrackerApp(root)
    root.geometry('800x600')
    root.mainloop()

if __name__ == "__main__":
    main()
